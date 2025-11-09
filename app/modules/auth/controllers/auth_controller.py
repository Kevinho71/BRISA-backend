"""
auth_controller.py - CORREGIDO CON CURRENT_USER Y DECORADORES
Controlador de autenticación y usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.usuarios.models.usuario_models import Persona1, Usuario
from app.modules.auth.dto.auth_dto import LoginDTO, RegistroDTO
from app.modules.auth.services.auth_service import AuthService, get_current_user_dependency

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.shared.security import verify_token
from app.shared.decorators.auth_decorators import require_permissions
from app.modules.usuarios.dto.usuario_dto import (
    UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO,
    RolCreateDTO, RolUpdateDTO, RolResponseDTO,
    PermisoResponseDTO, AsignarRolDTO
)
from app.modules.usuarios.services.usuario_service import (
    UsuarioService, RolService, PermisoService
)
from app.shared.response import StandardResponse


router = APIRouter()

# ==================== AUTENTICACIÓN ====================

@router.post("/login")
async def login(
    login_data: LoginDTO,
    db: Session = Depends(get_db)
):
    """
    Login de usuario
    
    ⚠️ SEGURIDAD: 
    - Los mensajes de error deben ser genéricos
    - No revelar si el usuario existe o no
    """
    try:
        # AuthService.login ya devuelve TokenDTO
        token_dto = AuthService.login(db, login_data)
        
        # Obtener información adicional del usuario
        usuario = db.query(Usuario).filter(
            Usuario.usuario == login_data.usuario
        ).first()
        
        # Obtener roles y permisos
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
        
        # ⚠️ IMPORTANTE: Estructura específica para que pasen los tests
        # Los tests esperan: response.json()["data"]["access_token"]
        return {
            "success": True,
            "message": "Login exitoso",
            "data": {
                "access_token": token_dto.access_token,
                "token_type": token_dto.token_type,
                "usuario_id": token_dto.usuario_id,
                "usuario": login_data.usuario,
                "nombres": f"{usuario.persona.nombres} {usuario.persona.apellido_paterno}" if usuario and usuario.persona else "",
                "rol": rol_principal,
                "permisos": permisos,
                "expires_in": 1800  # 30 minutos
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Mensaje genérico para cualquier error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    

# CRÍTICO: /me DEBE ESTAR ANTES DE /{id_usuario}
@router.get("/me")
async def obtener_usuario_actual(
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Obtener información del usuario autenticado
    """
    try:
        usuario_dto = AuthService.obtener_usuario_actual(db, current_user.id_usuario)
        return {
            "success": True,
            "message": "Usuario obtenido exitosamente",
            "data": usuario_dto.dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    registro: RegistroDTO,
    db: Session = Depends(get_db)
):
    """
    Registrar nuevo usuario (RF-01)
    Crea persona + usuario + asigna rol
    """
    try:
        resultado = AuthService.registrar_usuario(db, registro)
        return {
            "success": True,
            "message": "Usuario registrado exitosamente",
            "data": resultado
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/logout")
async def logout(
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Logout de usuario
    
    Nota: Con JWT stateless, el logout es del lado del cliente.
    El cliente debe eliminar el token.
    """
    return {
        "success": True,
        "message": "Logout exitoso",
        "data": {"mensaje": "Token debe ser eliminado del cliente"}
    }



@router.post("/refresh")
async def refresh_token(
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Refrescar token JWT
    Genera un nuevo token para el usuario autenticado
    """
    try:
        # Generar nuevo token
        nuevo_token = AuthService.create_access_token(
            data={"sub": current_user.id_usuario}
        )
        
        return {
            "success": True,
            "message": "Token refrescado exitosamente",
            "data": {
                "access_token": nuevo_token,
                "token_type": "bearer",
                "expires_in": 1800
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al refrescar token"
        )
    
# ==================== USUARIOS ====================

@router.get("/usuarios", response_model=dict)
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
            data=[u.dict() for u in usuarios],
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al listar usuarios",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/usuarios/{id_usuario}", response_model=dict)
async def obtener_usuario(
    id_usuario: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener detalles de usuario específico"""
    usuario = UsuarioService.obtener_usuario(db, id_usuario)
    
    return ResponseModel.success(
        message="Usuario obtenido",
        data=usuario.dict(),
        status_code=status.HTTP_200_OK
    )

@router.put("/usuarios/{id_usuario}", response_model=dict)
async def actualizar_usuario(
    id_usuario: int,
    usuario_update: UsuarioUpdateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Actualizar usuario (RF-06)"""
    try:
        usuario_actualizado = UsuarioService.actualizar_usuario(
            db, 
            id_usuario, 
            usuario_update, 
            current_user=current_user
        )
        
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

@router.delete("/usuarios/{id_usuario}", response_model=dict)
async def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Eliminar usuario (borrado lógico) (RF-06)"""
    try:
        resultado = UsuarioService.eliminar_usuario(
            db, 
            id_usuario, 
            current_user=current_user
        )
        
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

# ==================== ROLES ====================

@router.post("/roles", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_rol(
    rol_create: RolCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Crear nuevo rol (RF-03)"""
    try:
        nuevo_rol = RolService.crear_rol(
            db, 
            rol_create, 
            current_user=current_user
        )
        
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
    current_user: Usuario = Depends(get_current_user_dependency),
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
    current_user: Usuario = Depends(get_current_user_dependency),
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

@router.post("/usuarios/{id_usuario}/roles/{id_rol}", response_model=dict)
async def asignar_rol_usuario(
    id_usuario: int,
    id_rol: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Asignar rol a usuario (RF-02)"""
    try:
        resultado = RolService.asignar_rol_usuario(
            db, 
            id_usuario, 
            id_rol, 
            current_user=current_user
        )
        
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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """Asignar permisos a rol (RF-04)"""
    try:
        rol_actualizado = RolService.asignar_permisos_rol(
            db, 
            id_rol, 
            permisos_ids, 
            current_user=current_user
        )
        
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

# ==================== PERMISOS ====================

@router.get("/permisos", response_model=dict)
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
    current_user: Usuario = Depends(get_current_user_dependency),
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