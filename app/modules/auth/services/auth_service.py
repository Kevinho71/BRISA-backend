"""auth_service.py """

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
import logging
from app.shared.security import (
    pwd_context,
    hash_password,
    verify_password,
    create_access_token
)

import os

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db

from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona1, Rol, Permiso, LoginLog, Bitacora
)
from app.modules.auth.dto.auth_dto import RegistroDTO, LoginDTO, TokenDTO, UsuarioActualDTO
from app.shared.exceptions import Unauthorized, NotFound

from app.config.config import config

logger = logging.getLogger(__name__)

# Seleccionar configuración según el entorno
env = os.environ.get("ENV", "development")
Settings = config.get(env, config['default'])

# Variables necesarias para JWT
SECRET_KEY = getattr(Settings, "SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(Settings, "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)

# Contexto para hash de contraseñas

class AuthService:
    """Servicio de autenticación con JWT"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashear contraseña con bcrypt (usa módulo shared.security)"""
        return hash_password(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña contra hash"""
        return verify_password(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT"""
        return create_access_token(data, expires_delta)

    @staticmethod
    def decode_token(token: str) -> Dict:
        """Decodificar y validar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Buscar tanto 'usuario_id' como 'sub' para compatibilidad
            usuario_id: int = payload.get("usuario_id") or payload.get("sub")
            if usuario_id is None:
                raise Unauthorized("Token inválido")
            return payload
        except JWTError:
            raise Unauthorized("Token expirado o inválido")

    @staticmethod
    def registrar_usuario(db: Session, registro: RegistroDTO) -> dict:
        """Registrar nuevo usuario"""
        # Validar duplicados
        usuario_existente = db.query(Usuario).filter(
            (Usuario.usuario == registro.usuario) | (Usuario.correo == registro.correo)
        ).first()
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario o correo ya existe"
            )

        persona_existente = db.query(Persona1).filter(Persona1.ci == registro.ci).first()
        if persona_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CI ya registrado"
            )

        try:
            # Crear persona
            persona = Persona1(
                ci=registro.ci,
                nombres=registro.nombres,
                apellido_paterno=registro.apellido_paterno,
                apellido_materno=registro.apellido_materno,
                telefono=registro.telefono,
                direccion=registro.direccion,
                correo=registro.correo,
                tipo_persona=registro.tipo_persona
            )
            db.add(persona)
            db.flush()

            # Crear usuario
            usuario = Usuario(
                id_persona=persona.id_persona,
                usuario=registro.usuario,
                correo=registro.correo,
                password=AuthService.hash_password(registro.password),
                is_active=True
            )
            db.add(usuario)
            db.flush()

            # Asignar rol
            if registro.id_rol:
                rol = db.query(Rol).filter(Rol.id_rol == registro.id_rol).first()
                if not rol:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Rol no encontrado"
                    )
                usuario.roles.append(rol)
            else:
                # Asignar rol "Administrativo" por defecto
                rol_default = db.query(Rol).filter(Rol.nombre == "Administrativo").first()
                if rol_default:
                    usuario.roles.append(rol_default)

            db.commit()
            db.refresh(usuario)

            logger.info(f"Usuario registrado: {usuario.usuario}")

            return {
                "id_usuario": usuario.id_usuario,
                "usuario": usuario.usuario,
                "correo": usuario.correo,
                "nombres": f"{persona.nombres} {persona.apellido_paterno}",
                "mensaje": "Usuario registrado exitosamente"
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Error al registrar usuario: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al registrar usuario"
            )

    @staticmethod
    def login(db: Session, login_dto: LoginDTO) -> TokenDTO:
        """
        Autenticación de usuario
        
        SEGURIDAD: El mensaje de error debe ser genérico para no revelar
        si el usuario existe o no (prevenir enumeración de usuarios)
        """
        MENSAJE_ERROR_GENERICO = "Usuario o contraseña incorrectos"
        
        # Buscar usuario activo
        usuario = db.query(Usuario).filter(
            Usuario.usuario == login_dto.usuario
        ).first()
        
        # Usuario no encontrado -> mensaje genérico
        if not usuario:
            raise Unauthorized(MENSAJE_ERROR_GENERICO)
        
        # Contraseña incorrecta -> mismo mensaje genérico
        if not AuthService.verify_password(login_dto.password, usuario.password):
            raise Unauthorized(MENSAJE_ERROR_GENERICO)
        
        if usuario.is_active is False:
            raise Unauthorized("Cuenta desactivada")

        # Crear token con AMBOS campos para compatibilidad
        access_token = AuthService.create_access_token(
            data={
                "sub": usuario.id_usuario, 
                "usuario_id": usuario.id_usuario,  
                "usuario": usuario.usuario
            }
        )
        
        # Retornar TokenDTO completo
        return TokenDTO(
            access_token=access_token,
            token_type="bearer",
            usuario_id=usuario.id_usuario,
            usuario=usuario.usuario,
            nombres=f"{usuario.persona.nombres} {usuario.persona.apellido_paterno}",
            rol=usuario.roles[0].nombre if usuario.roles else "",
            permisos=[p.nombre for r in usuario.roles for p in r.permisos if r.is_active and p.is_active],
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )


    @staticmethod
    def get_current_user(db: Session, token: str) -> Usuario:
        """Obtener usuario actual desde token JWT"""
        try:
            payload = AuthService.decode_token(token)
            # Buscar tanto 'usuario_id' como 'sub'
            usuario_id: int = payload.get("usuario_id") or payload.get("sub")

            usuario = db.query(Usuario).filter(
                Usuario.id_usuario == usuario_id, 
                Usuario.is_active == True
            ).first()
            
            if not usuario:
                raise NotFound("Usuario", usuario_id)

            return usuario
        except Exception as e:
            logger.error(f"Error al obtener usuario del token: {str(e)}")
            raise Unauthorized("No autorizado")

    @staticmethod
    def obtener_usuario_actual(db: Session, usuario_id: int) -> UsuarioActualDTO:
        """Obtener datos del usuario autenticado"""
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        roles = []
        permisos = []

        for rol in usuario.roles:
            if rol.is_active:
                roles.append({"id_rol": rol.id_rol, "nombre": rol.nombre})
                for permiso in rol.permisos:
                    if permiso.is_active and permiso.nombre not in permisos:
                        permisos.append(permiso.nombre)

        estado = "activo" if usuario.is_active else "inactivo"

        return UsuarioActualDTO(
            id_usuario=usuario.id_usuario,
            id_persona=usuario.id_persona,
            usuario=usuario.usuario,
            correo=usuario.correo,
            nombres=usuario.persona.nombres,
            apellido_paterno=usuario.persona.apellido_paterno,
            apellido_materno=usuario.persona.apellido_materno,
            ci=usuario.persona.ci,
            roles=roles,
            permisos=permisos,
            estado=estado
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """ Dependency mejorado con manejo de errores"""
    from app.modules.auth.services.auth_service import AuthService
    try:
        return AuthService.get_current_user(db, token)
    except Unauthorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Error en get_current_user_dependency: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )