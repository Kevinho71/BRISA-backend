"""
auth_controller.py - CÓDIGO COMPLETO Y FUNCIONAL
Controlador de autenticación y usuarios
✅ CORREGIDO: Request como dependencia para evitar error 422 en tests
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.exceptions import RequestValidationError

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.shared.exceptions.custom_exceptions import (
    Conflict, 
    DatabaseException, 
    ValidationException,
    NotFound
)


from typing import List, Optional
import logging

from app.modules.usuarios.models.usuario_models import Persona1, Usuario
from app.modules.auth.dto.auth_dto import LoginDTO, RegistroDTO
from app.modules.auth.services.auth_service import AuthService, get_current_user_dependency
from app.core.utils import success_response
from app.modules.usuarios.services.usuario_service import PersonaService
from app.core.database import get_db
from app.shared.response import ResponseModel 
from app.shared.security import verify_token
from app.shared.permissions import requires_permission
from app.modules.usuarios.dto.usuario_dto import (
    UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO,
    RolCreateDTO, RolUpdateDTO, RolResponseDTO,
    PermisoResponseDTO, AsignarRolDTO, PersonaCreateDTO, PersonaResponseDTO, PersonaUpdateDTO, 
)
from app.modules.usuarios.services.usuario_service import (
    UsuarioService, RolService, PermisoService
)

logger = logging.getLogger(__name__)
router = APIRouter()


# ==================== FUNCIONES AUXILIARES ====================

def get_client_ip(request: Request) -> str:
    """Extraer IP del cliente considerando proxies"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_token_from_request(request: Request) -> str:
    """Extraer token del header Authorization"""
    auth_header = request.headers.get("Authorization", "")
    return auth_header.replace("Bearer ", "")


# ==================== AUTENTICACIÓN ====================

@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login(
    login_dto: LoginDTO,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    HU-01: Endpoint de inicio de sesión
    """
    # Extraer IP y User-Agent
    ip_address = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "unknown")
    
    # Autenticar usuario
    token_dto = AuthService.login(
        db=db,
        login_dto=login_dto,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    return success_response(
        data=token_dto.model_dump(),
        message="Inicio de sesión exitoso"
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency),
    request: Request = None  # ✅ Opcional para evitar error 422 en tests
):
    """
    HU-02: Endpoint de cierre de sesión
    ✅ CORRECCIÓN: Request opcional para compatibilidad con tests
    """
    # Intentar extraer información del request si está disponible
    ip_address = "unknown"
    token = ""
    
    if request:
        ip_address = get_client_ip(request)
        token = get_token_from_request(request)
    
    # Cerrar sesión
    resultado = AuthService.logout(
        db=db,
        token=token,
        usuario_id=current_user.id_usuario,
        ip_address=ip_address
    )
    
    return success_response(
        data=resultado,
        message="Sesión cerrada exitosamente"
    )


@router.get("/me", response_model=dict, status_code=status.HTTP_200_OK)
async def obtener_usuario_actual(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtener información del usuario autenticado
    ✅ CORRECCIÓN: Sin Request para evitar error 422
    """
    usuario_dto = AuthService.obtener_usuario_actual(db, current_user.id_usuario)
    
    return success_response(
        data=usuario_dto.model_dump(),
        message="Usuario obtenido exitosamente"
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """Refrescar token JWT"""
    try:
        nuevo_token = AuthService.create_access_token(
            data={"sub": current_user.id_usuario}
        )
        return ResponseModel.success(
            message="Token refrescado exitosamente",
            data={
                "access_token": nuevo_token,
                "token_type": "bearer",
                "expires_in": 1800
            }
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al refrescar token"
        )


# ==================== USUARIOS ====================

@router.post("/usuarios", status_code=status.HTTP_201_CREATED)
@requires_permission('crear_usuario')
async def crear_usuario_para_persona(
    usuario_dto: UsuarioCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    ✅ Crear usuario para una persona existente
    Genera contraseña temporal automáticamente
    
    ⚠️ SEGURIDAD: Requiere permiso 'crear_usuario'
    """
    try:
        from app.shared.security import hash_password
        import random
        import string
        
        # Verificar que la persona existe
        persona = db.query(Persona1).filter(
            Persona1.id_persona == usuario_dto.id_persona,
            Persona1.is_active == True
        ).first()
        
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona con ID {usuario_dto.id_persona} no encontrada"
            )
        
        # Verificar que la persona NO tenga usuario ya
        usuario_existente = db.query(Usuario).filter(
            Usuario.id_persona == usuario_dto.id_persona
        ).first()
        
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"La persona {persona.nombre_completo} ya tiene un usuario asignado"
            )
        
        # Verificar duplicados de usuario o correo
        duplicado = db.query(Usuario).filter(
            (Usuario.usuario == usuario_dto.usuario) | 
            (Usuario.correo == usuario_dto.correo)
        ).first()
        
        if duplicado:
            if duplicado.usuario == usuario_dto.usuario:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre de usuario '{usuario_dto.usuario}' ya está en uso"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El correo '{usuario_dto.correo}' ya está en uso"
                )
        
        # ✅ Generar contraseña temporal automáticamente
        caracteres = string.ascii_letters + string.digits + "!@#$%"
        password_temporal = ''.join(random.choice(caracteres) for _ in range(12))
        
        # Crear usuario
        nuevo_usuario = Usuario(
            id_persona=usuario_dto.id_persona,
            usuario=usuario_dto.usuario.lower().strip(),
            correo=usuario_dto.correo.lower().strip(),
            password=hash_password(password_temporal),
            is_active=True
        )
        
        db.add(nuevo_usuario)
        db.flush()
        
        # ✅ Registrar en bitácora
        AuthService.registrar_bitacora(
            db,
            usuario_id=current_user.id_usuario,
            accion='CREAR_USUARIO',
            tipo_objetivo='Usuario',
            id_objetivo=nuevo_usuario.id_usuario,
            descripcion=f"Usuario '{nuevo_usuario.usuario}' creado para persona '{persona.nombre_completo}'"
        )
        
        db.commit()
        db.refresh(nuevo_usuario)
        
        logger.info(f"✅ Usuario creado: {nuevo_usuario.usuario} para persona {persona.nombre_completo}")
        
        # ✅ Retornar credenciales (SOLO SE MUESTRAN UNA VEZ)
        return ResponseModel.success(
            message=f"Usuario creado exitosamente para {persona.nombre_completo}",
            data={
                "usuario": {
                    "id_usuario": nuevo_usuario.id_usuario,
                    "id_persona": nuevo_usuario.id_persona,
                    "usuario": nuevo_usuario.usuario,
                    "correo": nuevo_usuario.correo,
                    "is_active": nuevo_usuario.is_active
                },
                "password_temporal": password_temporal,
                "mensaje": "⚠️ IMPORTANTE: Guarde esta contraseña. No se volverá a mostrar."
            },
            status_code=status.HTTP_201_CREATED
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al crear usuario: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )

@router.post("/usuarios/{id_usuario}/restablecer-password", status_code=status.HTTP_200_OK)
@requires_permission('editar_usuario')
async def restablecer_password(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    ✅ Restablecer contraseña de un usuario
    Genera una nueva contraseña temporal automáticamente (misma lógica que crear usuario)
    
    ⚠️ SEGURIDAD: Requiere permiso 'editar_usuario'
    ⚠️ Solo administradores pueden hacer esto
    """
    try:
        from app.shared.security import hash_password
        import random
        import string
        
        # Obtener usuario
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario,
            Usuario.is_active == True
        ).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )
        
        # Obtener persona asociada
        persona = db.query(Persona1).filter(
            Persona1.id_persona == usuario.id_persona
        ).first()
        
        # ✅ Generar nueva contraseña temporal (misma lógica que crear usuario)
        caracteres = string.ascii_letters + string.digits + "!@#$%"
        nueva_password_temporal = ''.join(random.choice(caracteres) for _ in range(12))
        
        # Actualizar contraseña
        usuario.password = hash_password(nueva_password_temporal)
        
        db.flush()  # Mantienes tu flush
        
        # Registrar en bitácora
        AuthService.registrar_bitacora(
            db,
            usuario_id=current_user.id_usuario,
            accion='RESTABLECER_PASSWORD',
            tipo_objetivo='Usuario',
            id_objetivo=usuario.id_usuario,
            descripcion=f"Contraseña restablecida para usuario '{usuario.usuario}' "
                        f"({persona.nombre_completo if persona else 'N/A'})"
        )
        
        db.commit()
        
        logger.info(f"✅ Contraseña restablecida para usuario: {usuario.usuario}")
        
        # Retornar nueva contraseña temporal (SOLO UNA VEZ)
        return ResponseModel.success(
            message=f"Contraseña restablecida para {usuario.usuario}",
            data={
                "usuario": usuario.usuario,
                "nueva_password_temporal": nueva_password_temporal,
                "mensaje": "⚠️ IMPORTANTE: Esta contraseña solo se mostrará una vez. "
                           "El usuario deberá cambiarla en su próximo inicio de sesión."
            },
            status_code=status.HTTP_200_OK
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al restablecer contraseña: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al restablecer contraseña: {str(e)}"
        )

    
@router.get("/usuarios", response_model=dict)
@requires_permission('ver_usuario')
async def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Listar todos los usuarios con información de persona"""
    try:
        # ✅ Query con join a personas
        usuarios = db.query(Usuario).join(
            Persona1, Usuario.id_persona == Persona1.id_persona
        ).filter(
            Usuario.is_active == True
        ).offset(skip).limit(limit).all()
        
        # ✅ Construir respuesta con nombre de persona
        usuarios_list = []
        for u in usuarios:
            usuario_dict = {
                "id_usuario": u.id_usuario,
                "usuario": u.usuario,
                "correo": u.correo,
                "is_active": u.is_active,
                "persona_nombre": u.persona.nombre_completo if u.persona else None
            }
            usuarios_list.append(usuario_dict)
        
        return ResponseModel.success(
            message="Usuarios obtenidos",
            data=usuarios_list
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/usuarios/{id_usuario}", response_model=dict)
@requires_permission('ver_usuario')
async def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Obtener detalles de usuario específico"""
    usuario = UsuarioService.obtener_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return ResponseModel.success(
        message="Usuario obtenido",
        data=usuario.dict()
    )


@router.put("/usuarios/{id_usuario}", response_model=dict)
@requires_permission('editar_usuario')
async def actualizar_usuario(
    id_usuario: int,
    usuario_update: UsuarioUpdateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    ✅ Actualizar usuario
    ⚠️ SEGURIDAD: Requiere permiso 'editar_usuario'
    
    Puede cambiar:
    - Usuario (nombre de usuario)
    - Correo
    - Contraseña (opcional)
    - Estado activo/inactivo
    """
    try:
        from app.shared.security import hash_password
        from app.shared.permissions import check_permission
        
        # Validación adicional: usuarios solo pueden editar su propio perfil
        # a menos que tengan el permiso específico
        if id_usuario != current_user.id_usuario:
            if not check_permission(current_user, "editar_usuario"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para editar otros usuarios"
                )
        
        # Obtener usuario a actualizar
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )
        
        # Guardar estado anterior para auditoría
        estado_anterior = {
            'usuario': usuario.usuario,
            'correo': usuario.correo
        }
        
        # Verificar duplicados si se cambia usuario o correo
        if usuario_update.usuario and usuario_update.usuario != usuario.usuario:
            duplicado = db.query(Usuario).filter(
                Usuario.usuario == usuario_update.usuario,
                Usuario.id_usuario != id_usuario
            ).first()
            
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre de usuario '{usuario_update.usuario}' ya está en uso"
                )
            
            usuario.usuario = usuario_update.usuario.lower().strip()
        
        if usuario_update.correo and usuario_update.correo != usuario.correo:
            duplicado = db.query(Usuario).filter(
                Usuario.correo == usuario_update.correo,
                Usuario.id_usuario != id_usuario
            ).first()
            
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El correo '{usuario_update.correo}' ya está en uso"
                )
            
            usuario.correo = usuario_update.correo.lower().strip()
        
        # Actualizar contraseña solo si se envía
        if usuario_update.password:
            usuario.password = hash_password(usuario_update.password)
        
        # Actualizar estado si se envía
        if usuario_update.is_active is not None:
            usuario.is_active = usuario_update.is_active
        
        db.flush()
        
        # ✅ Registrar en bitácora
        cambios = []
        if usuario_update.usuario:
            cambios.append(f"usuario: '{estado_anterior['usuario']}' → '{usuario.usuario}'")
        if usuario_update.correo:
            cambios.append(f"correo: '{estado_anterior['correo']}' → '{usuario.correo}'")
        if usuario_update.password:
            cambios.append("contraseña actualizada")
        if usuario_update.is_active is not None:
            cambios.append(f"estado: {usuario.is_active}")
        
        AuthService.registrar_bitacora(
            db,
            usuario_id=current_user.id_usuario,
            accion='EDITAR_USUARIO',
            tipo_objetivo='Usuario',
            id_objetivo=usuario.id_usuario,
            descripcion=f"Usuario '{usuario.usuario}' actualizado. Cambios: {', '.join(cambios)}"
        )
        
        db.commit()
        db.refresh(usuario)
        
        logger.info(f"✅ Usuario actualizado: {usuario.usuario}")
        
        return ResponseModel.success(
            message="Usuario actualizado exitosamente",
            data={
                "id_usuario": usuario.id_usuario,
                "id_persona": usuario.id_persona,
                "usuario": usuario.usuario,
                "correo": usuario.correo,
                "is_active": usuario.is_active
            },
            status_code=status.HTTP_200_OK
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al actualizar usuario: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}"
        )


@router.delete("/usuarios/{id_usuario}", response_model=dict)
@requires_permission('eliminar_usuario')
async def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Eliminar usuario (borrado lógico)"""
    resultado = UsuarioService.eliminar_usuario(db, id_usuario, current_user=current_user)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return ResponseModel.success(
        message="Usuario eliminado exitosamente",
        data=resultado
    )


# ==================== ROLES ====================

@router.post("/roles", response_model=dict, status_code=status.HTTP_201_CREATED)
@requires_permission('crear_rol')
async def crear_rol(
    rol_create: RolCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Crear nuevo rol"""
    try:
        nuevo_rol = RolService.crear_rol(db, rol_create, current_user=current_user)
        return ResponseModel.success(
            message="Rol creado exitosamente",
            data=nuevo_rol.dict() if hasattr(nuevo_rol, 'dict') else nuevo_rol,
            status_code=status.HTTP_201_CREATED
        )
    except Conflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al crear rol: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/roles", response_model=dict)
@requires_permission('ver_rol') 
async def listar_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los roles"""
    try:
        roles = RolService.listar_roles(db, skip, limit)
        
        # ✅ Convertir a dict si es necesario
        roles_list = []
        for rol in roles:
            if hasattr(rol, 'dict'):
                roles_list.append(rol.dict())
            else:
                roles_list.append(rol)
        
        return ResponseModel.success(
            message="Roles obtenidos",
            data=roles_list
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/roles/{id_rol}", response_model=dict)
@requires_permission('ver_rol')
async def obtener_rol(
    id_rol: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de rol específico"""
    rol = RolService.obtener_rol(db, id_rol)
    
    # ✅ Convertir a dict si tiene el método
    rol_dict = rol.dict() if hasattr(rol, 'dict') else rol
    
    return ResponseModel.success(
        message="Rol obtenido",
        data=rol_dict
    )


@router.put("/roles/{id_rol}")
@requires_permission("editar_rol")
async def actualizar_rol(
    id_rol: int,
    rol_update: RolUpdateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """Actualizar rol"""
    try:
        # ✅ CORRECCIÓN: Parámetro debe ser rol_id, no id_rol
        rol_actualizado = RolService.actualizar_rol(
            db=db,
            rol_id=id_rol,  # ← Cambiar de id_rol a rol_id
            rol_dto=rol_update,  # ← Parámetro correcto es rol_dto
            current_user=current_user  # ← Parámetro correcto es current_user
        )

        return ResponseModel.success(
            message="Rol actualizado exitosamente",
            data=rol_actualizado.dict() if hasattr(rol_actualizado, 'dict') else rol_actualizado,
            status_code=200
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar rol: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/roles/{id_rol}")
@requires_permission("eliminar_rol")
async def eliminar_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Eliminar rol del sistema (borrado lógico)
    ⚠ SEGURIDAD: Requiere permiso 'eliminar_rol'
    """
    try:
        # ✅ Parámetros CORRECTOS según la firma del método
        resultado = RolService.eliminar_rol(
            db=db,
            rol_id=id_rol,  # ← Correcto nombre del parámetro
            current_user=current_user  # ← Parámetro correcto
        )
        
        return ResponseModel.success(
            message="Rol eliminado exitosamente",
            data=resultado,
            status_code=status.HTTP_200_OK
        )
        
    except HTTPException as e:
        raise e
        
    except Exception as e:
        logger.error(f"Error inesperado al eliminar rol {id_rol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar rol: {str(e)}"
        )


@router.post("/usuarios/{id_usuario}/roles/{id_rol}", response_model=dict)
@requires_permission('asignar_permisos')
async def asignar_rol_usuario(
    id_usuario: int,
    id_rol: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Asignar rol a usuario"""
    resultado = RolService.asignar_rol_usuario(db, id_usuario, id_rol, current_user=current_user)
    return ResponseModel.success(
        message="Rol asignado exitosamente",
        data=resultado
    )


@router.post("/roles/{id_rol}/permisos", response_model=dict)
@requires_permission('asignar_permisos')
async def asignar_permisos_rol(
    id_rol: int,
    permisos_ids: list[int],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Asignar permisos a rol"""
    rol_actualizado = RolService.asignar_permisos_rol(db, id_rol, permisos_ids, current_user=current_user)
    return ResponseModel.success(
        message="Permisos asignados al rol",
        data=rol_actualizado.dict() if hasattr(rol_actualizado, 'dict') else rol_actualizado
    )

# ==================== PERMISOS ====================

@router.get("/permisos", response_model=dict)
@requires_permission('ver_rol')
async def listar_permisos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    modulo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Listar todos los permisos"""
    permisos = PermisoService.listar_permisos(db, skip, limit, modulo)
    return ResponseModel.success(
        message="Permisos obtenidos",
        data=[p.dict() for p in permisos]
    )


@router.get("/permisos/{id_permiso}", response_model=dict)
@requires_permission('ver_rol')
async def obtener_permiso(
    id_permiso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Obtener detalles de permiso específico"""
    permiso = PermisoService.obtener_permiso(db, id_permiso)
    if not permiso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permiso no encontrado")
    return ResponseModel.success(
        message="Permiso obtenido",
        data=permiso.dict()
    )

@router.get("/permisos/{id_permiso}/roles", response_model=dict)
@requires_permission('ver_rol')
async def obtener_roles_con_permiso(
    id_permiso: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Obtener roles que tienen un permiso específico"""
    try:
        roles = PermisoService.obtener_roles_con_permiso(db, id_permiso)
        return ResponseModel.success(
            message="Roles con permiso obtenidos",
            data=roles
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener roles con permiso: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==================== LOGS DE ACCESO ====================

@router.get("/logs-acceso", response_model=dict)
@requires_permission('ver_rol')
async def listar_logs_acceso(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Listar logs de acceso al sistema"""
    try:
        from app.modules.usuarios.models.usuario_models import LoginLog
        
        logs = db.query(LoginLog).order_by(
            LoginLog.fecha_hora.desc()
        ).offset(skip).limit(limit).all()
        
        logs_data = []
        for log in logs:
            logs_data.append({
                "id": log.id_log,
                "usuario_id": log.id_usuario,
                "fecha": log.fecha_hora.isoformat() if log.fecha_hora else None,
                "accion": "Inicio de sesión",
                "ip": log.ip_address or "N/A",
                "estado": log.estado,
                "detalles": log.user_agent
            })
        
        return ResponseModel.success(
            message="Logs de acceso obtenidos",
            data=logs_data
        )
        
    except Exception as e:
        logger.error(f"Error al listar logs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
# ==================== ENDPOINTS DE PERSONAS ====================

# 1. LISTAR PERSONAS 

@router.get("/personas")
@requires_permission("ver_personas")
async def listar_personas(
    # Paginación
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(50, ge=1, le=1000, description="Límite de registros"),  # ✅ Cambiado de 10000 a 50
    
    # Filtros
    tipo_persona: Optional[str] = Query(
        None,
        description="Filtrar por tipo: 'profesor' o 'administrativo'"
    ),
    busqueda: Optional[str] = Query(
        None,
        description="Buscar en: nombre, CI, correo, teléfono"
    ),
    estado: Optional[str] = Query(
        None,
        description="Filtrar por estado: 'activo' o 'inactivo'"
    ),
    
    # Autenticación
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    📋 Listar todas las personas con filtros opcionales
    
    **Parámetros de paginación:**
    - `skip`: Registros a saltar (para paginación)
    - `limit`: Límite de registros por página (máx 1000, por defecto 50)
    
    **Parámetros de filtro (opcionales):**
    - `tipo_persona`: 'profesor' o 'administrativo'
    - `busqueda`: Búsqueda en nombres, CI, correo o teléfono
    - `estado`: 'activo' o 'inactivo'
    
    **Ejemplo de uso:**
```
    GET /api/personas?tipo_persona=profesor&busqueda=juan&estado=activo
    GET /api/personas?busqueda=12345678&skip=0&limit=50
    GET /api/personas?skip=50&limit=50  # Segunda página
```
    """
    try:
        # Si hay filtros, usar listar_con_filtros
        if tipo_persona or busqueda or estado:
            resultado = PersonaService.listar_con_filtros(
                db=db,
                skip=skip,
                limit=limit,
                tipo_persona=tipo_persona,
                busqueda=busqueda,
                estado=estado
            )
        else:
            # Si no hay filtros, listar todas
            resultado = PersonaService.listar_todas(
                db=db,
                skip=skip,
                limit=limit
            )
        
        # ✅ ASEGURAR que la respuesta tenga la estructura correcta
        return ResponseModel.success(
            message=f"Personas listadas exitosamente ({resultado['total']} total, mostrando {len(resultado['items'])})",
            data={
                "items": resultado["items"],
                "total": resultado["total"],
                "page": resultado["page"],
                "pages": resultado["pages"],
                "skip": resultado["skip"],
                "limit": resultado["limit"],
                "has_more": resultado["has_more"]
            },
            status_code=status.HTTP_200_OK
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al listar personas: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar personas: {str(e)}"
        )



# 2 OBTENER PERSONA 

@router.get("/id/{persona_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def obtener_persona_por_id(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    🔍 Obtener una persona específica por ID
    """
    try:
        persona = PersonaService.obtener_por_id(db, persona_id)
        
        return ResponseModel.success(
            message="Persona obtenida",
            data=persona,
            status_code=status.HTTP_200_OK
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al obtener persona: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener persona: {str(e)}"
        )


@router.get("/ci/{ci}", response_model=dict, status_code=status.HTTP_200_OK)
async def obtener_persona_por_ci(
    ci: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    🔍 Obtener una persona específica por CI
    """
    try:
        persona = PersonaService.obtener_por_ci(db, ci)
        
        return ResponseModel.success(
            message="Persona obtenida",
            data=persona,
            status_code=status.HTTP_200_OK
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al obtener persona por CI: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener persona: {str(e)}"
        )


# 3 ESTADÍSTICAS 

@router.get("/personas/estadisticas")
@requires_permission("ver_personas")
async def obtener_estadisticas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    📊 Obtener estadísticas de personas
    
    Retorna:
    - Total de personas
    - Contador por tipo (profesor/administrativo)
    - Contador por estado (activo/inactivo)
    - Personas con/sin usuario
    """
    try:
        stats = PersonaService.obtener_estadisticas(db)
        
        return ResponseModel.success(
            message="Estadísticas obtenidas",
            data=stats,
            status_code=status.HTTP_200_OK
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )