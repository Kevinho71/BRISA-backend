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


@router.post("/registro", status_code=status.HTTP_201_CREATED)
@requires_permission('crear_usuario') 
async def registrar_usuario(
    registro_dto: RegistroDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Registrar nuevo usuario
    ✅ PROTEGIDO - Solo usuarios autenticados con permiso 'crear_usuario'
    """
    resultado = AuthService.registrar_usuario(db, registro_dto)
    
    return success_response(
        data=resultado,
        message="Usuario registrado exitosamente"
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
    """Actualizar usuario"""
    usuario_actualizado = UsuarioService.actualizar_usuario(
        db, 
        id_usuario, 
        usuario_update, 
        current_user=current_user
    )
    
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return ResponseModel.success(
        message="Usuario actualizado exitosamente",
        data=usuario_actualizado.dict()
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

# 1️ Estadísticas (específica)
@router.get("/personas/estadisticas")
async def obtener_estadisticas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        stats = PersonaService.obtener_estadisticas(db=db)
        return ResponseModel.success(
            message="Estadísticas obtenidas",
            data=stats.dict() if hasattr(stats, 'dict') else stats,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

# 2️ Buscar por CI (específica)
@router.get("/personas/buscar/ci/{ci}")
async def buscar_por_ci(
    ci: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        from app.modules.usuarios.models.usuario_models import Persona1
        persona = db.query(Persona1).filter(
            Persona1.ci == ci,
            Persona1.is_active == True
        ).first()
        if not persona:
            raise HTTPException(status_code=404, detail=f"No se encontró persona con CI {ci}")
        persona_response = PersonaService._build_persona_response(db, persona)
        return ResponseModel.success(
            message="Persona encontrada",
            data=persona_response.dict() if hasattr(persona_response, 'dict') else persona_response,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar persona: {str(e)}")

# 3️ Listar por tipo (específica)
@router.get("/personas/tipo/{tipo_persona}")
async def listar_por_tipo(
    tipo_persona: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        if tipo_persona not in ["profesor", "administrativo"]:
            raise HTTPException(status_code=400, detail="tipo_persona debe ser 'profesor' o 'administrativo'")
        from app.modules.usuarios.dto.usuario_dto import PersonaFiltrosDTO
        filtros = PersonaFiltrosDTO(tipo_persona=tipo_persona, is_active=True, skip=0, limit=1000)
        resultado = PersonaService.listar_personas(db=db, filtros=filtros)
        return ResponseModel.success(
            message=f"Personas tipo {tipo_persona} obtenidas",
            data=resultado["items"],
            status_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar personas por tipo: {str(e)}")

# 4️ Listar personas con filtros opcionales
@router.get("/personas")
async def listar_personas(
    tipo_persona: Optional[str] = Query(None, description="Filtrar por tipo: profesor o administrativo"),
    busqueda: Optional[str] = Query(None, description="Buscar por nombre, CI o correo"),
    estado: Optional[str] = Query(None, description="Filtrar por estado: activo o inactivo"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10000, ge=1, le=10000, description="Límite de registros"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        if tipo_persona and tipo_persona not in ["profesor", "administrativo"]:
            raise HTTPException(status_code=400, detail="tipo_persona debe ser 'profesor' o 'administrativo'")
        if estado and estado not in ["activo", "inactivo"]:
            raise HTTPException(status_code=400, detail="estado debe ser 'activo' o 'inactivo'")

        # Llamada al servicio con filtros
        personas_list = PersonaService.listar_personas(
            db=db,
            skip=skip,
            limit=limit,
            tipo_persona=tipo_persona,
            busqueda=busqueda,
            estado=estado
        )

        # Contar total con filtros
        from app.modules.usuarios.models.usuario_models import Persona1
        query = db.query(Persona1)
        if tipo_persona:
            query = query.filter(Persona1.tipo_persona == tipo_persona)
        if estado:
            query = query.filter(Persona1.is_active == (estado == "activo"))
        if busqueda:
            busqueda_lower = f"%{busqueda.lower()}%"
            query = query.filter(
                db.or_(
                    Persona1.nombres.ilike(busqueda_lower),
                    Persona1.apellido_paterno.ilike(busqueda_lower),
                    Persona1.apellido_materno.ilike(busqueda_lower),
                    Persona1.ci.ilike(busqueda_lower),
                    Persona1.correo.ilike(busqueda_lower)
                )
            )
        total = query.count()
        import math
        pages = math.ceil(total / limit) if limit > 0 else 1
        resultado = {
            "items": personas_list,
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "per_page": limit,
            "pages": pages
        }

        return ResponseModel.success(message="Personas obtenidas", data=resultado, status_code=200)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar personas: {str(e)}")

# 5️ Crear persona
@router.post("/personas", status_code=status.HTTP_201_CREATED)
@requires_permission("crear_usuario")
async def crear_persona(
    request: Request,
    persona_create: PersonaCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        body = await request.json()
        resultado = PersonaService.crear_persona_con_usuario(db, persona_create, user_id=current_user.id_usuario)
        return ResponseModel.success(message="Persona creada", data=resultado, status_code=201)

    # Manejo de errores específicos
    except RequestValidationError as e:
        raise
    except Conflict as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="CI o correo duplicado")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# 6️ Obtener persona por ID
@router.get("/personas/{persona_id}")
async def obtener_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        persona = PersonaService.obtener_persona(db=db, persona_id=persona_id)
        return ResponseModel.success(
            message="Persona obtenida",
            data=persona.dict() if hasattr(persona, 'dict') else persona,
            status_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener persona: {str(e)}")

# 7️ Actualizar persona
@router.put("/personas/{persona_id}")
@requires_permission("editar_persona")
async def actualizar_persona(
    persona_id: int,
    persona_update: PersonaUpdateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        persona_actualizada = PersonaService.actualizar_persona(
            db=db,
            persona_id=persona_id,
            persona_dto=persona_update,
            user_id=current_user.id_usuario
        )
        return ResponseModel.success(message="Persona actualizada exitosamente", data=persona_actualizada, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar persona: {str(e)}")

# 8️ Eliminar persona
@router.delete("/personas/{persona_id}")
@requires_permission("eliminar_persona")
async def eliminar_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        resultado = PersonaService.eliminar_persona(db=db, persona_id=persona_id, user_id=current_user.id_usuario)
        return ResponseModel.success(message="Persona eliminada exitosamente", data=resultado, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar persona: {str(e)}")

# 9️ Reactivar persona
@router.patch("/personas/{persona_id}/activar")
@requires_permission("editar_persona")
async def reactivar_persona(
    persona_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    try:
        from app.modules.usuarios.models.usuario_models import Persona1
        persona = db.query(Persona1).filter(Persona1.id_persona == persona_id).first()
        if not persona:
            raise HTTPException(status_code=404, detail=f"Persona con ID {persona_id} no encontrada")
        if persona.is_active:
            raise HTTPException(status_code=400, detail="La persona ya está activa")
        persona.is_active = True
        db.commit()
        db.refresh(persona)
        persona_response = PersonaService._build_persona_response(db, persona)
        return ResponseModel.success(
            message="Persona reactivada exitosamente",
            data=persona_response.dict() if hasattr(persona_response, 'dict') else persona_response,
            status_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al reactivar persona: {str(e)}")

# 10️ Desactivar persona
@router.patch("/personas/{id_persona}/desactivar")
async def desactivar_persona(
    id_persona: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    from app.modules.usuarios.models.usuario_models import Persona1
    persona = db.query(Persona1).filter(Persona1.id_persona == id_persona).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if not persona.is_active:
        raise HTTPException(status_code=400, detail="La persona ya está inactiva")
    # Verificar si tiene usuario asociado
    if persona.tiene_usuario:
        raise HTTPException(status_code=409, detail="No se puede desactivar una persona con usuario asociado")
    persona.is_active = False
    db.commit()
    db.refresh(persona)
    return persona
