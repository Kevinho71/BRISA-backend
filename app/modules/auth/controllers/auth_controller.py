from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.usuarios.models.usuario_models import Persona1
from app.modules.auth.dto.auth_dto import LoginDTO
from app.modules.auth.services.auth_service import AuthService

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.shared.security import verify_token
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

@router.post("", response_model=dict)
async def crear_usuario(
    usuario_create: UsuarioCreateDTO,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Crear nuevo usuario (RF-01)
    
    Requiere permisos: crear_usuario
    """
    try:
        usuario_id = token_data.get("usuario_id")
        nuevo_usuario = UsuarioService.crear_usuario(db, usuario_create, usuario_id)
        
        return ResponseModel.success(
            message="Usuario creado exitosamente",
            data=nuevo_usuario.dict(),
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al crear usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{id_usuario}", response_model=dict)
async def obtener_usuario(
    id_usuario: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de usuario específico"""
    try:
        usuario = UsuarioService.obtener_usuario(db, id_usuario)
        
        return ResponseModel.success(
            message="Usuario obtenido",
            data=usuario.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("", response_model=dict)
async def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los usuarios"""
    try:
        usuarios = UsuarioService.listar_usuarios(db, skip, limit)
        return ResponseModel.success(
            message="Usuarios obtenidos",
            data=[u.dict() for u in usuarios],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al listar usuarios",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.put("/{id_usuario}", response_model=dict)
async def actualizar_usuario(
    id_usuario: int,
    usuario_update: UsuarioUpdateDTO,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Actualizar usuario (RF-06)
    
    Audita todos los cambios realizados
    """
    try:
        usuario_id = token_data.get("usuario_id")
        usuario_actualizado = UsuarioService.actualizar_usuario(db, id_usuario, usuario_update, usuario_id)
        
        return ResponseModel.success(
            message="Usuario actualizado exitosamente",
            data=usuario_actualizado.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al actualizar usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete("/{id_usuario}", response_model=dict)
async def eliminar_usuario(
    id_usuario: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Eliminar usuario (borrado lógico) (RF-06)
    
    Marca el usuario como inactivo
    """
    try:
        usuario_admin_id = token_data.get("usuario_id")
        resultado = UsuarioService.eliminar_usuario(db, id_usuario, usuario_admin_id)
        
        return ResponseModel.success(
            message="Usuario eliminado exitosamente",
            data=resultado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al eliminar usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ==================== ENDPOINTS DE ROLES ====================

@router.post("/roles", response_model=dict)
async def crear_rol(
    rol_create: RolCreateDTO,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Crear nuevo rol (RF-03)
    
    Requiere permisos: crear_rol
    """
    try:
        usuario_id = token_data.get("usuario_id")
        nuevo_rol = RolService.crear_rol(db, rol_create, usuario_id)
        
        return ResponseModel.success(
            message="Rol creado exitosamente",
            data=nuevo_rol.dict(),
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al crear rol",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/roles", response_model=dict)
async def listar_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los roles"""
    try:
        roles = RolService.listar_roles(db, skip, limit)
        
        return ResponseModel.success(
            message="Roles obtenidos",
            data=[r.dict() for r in roles],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al listar roles",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/roles/{id_rol}", response_model=dict)
async def obtener_rol(
    id_rol: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de rol específico"""
    try:
        rol = RolService.obtener_rol(db, id_rol)
        
        return ResponseModel.success(
            message="Rol obtenido",
            data=rol.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener rol",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/{id_usuario}/roles/{id_rol}", response_model=dict)
async def asignar_rol_usuario(
    id_usuario: int,
    id_rol: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Asignar rol a usuario (RF-02)
    
    Requiere permisos: asignar_permisos
    """
    try:
        usuario_id = token_data.get("usuario_id")
        resultado = RolService.asignar_rol_usuario(db, id_usuario, id_rol, usuario_id)
        
        return ResponseModel.success(
            message="Rol asignado exitosamente",
            data=resultado,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al asignar rol",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/roles/{id_rol}/permisos", response_model=dict)
async def asignar_permisos_rol(
    id_rol: int,
    permisos_ids: list[int],
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Asignar permisos a rol (RF-04)
    
    Requiere permisos: asignar_permisos
    """
    try:
        usuario_id = token_data.get("usuario_id")
        rol_actualizado = RolService.asignar_permisos_rol(db, id_rol, permisos_ids, usuario_id)
        
        return ResponseModel.success(
            message="Permisos asignados al rol",
            data=rol_actualizado.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al asignar permisos",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ==================== ENDPOINTS DE PERMISOS ====================

@router.get("/permisos", response_model=dict)
async def listar_permisos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    modulo: Optional[str] = None,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Listar todos los permisos disponibles"""
    try:
        permisos = PermisoService.listar_permisos(db, skip, limit, modulo)
        
        return ResponseModel.success(
            message="Permisos obtenidos",
            data=[p.dict() for p in permisos],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al listar permisos",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/permisos/{id_permiso}", response_model=dict)
async def obtener_permiso(
    id_permiso: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de permiso específico"""
    try:
        permiso = PermisoService.obtener_permiso(db, id_permiso)
        
        return ResponseModel.success(
            message="Permiso obtenido",
            data=permiso.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener permiso",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/me", response_model=dict)
async def obtener_usuario_actual(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Obtener información del usuario autenticado
    """
    try:
        usuario_id = token_data.get("usuario_id")
        from app.modules.auth.services.auth_service import AuthService
        usuario = AuthService.obtener_usuario_actual(db, usuario_id)
        
        return ResponseModel.success(
            message="Usuario autenticado obtenido",
            data=usuario.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener usuario autenticado",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/login", response_model=dict)
async def login(login_dto: LoginDTO, db: Session = Depends(get_db)):
    """
    Autenticación de usuario y generación de token
    """
    try:
        # Pasar la sesión de DB y el DTO completo a AuthService
        token_dto = AuthService.login(db=db, login_dto=login_dto)

        return ResponseModel.success(
            message="Login exitoso",
            data={"access_token": token_dto.access_token},
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al iniciar sesión",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )