"""
usuario_controller.py 
Controlador de usuarios, roles y permisos
"""
from fastapi import APIRouter, Depends, HTTPException, logger, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.shared.permissions import requires_permission, check_permission
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.modules.usuarios.models.usuario_models import Persona1, Rol, Usuario
from app.modules.usuarios.dto.usuario_dto import (
    UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO,
    RolCreateDTO, RolUpdateDTO, RolResponseDTO,
    PermisoResponseDTO, AsignarRolDTO
)
from app.modules.usuarios.services.usuario_service import (
    UsuarioService, RolService, PermisoService
)

router = APIRouter()

# ==================== ENDPOINTS DE USUARIOS ====================

@router.post("", status_code=status.HTTP_201_CREATED)
@requires_permission("crear_usuario")
async def crear_usuario(
    usuario_create: UsuarioCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Crear nuevo usuario (RF-01)
    ⚠️ SEGURIDAD: Requiere permiso 'crear_usuario'
    """
    try:
        nuevo_usuario = UsuarioService.crear_usuario(
            db, 
            usuario_create, 
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Usuario creado exitosamente",
            data=nuevo_usuario.dict() if hasattr(nuevo_usuario, 'dict') else nuevo_usuario,
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )
    
@router.get("/{id_usuario}")
async def obtener_usuario(
    id_usuario: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de usuario específico"""
    try:
        usuario = UsuarioService.obtener_usuario(db, id_usuario)
        
        return ResponseModel.success(
            message="Usuario obtenido",
            data=usuario.dict() if hasattr(usuario, 'dict') else usuario,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al obtener usuario: {str(e)}"
        )

@router.get("")
async def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    estado: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los usuarios (RF-01)"""
    try:
        usuarios = UsuarioService.listar_usuarios(db, skip, limit, estado)
        return ResponseModel.success(
            message="Usuarios obtenidos",
            data=[u.dict() if hasattr(u, 'dict') else u for u in usuarios],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar usuarios: {str(e)}"
        )

@router.put("/{id_usuario}")
@requires_permission("editar_usuario")
async def actualizar_usuario(
    id_usuario: int,
    usuario_update: UsuarioUpdateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Actualizar usuario (RF-06)
    ⚠️ SEGURIDAD: Requiere permiso 'editar_usuario'
    
    Audita todos los cambios realizados
    """
    try:
        # Validación adicional: usuarios solo pueden editar su propio perfil
        # a menos que tengan el permiso específico
        if id_usuario != current_user.id_usuario:
            if not check_permission(current_user, "editar_usuario"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para editar otros usuarios"
                )
        
        usuario_actualizado = UsuarioService.actualizar_usuario(
            db, 
            id_usuario, 
            usuario_update, 
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Usuario actualizado exitosamente",
            data=usuario_actualizado.dict() if hasattr(usuario_actualizado, 'dict') else usuario_actualizado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}"
        )

@router.delete("/{id_usuario}")
@requires_permission("eliminar_usuario")
async def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Eliminar usuario (borrado lógico) (RF-06)
    ⚠️ SEGURIDAD: Requiere permiso 'eliminar_usuario'
    
    Marca el usuario como inactivo
    """
    try:
        # Validación: no permitir auto-eliminación
        if id_usuario == current_user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar tu propia cuenta"
            )
        
        resultado = UsuarioService.eliminar_usuario(
            db, 
            id_usuario, 
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Usuario eliminado exitosamente",
            data=resultado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}"
        )


# ==================== ENDPOINTS DE ROLES ====================

@router.post("/roles")
@requires_permission("crear_rol")
async def crear_rol(
    rol_create: RolCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Crear nuevo rol (RF-03)
    ⚠️ SEGURIDAD: Requiere permiso 'crear_rol'
    """
    try:
        nuevo_rol = RolService.crear_rol(
            db, 
            rol_create, 
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Rol creado exitosamente",
            data=nuevo_rol.dict() if hasattr(nuevo_rol, 'dict') else nuevo_rol,
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear rol: {str(e)}"
        )

@router.get("/roles")
async def listar_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los roles"""
    try:
        roles = RolService.listar_roles(db, skip, limit)
        
        return ResponseModel.success(
            message="Roles obtenidos",
            data=[r.dict() if hasattr(r, 'dict') else r for r in roles],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar roles: {str(e)}"
        )

@router.get("/roles/{id_rol}")
async def obtener_rol(
    id_rol: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de rol específico"""
    try:
        rol = RolService.obtener_rol(db, id_rol)
        
        return ResponseModel.success(
            message="Rol obtenido",
            data=rol.dict() if hasattr(rol, 'dict') else rol,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al obtener rol: {str(e)}"
        )


@router.get("/roles/{id_rol}/usuarios", response_model=dict)
@requires_permission('ver_rol')
async def obtener_usuarios_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    👥 Obtener usuarios asignados a un rol específico
    
    Retorna lista de usuarios con:
    - Información básica del usuario
    - Información de la persona asociada
    - Estado activo/inactivo
    """
    try:
        # Verificar que el rol existe
        rol = db.query(Rol).filter(
            Rol.id_rol == id_rol,
            Rol.is_active == True
        ).first()
        
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {id_rol} no encontrado"
            )
        
        # Obtener usuarios con este rol (solo activos)
        usuarios_data = []
        for usuario in rol.usuarios:
            if usuario.is_active:
                # Obtener información de la persona
                persona = db.query(Persona1).filter(
                    Persona1.id_persona == usuario.id_persona
                ).first()
                
                usuarios_data.append({
                    "id_usuario": usuario.id_usuario,
                    "usuario": usuario.usuario,
                    "email": usuario.correo,
                    "activo": usuario.is_active,
                    # Información de la persona
                    "nombre": persona.nombres if persona else None,
                    "apellido": f"{persona.apellido_paterno or ''} {persona.apellido_materno or ''}".strip() if persona else None,
                    "nombre_completo": persona.nombre_completo if persona else None,
                    "ci": persona.ci if persona else None,
                    "tipo_persona": persona.tipo_persona if persona else None
                })
        
        logger.info(f"✅ Usuarios del rol {id_rol} obtenidos: {len(usuarios_data)}")
        
        return ResponseModel.success(
            message=f"Usuarios del rol obtenidos ({len(usuarios_data)} usuarios)",
            data=usuarios_data,
            status_code=status.HTTP_200_OK
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al obtener usuarios del rol {id_rol}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios del rol: {str(e)}"
        )


@router.post("/{id_usuario}/roles/{id_rol}")
@requires_permission("asignar_permisos")
async def asignar_rol_usuario(
    id_usuario: int,
    id_rol: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Asignar rol a usuario (RF-02)
    ⚠️ SEGURIDAD: Requiere permiso 'asignar_permisos'
    """
    try:
        resultado = UsuarioService.asignar_rol(
            db, 
            id_usuario, 
            id_rol, 
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Rol asignado exitosamente",
            data=resultado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar rol: {str(e)}"
        )

@router.delete("/{id_usuario}/roles/{id_rol}")
@requires_permission("asignar_permisos")
async def revocar_rol_usuario(
    id_usuario: int,
    id_rol: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Revocar rol de usuario (RF-02)
    ⚠️ SEGURIDAD: Requiere permiso 'asignar_permisos'
    """
    try:
        resultado = UsuarioService.revocar_rol(
            db,
            id_usuario,
            id_rol,
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Rol revocado exitosamente",
            data=resultado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al revocar rol: {str(e)}"
        )

@router.post("/roles/{id_rol}/permisos")
@requires_permission("asignar_permisos")
async def asignar_permisos_rol(
    id_rol: int,
    permisos_ids: list[int],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    Asignar permisos a rol (RF-04)
    ⚠️ SEGURIDAD: Requiere permiso 'asignar_permisos'
    """
    try:
        rol_actualizado = RolService.asignar_permisos_rol(
            db, 
            id_rol, 
            permisos_ids, 
            user_id=current_user.id_usuario
        )
        
        return ResponseModel.success(
            message="Permisos asignados al rol",
            data=rol_actualizado.dict() if hasattr(rol_actualizado, 'dict') else rol_actualizado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar permisos: {str(e)}"
        )
    

# ==================== ENDPOINTS DE PERMISOS ====================

@router.get("/permisos")
async def listar_permisos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    modulo: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los permisos disponibles"""
    try:
        permisos = PermisoService.listar_permisos(db, skip, limit, modulo)
        
        return ResponseModel.success(
            message="Permisos obtenidos",
            data=[p.dict() if hasattr(p, 'dict') else p for p in permisos],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar permisos: {str(e)}"
        )

@router.get("/permisos/{id_permiso}")
async def obtener_permiso(
    id_permiso: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de permiso específico"""
    try:
        permiso = PermisoService.obtener_permiso(db, id_permiso)
        
        return ResponseModel.success(
            message="Permiso obtenido",
            data=permiso.dict() if hasattr(permiso, 'dict') else permiso,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al obtener permiso: {str(e)}"
        )