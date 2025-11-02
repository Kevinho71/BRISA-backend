from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
import logging
from passlib.context import CryptContext

from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona, Rol, Permiso, LoginLog
)
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.modules.auth.dto.auth_dto import RegistroDTO, LoginDTO, TokenDTO, UsuarioActualDTO
from app.modules.usuarios.dto.usuario_dto import LoginDTO as UsuarioLoginDTO, TokenResponseDTO, UsuarioResponseDTO
from app.shared.exceptions import Unauthorized, NotFound

logger = logging.getLogger(__name__)

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Servicio de autenticación con JWT"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashear contraseña con bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña contra hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Dict:
        """Decodificar y validar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id: int = payload.get("sub")
            if usuario_id is None:
                raise Unauthorized("Token inválido")
            return payload
        except JWTError:
            raise Unauthorized("Token expirado o inválido")
    
    @staticmethod
    def registrar_usuario(db: Session, registro: RegistroDTO) -> dict:
        """
        Registrar nuevo usuario (RF-01)
        - Validar duplicados
        - Encriptar contraseña
        - Crear persona y usuario
        - Asignar rol predefinido
        """
        # Validar duplicados
        usuario_existente = db.query(Usuario).filter(
            (Usuario.usuario == registro.usuario) | (Usuario.correo == registro.correo)
        ).first()
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario o correo ya existe"
            )
        
        persona_existente = db.query(Persona).filter(Persona.ci == registro.ci).first()
        if persona_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CI ya registrado"
            )
        
        try:
            # Crear persona
            persona = Persona(
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
                password_hash=AuthService.hash_password(registro.password),
                estado='activo'
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
    def login(db: Session, login_dto: LoginDTO, ip_address: str = None) -> TokenDTO:
        """
        Autenticar usuario y generar token JWT
        RF-05: Autenticación con contraseña encriptada
        """
        usuario = db.query(Usuario).filter(Usuario.correo == login_dto.correo).first()
        
        if not usuario or not AuthService.verify_password(login_dto.password, usuario.password_hash):
            # Registrar intento fallido
            if usuario:
                login_log = LoginLog(
                    id_usuario=usuario.id,
                    ip_address=ip_address,
                    estado='fallido'
                )
                db.add(login_log)
                db.commit()
                logger.warning(f"Intento de login fallido: {usuario.correo}")
            
            raise Unauthorized("Correo o contraseña incorrectos")
        
        if not usuario.is_active:
            raise Unauthorized("Usuario inactivo")
        
        # Crear token
        access_token = AuthService.create_access_token(
            data={"sub": usuario.id, "correo": usuario.correo},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Registrar login exitoso
        usuario.ultimo_acceso = datetime.utcnow()
        login_log = LoginLog(
            id_usuario=usuario.id,
            ip_address=ip_address,
            estado='exitoso'
        )
        db.add(login_log)
        db.commit()
        
        logger.info(f"Login exitoso: {usuario.correo}")
        
        # Obtener roles y permisos
        roles = usuario.roles
        permisos = []
        for rol in roles:
            if rol.is_active:
                for permiso in rol.permisos:
                    if permiso.is_active and permiso.nombre not in permisos:
                        permisos.append(permiso.nombre)
        
        usuario_response = UsuarioResponseDTO(
            id=usuario.id,
            id_persona=usuario.id_persona,
            correo=usuario.correo,
            ultimo_acceso=usuario.ultimo_acceso,
            is_active=usuario.is_active,
            created_at=usuario.created_at,
            updated_at=usuario.updated_at,
            roles=[{"id": r.id, "nombre": r.nombre} for r in roles if r.is_active]
        )
        
        return TokenDTO(
            access_token=access_token,
            token_type="bearer",
            usuario=usuario_response
        )
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> Usuario:
        """Obtener usuario actual desde token JWT"""
        try:
            payload = AuthService.decode_token(token)
            usuario_id: int = payload.get("sub")
            
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
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
        
        # Obtener roles y permisos
        roles = []
        permisos = []
        
        for rol in usuario.roles:
            if rol.is_active:
                roles.append({"id_rol": rol.id_rol, "nombre": rol.nombre})
                for permiso in rol.permisos:
                    if permiso.is_active and permiso.nombre not in permisos:
                        permisos.append(permiso.nombre)
        
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
            estado=usuario.estado
        )
