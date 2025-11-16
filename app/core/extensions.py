# app/core/extensions.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.modules.auth.dto.auth_dto import RegistroDTO, LoginDTO, TokenDTO, UsuarioActualDTO
from app.modules.auth.services.auth_service import AuthService
from app.shared.security import verify_token

# Router principal
router = APIRouter()


@router.post("/register", response_model=dict)
async def registrar(
    registro: RegistroDTO,
    db: Session = Depends(get_db)
) -> dict:
    """
    Registrar nuevo usuario (RF-01)
    """
    try:
        resultado = AuthService.registrar_usuario(db, registro)
        return ResponseModel.success(
            message="Usuario registrado exitosamente",
            data=resultado,
            status_code=status.HTTP_201_CREATED
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al registrar usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/login", response_model=dict)
async def login(
    login: LoginDTO,
    request: Request,
    db: Session = Depends(get_db)
) -> dict:
    """
    Iniciar sesión y obtener token JWT (RF-05)
    """
    try:
        ip_address = request.client.host if request.client else None
        token_data = AuthService.login(db, login, ip_address)
        return ResponseModel.success(
            message="Inicio de sesión exitoso",
            data=token_data.dict(),
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error en inicio de sesión",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/me", response_model=dict)
async def obtener_usuario_actual(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Obtener datos del usuario autenticado
    """
    try:
        usuario_id = token_data.get("usuario_id")
        usuario_actual = AuthService.obtener_usuario_actual(db, usuario_id)
        return ResponseModel.success(
            message="Datos del usuario obtenidos",
            data=usuario_actual.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener datos del usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/validate-token", response_model=dict)
async def validar_token(
    token_data: dict = Depends(verify_token)
) -> dict:
    """
    Validar que un token JWT es válido
    """
    return ResponseModel.success(
        message="Token válido",
        data={"usuario_id": token_data.get("usuario_id")},
        status_code=status.HTTP_200_OK
    )


def init_extensions(app):
    """
    Inicializar extensiones y routers de FastAPI.
    - Agregar middlewares, CORS, routers adicionales aquí.
    """
    app.include_router(router)
