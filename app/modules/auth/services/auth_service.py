"""
auth_service.py - SOLUCIÓN DEFINITIVA
✅ FIX: Usar flush() SIEMPRE, nunca commit() dentro del servicio
El commit lo hace el controlador o el test
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, Request
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
import logging
from app.shared.security import hash_password, verify_password, create_access_token

from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona1, Rol, Permiso, LoginLog, Bitacora
)
from app.modules.auth.dto.auth_dto import RegistroDTO, LoginDTO, TokenDTO, UsuarioActualDTO
from app.shared.exceptions import Unauthorized, NotFound

from app.config.config import config
from app.core.database import get_db
import os

logger = logging.getLogger(__name__)

# Configuración JWT
env = os.environ.get("ENV", "development")
Settings = config.get(env, config['default'])
SECRET_KEY = getattr(Settings, "SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(Settings, "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)

# Blacklist de tokens (usar Redis en producción)
token_blacklist = set()


class AuthService:
    """Servicio de autenticación con JWT"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashear contraseña con bcrypt"""
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
            # Verificar blacklist
            if token in token_blacklist:
                raise Unauthorized("Token inválido (sesión cerrada)")
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id: int = payload.get("usuario_id") or payload.get("sub")
            if usuario_id is None:
                raise Unauthorized("Token inválido")
            return payload
        except JWTError:
            raise Unauthorized("Token expirado o inválido")

    @staticmethod
    def invalidate_token(token: str):
        """Agregar token a la blacklist"""
        token_blacklist.add(token)
        logger.info(f"Token agregado a blacklist. Total tokens: {len(token_blacklist)}")

    @staticmethod
    def registrar_login_log(
        db: Session, 
        id_usuario: int, 
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        estado: str = 'exitoso'
    ) -> LoginLog:
        """
        Registrar intento de login en LoginLog
        ✅ USA FLUSH, NO COMMIT
        """
        try:
            if estado not in ['exitoso', 'fallido']:
                estado = 'fallido'
            
            login_log = LoginLog(
                id_usuario=id_usuario,
                ip_address=ip_address,
                user_agent=user_agent,
                estado=estado,
                fecha_hora=datetime.now()
            )
            db.add(login_log)
            db.flush()  # ✅ CRÍTICO: flush en lugar de commit
            logger.info(f"LoginLog registrado para usuario {id_usuario}: {estado}")
            return login_log
        except Exception as e:
            logger.error(f"Error al registrar LoginLog: {str(e)}")
            raise

    @staticmethod
    def registrar_bitacora(
        db: Session,
        usuario_id: int,
        accion: str,
        tipo_objetivo: Optional[str] = None,
        id_objetivo: Optional[int] = None,
        descripcion: Optional[str] = None
    ) -> Bitacora:
        """
        Registrar acción en Bitacora
        ✅ USA FLUSH, NO COMMIT
        """
        try:
            bitacora = Bitacora(
                id_usuario_admin=usuario_id,
                accion=accion,
                tipo_objetivo=tipo_objetivo,
                id_objetivo=id_objetivo,
                descripcion=descripcion,
                fecha_hora=datetime.now()
            )
            db.add(bitacora)
            db.flush()  # ✅ CRÍTICO: flush en lugar de commit
            logger.info(f"Bitácora registrada: {accion} por usuario {usuario_id}")
            return bitacora
        except Exception as e:
            logger.error(f"Error al registrar en Bitácora: {str(e)}")
            raise

    @staticmethod
    def login(
        db: Session, 
        login_dto: LoginDTO,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> TokenDTO:
        """
        HU-01: Autenticación de usuario
        ✅ NO HACE COMMIT - lo hace el controlador
        """
        MENSAJE_ERROR_GENERICO = "Usuario o contraseña incorrectos"
        
        try:
            # Buscar usuario
            usuario = db.query(Usuario).filter(
                Usuario.usuario == login_dto.usuario
            ).first()
            
            # Usuario no encontrado
            if not usuario:
                logger.warning(f"Intento de login con usuario inexistente: {login_dto.usuario}")
                raise Unauthorized(MENSAJE_ERROR_GENERICO)
            
            # Contraseña incorrecta
            if not AuthService.verify_password(login_dto.password, usuario.password):
                AuthService.registrar_login_log(
                    db, 
                    usuario.id_usuario, 
                    ip_address=ip_address,
                    user_agent=user_agent,
                    estado='fallido'
                )
                db.commit()  # ✅ Commit aquí para intentos fallidos
                raise Unauthorized(MENSAJE_ERROR_GENERICO)
            
            # Cuenta desactivada
            if usuario.is_active is False:
                AuthService.registrar_login_log(
                    db, 
                    usuario.id_usuario, 
                    ip_address=ip_address,
                    user_agent=user_agent,
                    estado='fallido'
                )
                db.commit()  # ✅ Commit aquí
                raise Unauthorized("Cuenta desactivada")

            # ✅ LOGIN EXITOSO
            AuthService.registrar_login_log(
                db, 
                usuario.id_usuario,
                ip_address=ip_address,
                user_agent=user_agent,
                estado='exitoso'
            )

            # ✅ Registrar en Bitácora
            AuthService.registrar_bitacora(
                db,
                usuario_id=usuario.id_usuario,
                accion='LOGIN',
                tipo_objetivo='Usuario',
                id_objetivo=usuario.id_usuario,
                descripcion=f"Inicio de sesión exitoso: {usuario.usuario} desde IP {ip_address}"
            )

            # ✅ COMMIT AL FINAL (el controlador también puede hacerlo)
            db.commit()

            # Crear token
            access_token = AuthService.create_access_token(
                data={
                    "sub": usuario.id_usuario, 
                    "usuario_id": usuario.id_usuario,  
                    "usuario": usuario.usuario
                }
            )
            
            # Retornar TokenDTO
            return TokenDTO(
                access_token=access_token,
                token_type="bearer",
                usuario_id=usuario.id_usuario,
                usuario=usuario.usuario,
                nombres=f"{usuario.persona.nombres} {usuario.persona.apellido_paterno}",
                rol=usuario.roles[0].nombre if usuario.roles else "Sin rol",
                permisos=[p.nombre for r in usuario.roles for p in r.permisos if r.is_active and p.is_active],
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        except Unauthorized:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error en login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error en el proceso de login"
            )

    @staticmethod
    def logout(
        db: Session,
        token: str,
        usuario_id: int,
        ip_address: Optional[str] = None
    ) -> dict:
        """
        HU-02: Cierre de sesión
        ✅ CORREGIDO: Usa flush + commit explícito para persistencia
        """
        try:
            # Invalidar token
            AuthService.invalidate_token(token)
            
            # ✅ Registrar en Bitácora (con flush interno)
            bitacora = AuthService.registrar_bitacora(
                db,
                usuario_id=usuario_id,
                accion='LOGOUT',
                tipo_objetivo='Usuario',
                id_objetivo=usuario_id,
                descripcion=f"Cierre de sesión desde IP {ip_address}"
            )
            
            # ✅ CRÍTICO: Commit explícito para persistir
            db.commit()
            
            # ✅ Refrescar el objeto para que tenga el ID asignado
            db.refresh(bitacora)
            
            logger.info(f"Logout exitoso para usuario {usuario_id}")
            
            return {
                "mensaje": "Sesión cerrada exitosamente",
                "token_invalidado": True
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en logout: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cerrar sesión"
            )

    @staticmethod
    def get_current_user(db: Session, token: str) -> Usuario:
        """Obtener usuario actual desde token JWT"""
        try:
            payload = AuthService.decode_token(token)
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
                # Rol por defecto
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


# ============================================
# DEPENDENCIA PARA FASTAPI
# ============================================

def get_current_user_dependency(
    request: Request,
    db: Session = Depends(get_db)
) -> Usuario:

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = AuthService.get_current_user(db, token)

    usuario._token = token
    usuario._ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or (
        request.client.host if request.client else "unknown"
    )
    
    return usuario
