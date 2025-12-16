"""
app/core/middleware/jwt_middleware.py
Middleware JWT - OPTIMIZADO con debugging mejorado
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging
from datetime import datetime, timedelta

from app.shared.security import verify_token
from app.core.database import get_db
from app.modules.usuarios.models.usuario_models import Usuario, Rol
from sqlalchemy.orm import joinedload, selectinload

logger = logging.getLogger(__name__)

# Rutas públicas que NO requieren autenticación
PUBLIC_ROUTES = [
    "/api/auth/login",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/api/health",
    "/uploads",  # ✅ Archivos estáticos (imágenes, evidencias, etc.)
]

# ✅ CACHÉ EN MEMORIA: Evita consultas repetidas a BD
_user_cache = {}
CACHE_TTL_SECONDS = 300  # 5 minutos


def _get_cached_user(db, user_id: int):
    """
    ✅ Obtener usuario desde caché o BD (con eager loading)
    """
    now = datetime.utcnow()
    
    # Verificar caché
    if user_id in _user_cache:
        cached_user, expiry = _user_cache[user_id]
        if now < expiry:
            logger.debug(f"✅ Usuario {user_id} obtenido desde caché")
            return cached_user
        else:
            del _user_cache[user_id]
    
    # Consultar BD con EAGER LOADING
    usuario = db.query(Usuario).options(
        joinedload(Usuario.persona),
        selectinload(Usuario.roles).selectinload(Rol.permisos)
    ).filter(
        Usuario.id_usuario == user_id,
        Usuario.is_active == True
    ).first()
    
    if usuario:
        expiry = now + timedelta(seconds=CACHE_TTL_SECONDS)
        _user_cache[user_id] = (usuario, expiry)
        logger.debug(f"✅ Usuario {user_id} cargado desde BD y almacenado en caché")
    else:
        logger.warning(f"⚠️ Usuario {user_id} no encontrado o inactivo en BD")
    
    return usuario


def clear_user_cache(user_id: int = None):
    """Limpiar caché de usuario"""
    global _user_cache
    if user_id:
        _user_cache.pop(user_id, None)
        logger.info(f"🗑️ Caché limpiado para usuario {user_id}")
    else:
        _user_cache.clear()
        logger.info("🗑️ Caché completo limpiado")


class JWTMiddleware(BaseHTTPMiddleware):
    """
    Middleware optimizado para validar JWT con debugging mejorado
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Procesar request y validar JWT"""
        
        path = request.url.path
        method = request.method
        
        logger.info(f"🔍 JWT Middleware INICIO: {method} {path}")
        
        # 🚀 CRÍTICO: Permitir OPTIONS sin validación (CORS preflight)
        if method == "OPTIONS":
            logger.info(f"✅ OPTIONS - pasando sin validación: {path}")
            return await call_next(request)
        
        # 🚀 Verificar si la ruta es pública
        logger.info(f"🔍 Verificando si es ruta pública: {path}")
        if self._is_public_route(path):
            logger.info(f"✅ Ruta pública - pasando sin validación: {method} {path}")
            return await call_next(request)
        
        logger.info(f"🔐 Ruta protegida - validando JWT: {method} {path}")
        
        # 🔍 DEBUG: Mostrar headers recibidos
        auth_header = request.headers.get("Authorization")
        logger.info(f"🔐 Validando JWT para: {method} {path}")
        logger.debug(f"📋 Authorization header: {auth_header[:50] + '...' if auth_header else 'NO PRESENTE'}")
        
        # 🚀 Extraer token del header
        token = self._extract_token(request)
        
        if not token:
            logger.warning(f"❌ Token no proporcionado en: {method} {path}")
            logger.debug(f"📋 Headers recibidos: {dict(request.headers)}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message": "Token no proporcionado. Header 'Authorization: Bearer <token>' requerido.",
                    "data": None
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        try:
            # 🚀 Verificar token JWT
            logger.debug(f"🔍 Verificando token: {token[:20]}...")
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            logger.debug(f"✅ Token válido. User ID: {user_id}")
            
            if not user_id:
                logger.error("❌ Token no contiene 'sub' (user_id)")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": "Token inválido: falta identificador de usuario",
                        "data": None
                    }
                )
            
            # 🚀 OPTIMIZACIÓN: Obtener usuario desde caché o BD
            db = next(get_db())
            try:
                usuario = _get_cached_user(db, int(user_id))
                
                if not usuario:
                    logger.warning(f"❌ Usuario {user_id} no encontrado o inactivo")
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "success": False,
                            "message": "Usuario no encontrado o inactivo",
                            "data": None
                        }
                    )
                
                # ✅ Inyectar usuario en request.state
                request.state.user = usuario
                request.state.token = token
                request.state.client_ip = self._get_client_ip(request)
                
                logger.info(f"✅ Usuario autenticado: {usuario.usuario} ({usuario.id_usuario}) - {method} {path}")
                logger.info(f"✅ Roles del usuario: {[r.nombre for r in usuario.roles if r.is_active]}")
                
            finally:
                db.close()
            
            response = await call_next(request)
            
            # Log del status code de la respuesta
            logger.info(f"📤 Response: {response.status_code} - {method} {path}")
            
            return response
            
        except HTTPException as e:
            logger.error(f"❌ HTTPException en JWT: {e.status_code} - {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "message": str(e.detail),
                    "data": None
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error inesperado en JWT middleware: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Error interno del servidor al validar autenticación",
                    "data": None
                }
            )
    
    def _is_public_route(self, path: str) -> bool:
        """Verificar si la ruta es pública"""
        logger.info(f"🔍 Verificando ruta: '{path}' contra PUBLIC_ROUTES: {PUBLIC_ROUTES}")
        for route in PUBLIC_ROUTES:
            if path.startswith(route):
                logger.info(f"✅ MATCH encontrado: '{path}'.startswith('{route}') = True")
                return True
        logger.info(f"❌ NO es ruta pública: '{path}'")
        return False
    
    def _extract_token(self, request: Request) -> str:
        """Extraer token del header Authorization"""
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            logger.debug("❌ Header 'Authorization' no presente")
            return None
        
        # Formato: "Bearer <token>"
        parts = auth_header.split()
        
        if len(parts) != 2:
            logger.warning(f"❌ Formato de Authorization inválido: {len(parts)} partes (esperado: 2)")
            return None
        
        if parts[0].lower() != "bearer":
            logger.warning(f"❌ Tipo de auth inválido: '{parts[0]}' (esperado: 'Bearer')")
            return None
        
        logger.debug(f"✅ Token extraído correctamente: {parts[1][:20]}...")
        return parts[1]
    
    def _get_client_ip(self, request: Request) -> str:
        """Obtener IP del cliente (considerando proxies)"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"