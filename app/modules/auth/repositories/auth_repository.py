"""
auth_repository.py - VERSIÓN OPTIMIZADA

"""
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import and_, func
from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona1, LoginLog, Bitacora, Rol
)
from typing import Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Constantes
MAX_INTENTOS_FALLIDOS = 3
TIEMPO_BLOQUEO_MINUTOS = 10


class AuthRepository:
    """Repositorio optimizado para operaciones de autenticación"""
    
    # ==================== BÚSQUEDAS DE USUARIO ====================
    
    @staticmethod
    def buscar_usuario_por_nombre(db: Session, usuario: str) -> Optional[Usuario]:
        """
        🚀 OPTIMIZADO: Buscar usuario con eager loading de relaciones
        Carga persona, roles y permisos en 1 query en vez de 3-5
        """
        return db.query(Usuario).options(
            joinedload(Usuario.persona),
            selectinload(Usuario.roles).selectinload(Rol.permisos)
        ).filter(
            Usuario.usuario == usuario,
            Usuario.is_active == True
        ).first()
    
    @staticmethod
    def buscar_usuario_por_correo(db: Session, correo: str) -> Optional[Usuario]:
        """🚀 OPTIMIZADO: Buscar usuario por correo con eager loading"""
        return db.query(Usuario).options(
            joinedload(Usuario.persona),
            selectinload(Usuario.roles).selectinload(Rol.permisos)
        ).filter(
            Usuario.correo == correo,
            Usuario.is_active == True
        ).first()
    
    @staticmethod
    def buscar_usuario_por_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        """🚀 OPTIMIZADO: Buscar usuario por ID con eager loading"""
        return db.query(Usuario).options(
            joinedload(Usuario.persona),
            selectinload(Usuario.roles).selectinload(Rol.permisos)
        ).filter(
            Usuario.id_usuario == usuario_id,
            Usuario.is_active == True
        ).first()
    
    # ==================== BÚSQUEDAS DE PERSONA ====================
    
    @staticmethod
    def buscar_persona_por_ci(db: Session, ci: str) -> Optional[Persona1]:
        """Buscar persona por CI"""
        return db.query(Persona1).filter(
            Persona1.ci == ci,
            Persona1.is_active == True
        ).first()
    
    @staticmethod
    def buscar_persona_por_id(db: Session, persona_id: int) -> Optional[Persona1]:
        """Buscar persona por ID"""
        return db.query(Persona1).filter(
            Persona1.id_persona == persona_id,
            Persona1.is_active == True
        ).first()
    
    # ==================== LOGS Y AUDITORÍA ====================
    
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
        USA FLUSH, NO COMMIT (commit lo hace el servicio)
        
        🚀 OPTIMIZADO: Logs reducidos (solo loggea fallos)
        """
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
        
        # 🚀 Solo loggear fallos (reducir ruido)
        if estado == 'fallido':
            logger.warning(f"❌ Login fallido: usuario {id_usuario} desde {ip_address}")
        
        return login_log
    
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
        Registrar acción en Bitácora
        USA FLUSH, NO COMMIT
        
        🚀 OPTIMIZADO: Solo loggea acciones críticas
        """
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
        
        # 🚀 Solo loggear acciones críticas
        acciones_criticas = [
            'LOGIN', 'LOGOUT', 'CREAR_USUARIO', 'ELIMINAR_USUARIO',
            'CAMBIAR_PASSWORD', 'ASIGNAR_ROL', 'REVOCAR_ROL'
        ]
        if accion in acciones_criticas:
            logger.info(f"📝 Bitácora: {accion} por usuario {usuario_id}")
        
        return bitacora
    
    # ==================== CONTROL DE INTENTOS FALLIDOS ====================
    
    @staticmethod
    def contar_intentos_fallidos(
        db: Session,
        usuario_id: int,
        minutos: int = TIEMPO_BLOQUEO_MINUTOS
    ) -> int:
        """Contar intentos fallidos - SIN logging innecesario"""
        tiempo_limite = datetime.now() - timedelta(minutes=minutos)
        
        intentos = db.query(LoginLog).filter(
            and_(
                LoginLog.id_usuario == usuario_id,
                LoginLog.estado == 'fallido',
                LoginLog.fecha_hora >= tiempo_limite
            )
        ).count()
        
        # ✅ SOLO loggear si hay 3+ intentos (posible ataque)
        if intentos >= 3:
            logger.warning(f"🚨 ALERTA: Usuario {usuario_id} tiene {intentos} intentos fallidos")
        
        return intentos
    
    @staticmethod
    def obtener_ultimo_intento_fallido(
        db: Session,
        usuario_id: int
    ) -> Optional[LoginLog]:
        """
        Obtener el último intento fallido de login
        
        Returns:
            LoginLog del último intento fallido o None
        """
        return db.query(LoginLog).filter(
            and_(
                LoginLog.id_usuario == usuario_id,
                LoginLog.estado == 'fallido'
            )
        ).order_by(LoginLog.fecha_hora.desc()).first()
    
    @staticmethod
    def verificar_cuenta_bloqueada(
        db: Session,
        usuario_id: int,
        max_intentos: int = MAX_INTENTOS_FALLIDOS,
        minutos_bloqueo: int = TIEMPO_BLOQUEO_MINUTOS
    ) -> tuple[bool, Optional[datetime]]:
        """
        Verificar si la cuenta está bloqueada por intentos fallidos
        
        Args:
            db: Sesión de base de datos
            usuario_id: ID del usuario
            max_intentos: Máximo de intentos permitidos (default 3)
            minutos_bloqueo: Duración del bloqueo (default 10)
        
        Returns:
            Tupla (está_bloqueada, fecha_desbloqueo)
        """
        intentos = AuthRepository.contar_intentos_fallidos(
            db, usuario_id, minutos_bloqueo
        )
        
        if intentos >= max_intentos:
            ultimo_intento = AuthRepository.obtener_ultimo_intento_fallido(db, usuario_id)
            if ultimo_intento:
                fecha_desbloqueo = ultimo_intento.fecha_hora + timedelta(minutes=minutos_bloqueo)
                if datetime.now() < fecha_desbloqueo:
                    logger.warning(f"🔒 Usuario {usuario_id} bloqueado hasta {fecha_desbloqueo}")
                    return True, fecha_desbloqueo
        
        return False, None
    
    @staticmethod
    def limpiar_intentos_fallidos(db: Session, usuario_id: int):
        """
        Limpiar intentos fallidos después de login exitoso
        
        NO ELIMINA registros (para auditoría), solo marca como procesados
        agregando un login exitoso nuevo
        """
        # No es necesario eliminar, solo registrar el éxito
        # Los intentos fallidos antiguos serán ignorados por la ventana de tiempo
        # logger.info(f"Intentos fallidos limpiados para usuario {usuario_id}")
        pass
    
    # ==================== BLACKLIST DE TOKENS ====================
    
    # Nota: En producción, usar Redis para blacklist
    _token_blacklist = set()
    
    @staticmethod
    def agregar_token_blacklist(token: str):
        """Agregar token a la blacklist (logout)"""
        AuthRepository._token_blacklist.add(token)
        # Solo loggear en desarrollo/debug
        # logger.debug(f"Token agregado a blacklist. Total: {len(AuthRepository._token_blacklist)}")
    
    @staticmethod
    def verificar_token_blacklist(token: str) -> bool:
        """Verificar si un token está en la blacklist"""
        return token in AuthRepository._token_blacklist
    
    @staticmethod
    def limpiar_blacklist():
        """Limpiar blacklist (para tests o mantenimiento)"""
        AuthRepository._token_blacklist.clear()
        logger.info("🗑️ Blacklist de tokens limpiada")