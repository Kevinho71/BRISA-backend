"""
auth_controller.py -Usando ResponseModel
Controlador de autenticación y usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.modules.usuarios.models.usuario_models import Persona1, Usuario
from app.modules.auth.dto.auth_dto import LoginDTO, RegistroDTO
from app.modules.auth.services.auth_service import AuthService, get_current_user_dependency

from app.core.database import get_db
from app.shared.response import ResponseModel 
from app.shared.security import verify_token
from app.shared.permissions import requires_permission
from app.modules.usuarios.dto.usuario_dto import (
    UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO,
    RolCreateDTO, RolUpdateDTO, RolResponseDTO,
    PermisoResponseDTO, AsignarRolDTO
)
from app.modules.usuarios.services.usuario_service import (
    UsuarioService, RolService, PermisoService
)

logger = logging.getLogger(__name__)
router = APIRouter()


# ==================== AUTENTICACIÓN ====================

@router.post("/login", response_model=dict)
async def login(
    login_data: LoginDTO,
    db: Session = Depends(get_db)
):
    """Login de usuario"""
    try:
        token_dto = AuthService.login(db, login_data)
        usuario = db.query(Usuario).filter(Usuario.usuario == login_data.usuario).first()
        
        roles = []
        permisos = []
        rol_principal = "Usuario"
        if usuario and usuario.roles:
            for rol in usuario.roles:
                if rol.is_active:
                    roles.append(rol.nombre)
                    for permiso in rol.permisos:
                        if permiso.is_active and permiso.nombre not in permisos:
                            permisos.append(permiso.nombre)
            rol_principal = roles[0] if roles else "Usuario"
        
        return ResponseModel.success(
            message="Login exitoso",
            data={
                "access_token": token_dto.access_token,
                "token_type": token_dto.token_type,
                "usuario_id": token_dto.usuario_id,
                "usuario": login_data.usuario,
                "nombres": f"{usuario.persona.nombres} {usuario.persona.apellido_paterno}" if usuario and usuario.persona else "",
                "rol": rol_principal,
                "permisos": permisos,
                "expires_in": 1800
            }
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )


# CRÍTICO: /me DEBE ESTAR ANTES DE /{id_usuario}
@router.get("/me", response_model=dict)
async def obtener_usuario_actual(
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Obtener información del usuario autenticado"""
    try:
        usuario_dto = AuthService.obtener_usuario_actual(db, current_user.id_usuario)
        return ResponseModel.success(
            message="Usuario obtenido exitosamente",
            data=usuario_dto.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/registro", response_model=dict, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    registro_dto: RegistroDTO,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Registrar nuevo usuario (RF-01)"""
    try:
        resultado = AuthService.registrar_usuario(db, registro_dto)
        return ResponseModel.success(
            message="Usuario registrado exitosamente",
            data=resultado,
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException:
        raise
    except Exception as e:
        return ResponseModel.error(
            message="Error al registrar usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/logout", response_model=dict)
async def logout(
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """Logout de usuario"""
    return ResponseModel.success(
        message="Logout exitoso",
        data={"mensaje": "Token debe ser eliminado del cliente"}
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
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
@requires_permission('ver_usuario')  # Decorador para validar permiso
async def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los usuarios"""
    try:
        usuarios = UsuarioService.listar_usuarios(db, skip, limit)
        return ResponseModel.success(
            message="Usuarios obtenidos",
            data=[u.dict() for u in usuarios]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/usuarios/{id_usuario}", response_model=dict)
@requires_permission('ver_usuario')  # Decorador
async def obtener_usuario(
    id_usuario: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
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
@requires_permission('editar_usuario')  # Decorador
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
@requires_permission('eliminar_usuario')  # Decorador
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
@requires_permission('crear_rol')  # Decorador
async def crear_rol(
    rol_create: RolCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Crear nuevo rol"""
    from app.shared.exceptions.custom_exceptions import Conflict, DatabaseException
    
    try:
        nuevo_rol = RolService.crear_rol(db, rol_create, current_user=current_user)
        return ResponseModel.success(
            message="Rol creado exitosamente",
            data=nuevo_rol.dict()
        )
    except Conflict as e:
        # Manejar conflicto de nombre duplicado
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
@requires_permission('ver_rol')  # Decorador
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
            data=[r.dict() for r in roles]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/roles/{id_rol}", response_model=dict)
@requires_permission('ver_rol')  # Decorador
async def obtener_rol(
    id_rol: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de rol específico"""
    rol = RolService.obtener_rol(db, id_rol)
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return ResponseModel.success(
        message="Rol obtenido",
        data=rol.dict()
    )


@router.post("/usuarios/{id_usuario}/roles/{id_rol}", response_model=dict)
@requires_permission('asignar_permisos')  # Decorador
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
@requires_permission('asignar_permisos')  # Decorador
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
        data=rol_actualizado.dict()
    )


# ==================== PERMISOS ====================

@router.get("/permisos", response_model=dict)
@requires_permission('ver_rol')  # Decorador
async def listar_permisos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    modulo: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los permisos"""
    permisos = PermisoService.listar_permisos(db, skip, limit, modulo)
    return ResponseModel.success(
        message="Permisos obtenidos",
        data=[p.dict() for p in permisos]
    )


@router.get("/permisos/{id_permiso}", response_model=dict)
@requires_permission('ver_rol')  # Decorador
async def obtener_permiso(
    id_permiso: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de permiso específico"""
    permiso = PermisoService.obtener_permiso(db, id_permiso)
    if not permiso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permiso no encontrado")
    return ResponseModel.success(
        message="Permiso obtenido",
        data=permiso.dict()
    )

# ==================== LOGS DE ACCESO ====================

@router.get("/logs-acceso", response_model=dict)
@requires_permission('ver_rol')
async def listar_logs_acceso(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
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