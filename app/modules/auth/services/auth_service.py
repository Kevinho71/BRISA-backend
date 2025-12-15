"""
auth_service.py - SOLUCIÓN DEFINITIVA

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

from app.modules.auth.repositories.auth_repository import AuthRepository, MAX_INTENTOS_FALLIDOS, TIEMPO_BLOQUEO_MINUTOS

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
        USA FLUSH, NO COMMIT
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
            db.flush() 
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
            db.flush() 
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
        HU-01: Autenticación de usuario con bloqueo por intentos fallidos
        
        Flujo según CU-04:
        1. Buscar usuario
        2. Verificar si está bloqueado (≥3 intentos fallidos en últimos 10 min)
        3. Validar contraseña
        4. Validar estado activo
        5. Registrar login exitoso
        6. Limpiar intentos fallidos anteriores
        7. Registrar en bitácora
        8. Generar y retornar token
        
        ⚠️ Si falla: Incrementa contador de intentos fallidos
        ⚠️ Si intentos ≥ 3: Bloquea cuenta por 10 minutos
        """
        MENSAJE_ERROR_GENERICO = "Usuario o contraseña incorrectos"
        
        try:
           
            # 1 BUSCAR USUARIO
            
            usuario = AuthRepository.buscar_usuario_por_nombre(db, login_dto.usuario)
            
            # Usuario no encontrado
            if not usuario:
                logger.warning(f"❌ Intento de login con usuario inexistente: {login_dto.usuario}")
                raise Unauthorized(MENSAJE_ERROR_GENERICO)
            
        
            # 2️ VERIFICAR SI CUENTA ESTÁ BLOQUEADA
   
            bloqueada, fecha_desbloqueo = AuthRepository.verificar_cuenta_bloqueada(
                db, 
                usuario.id_usuario,
                max_intentos=MAX_INTENTOS_FALLIDOS,
                minutos_bloqueo=TIEMPO_BLOQUEO_MINUTOS
            )
            
            if bloqueada:
                # Registrar intento de login en cuenta bloqueada
                AuthRepository.registrar_login_log(
                    db, 
                    usuario.id_usuario, 
                    ip_address=ip_address,
                    user_agent=user_agent,
                    estado='fallido'
                )
                db.commit()
                
                tiempo_restante = (fecha_desbloqueo - datetime.now()).total_seconds() / 60
                logger.warning(
                    f"⚠️ Intento de login en cuenta bloqueada: {usuario.usuario} "
                    f"(desbloqueará en {tiempo_restante:.1f} minutos)"
                )
                
                raise Unauthorized(
                    f"Cuenta bloqueada por múltiples intentos fallidos. "
                    f"Intente nuevamente a las {fecha_desbloqueo.strftime('%H:%M:%S')}"
                )
            
            # 3️ VERIFICAR CONTRASEÑA

            if not verify_password(login_dto.password, usuario.password):
                # ❌ Contraseña incorrecta → Registrar intento fallido
                AuthRepository.registrar_login_log(
                    db, 
                    usuario.id_usuario, 
                    ip_address=ip_address,
                    user_agent=user_agent,
                    estado='fallido'
                )
                db.commit()
                
                # Contar intentos fallidos
                intentos_fallidos = AuthRepository.contar_intentos_fallidos(
                    db, 
                    usuario.id_usuario,
                    minutos=TIEMPO_BLOQUEO_MINUTOS
                )
                
                logger.warning(
                    f"❌ Contraseña incorrecta para usuario '{usuario.usuario}' "
                    f"(intento {intentos_fallidos}/{MAX_INTENTOS_FALLIDOS})"
                )
                
                # ⚠️ Advertir si está cerca del bloqueo
                if intentos_fallidos >= MAX_INTENTOS_FALLIDOS:
                    raise Unauthorized(
                        f"Demasiados intentos fallidos. Cuenta bloqueada por {TIEMPO_BLOQUEO_MINUTOS} minutos"
                    )
                elif intentos_fallidos == MAX_INTENTOS_FALLIDOS - 1:
                    raise Unauthorized(
                        f"{MENSAJE_ERROR_GENERICO}. "
                        f"⚠️ Un intento más y su cuenta será bloqueada por {TIEMPO_BLOQUEO_MINUTOS} minutos"
                    )
                else:
                    raise Unauthorized(MENSAJE_ERROR_GENERICO)
            

            # 4️ VERIFICAR ESTADO ACTIVO

            if usuario.is_active is False:
                AuthRepository.registrar_login_log(
                    db, 
                    usuario.id_usuario, 
                    ip_address=ip_address,
                    user_agent=user_agent,
                    estado='fallido'
                )
                db.commit()
                
                logger.warning(f"❌ Intento de login con cuenta desactivada: {usuario.usuario}")
                raise Unauthorized(
                    "Cuenta desactivada. Contacte al administrador"
                )
            

            # 5️ LOGIN EXITOSO - Registrar en LoginLog

            AuthRepository.registrar_login_log(
                db, 
                usuario.id_usuario,
                ip_address=ip_address,
                user_agent=user_agent,
                estado='exitoso'
            )
            

            # 6️ LIMPIAR INTENTOS FALLIDOS ANTERIORES

            # (Los intentos antiguos se ignoran automáticamente por la ventana de tiempo)
            AuthRepository.limpiar_intentos_fallidos(db, usuario.id_usuario)
            
            # 7️ REGISTRAR EN BITÁCORA

            AuthRepository.registrar_bitacora(
                db,
                usuario_id=usuario.id_usuario,
                accion='LOGIN',
                tipo_objetivo='Usuario',
                id_objetivo=usuario.id_usuario,
                descripcion=f"Inicio de sesión exitoso: {usuario.usuario} desde IP {ip_address}"
            )
            
            # ✅ COMMIT FINAL
            db.commit()
            

            # 8️ GENERAR TOKEN JWT

            from app.shared.security import create_access_token
            
            access_token = create_access_token(
                data={
                    "sub": usuario.id_usuario, 
                    "usuario_id": usuario.id_usuario,  
                    "usuario": usuario.usuario
                }
            )
            
            logger.info(f"✅ Login exitoso: {usuario.usuario} desde IP {ip_address}")
            
 
            # 9️ RETORNAR TOKEN DTO

            return TokenDTO(
                access_token=access_token,
                token_type="bearer",
                usuario_id=usuario.id_usuario,
                usuario=usuario.usuario,
                nombres=f"{usuario.persona.nombres} {usuario.persona.apellido_paterno}",
                rol=usuario.roles[0].nombre if usuario.roles else "Sin rol",
                permisos=[
                    p.nombre 
                    for r in usuario.roles 
                    for p in r.permisos 
                    if r.is_active and p.is_active
                ],
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
            
        except Unauthorized:
            # Re-lanzar errores de autenticación sin modificar
            raise
            
        except Exception as e:
            # Rollback en caso de error inesperado
            db.rollback()
            logger.error(f"❌ Error inesperado en login: {str(e)}", exc_info=True)
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
            
            # Commit explícito para persistir
            db.commit()
            
            # Refrescar el objeto para que tenga el ID asignado
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
            id_persona=usuario.persona.id_persona,
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
        
    @staticmethod
    def cambiar_password(
        db: Session,
        usuario_id: int,
        password_actual: str,
        password_nueva: str,
        ip_address: Optional[str] = None
    ) -> dict:
        """
        🔐 Cambiar contraseña del usuario autenticado
        
        Validaciones:
        - Verifica que la contraseña actual sea correcta
        - Valida que la nueva contraseña cumpla requisitos de seguridad
        - Registra el cambio en Bitácora
        - Registra intentos fallidos en LoginLog
        
        ✅ USA FLUSH + COMMIT explícito para persistencia
        
        Args:
            db: Sesión de base de datos
            usuario_id: ID del usuario que cambia su contraseña
            password_actual: Contraseña actual del usuario
            password_nueva: Nueva contraseña
            ip_address: IP desde donde se hace el cambio (para auditoría)
        
        Returns:
            dict con mensaje de éxito
            
        Raises:
            HTTPException 401: Si la contraseña actual es incorrecta
            HTTPException 404: Si el usuario no existe
        """
        try:
            # Obtener usuario
            usuario = db.query(Usuario).filter(
                Usuario.id_usuario == usuario_id,
                Usuario.is_active == True
            ).first()
            
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Verificar contraseña actual
            if not AuthService.verify_password(password_actual, usuario.password):
                # Registrar intento fallido
                AuthService.registrar_login_log(
                    db=db,
                    id_usuario=usuario_id,
                    ip_address=ip_address,
                    user_agent="Cambio de contraseña",
                    estado='fallido'
                )
                db.commit()  # Persistir el intento fallido
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="La contraseña actual es incorrecta"
                )
            
            # Hashear nueva contraseña
            nuevo_hash = AuthService.hash_password(password_nueva)
            
            # Actualizar contraseña
            usuario.password = nuevo_hash
            db.flush()
            
            # Registrar en Bitácora
            AuthService.registrar_bitacora(
                db=db,
                usuario_id=usuario_id,
                accion='CAMBIAR_PASSWORD',
                tipo_objetivo='Usuario',
                id_objetivo=usuario_id,
                descripcion=f"Usuario '{usuario.usuario}' cambió su contraseña desde IP {ip_address}"
            )
            
            # Commit explícito para persistir
            db.commit()
            
            logger.info(f"✅ Contraseña cambiada exitosamente para usuario {usuario.usuario}")
            
            return {
                "mensaje": "Contraseña cambiada exitosamente",
                "usuario": usuario.usuario
            }
            
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error al cambiar contraseña: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cambiar contraseña"
            )


# ============================================
# DEPENDENCIA PARA FASTAPI
# ============================================

# ============================================
# DEPENDENCIA PARA FASTAPI (FINAL DEL ARCHIVO)
# ============================================

from sqlalchemy.orm import joinedload, selectinload

def get_current_user_dependency(
    request: Request,
    db: Session = Depends(get_db)
) -> Usuario:
    """
    ✅ DEPENDENCIA CORREGIDA
    Obtener usuario actual desde el token JWT con eager loading
    
    Esta función:
    1. Extrae el token del header Authorization
    2. Valida el token usando AuthService.decode_token()
    3. Carga el usuario con TODAS sus relaciones (persona, roles, permisos)
    4. Inyecta metadata útil (_token, _ip)
    
    Returns:
        Usuario: Objeto Usuario con relaciones cargadas
        
    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    # 1️⃣ Extraer token del header
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    
    if not token:
        logger.warning("❌ Token no proporcionado en request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        # 2️⃣ Validar token y extraer usuario_id
        payload = AuthService.decode_token(token)
        usuario_id: int = payload.get("usuario_id") or payload.get("sub")
        
        if not usuario_id:
            logger.error("❌ Token no contiene usuario_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta identificador de usuario"
            )
        
        # 3️⃣ Cargar usuario con EAGER LOADING (crítico para permisos)
        # ✅ CORRECCIÓN: Usar Rol.permisos en vez de string 'permisos'
        usuario = db.query(Usuario).options(
            joinedload(Usuario.persona),  # Cargar persona
            selectinload(Usuario.roles).selectinload(Rol.permisos)  # ← CORREGIDO: Usar Rol.permisos
        ).filter(
            Usuario.id_usuario == usuario_id,
            Usuario.is_active == True
        ).first()
        
        if not usuario:
            logger.warning(f"❌ Usuario {usuario_id} no encontrado o inactivo")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        # 4️⃣ Inyectar metadata útil
        usuario._token = token
        usuario._ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or (
            request.client.host if request.client else "unknown"
        )
        
        logger.debug(f"✅ Usuario cargado correctamente: {usuario.usuario} (ID: {usuario.id_usuario})")
        logger.debug(f"   Roles: {[r.nombre for r in usuario.roles if r.is_active]}")
        
        return usuario
        
    except HTTPException:
        # Re-lanzar HTTPException sin modificar
        raise
    except Exception as e:
        logger.error(f"❌ Error al obtener usuario del token: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error al validar token"
        )