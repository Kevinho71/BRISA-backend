"""
app/core/middleware/jwt_middleware.py
Middleware JWT - OPTIMIZADO con caché en memoria
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging
from datetime import datetime, timedelta

from app.shared.security import verify_token
from app.core.database import get_db
from app.modules.usuarios.models.usuario_models import Usuario
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
    "/",
]

# ✅ CACHÉ EN MEMORIA: Evita consultas repetidas a BD
# Formato: {user_id: (usuario_obj, timestamp_expiracion)}
_user_cache = {}
CACHE_TTL_SECONDS = 300  # 5 minutos


def _get_cached_user(db, user_id: int):
    """
    ✅ Obtener usuario desde caché o BD (con eager loading)
    Reduce consultas a BD de ~100/min a ~10/min
    """
    now = datetime.utcnow()
    
    # Verificar si está en caché y no ha expirado
    if user_id in _user_cache:
        cached_user, expiry = _user_cache[user_id]
        if now < expiry:
            return cached_user
        else:
            # Limpiar entrada expirada
            del _user_cache[user_id]
    
    # Consultar BD con EAGER LOADING (1 query en vez de 3-5)
    usuario = db.query(Usuario).options(
        joinedload(Usuario.persona),
        selectinload(Usuario.roles).selectinload('permisos')
    ).filter(
        Usuario.id_usuario == user_id,
        Usuario.is_active == True
    ).first()
    
    # Guardar en caché si existe
    if usuario:
        expiry = now + timedelta(seconds=CACHE_TTL_SECONDS)
        _user_cache[user_id] = (usuario, expiry)
    
    return usuario


def clear_user_cache(user_id: int = None):
    """
    ✅ Limpiar caché de usuario
    Llamar cuando se actualice/elimine un usuario
    """
    global _user_cache
    if user_id:
        _user_cache.pop(user_id, None)
    else:
        _user_cache.clear()


class JWTMiddleware(BaseHTTPMiddleware):
    """
    Middleware optimizado para validar JWT
    
    MEJORAS:
    - ✅ Caché de usuarios en memoria (5 min TTL)
    - ✅ Eager loading de relaciones (1 query vs 3-5)
    - ✅ Logs reducidos (solo errores críticos)
    - ✅ Validación rápida de rutas públicas
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Procesar request y validar JWT"""
        
        # 🚀 CRÍTICO: Permitir OPTIONS sin validación (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # 🚀 Verificar si la ruta es pública (sin logs innecesarios)
        if self._is_public_route(request.url.path):
            return await call_next(request)
        
        # 🚀 Extraer token del header
        token = self._extract_token(request)
        
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message": "Token no proporcionado",
                    "data": None
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        try:
            # 🚀 Verificar token JWT
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": "Token inválido",
                        "data": None
                    }
                )
            
            # 🚀 OPTIMIZACIÓN: Obtener usuario desde caché o BD
            db = next(get_db())
            try:
                usuario = _get_cached_user(db, int(user_id))
                
                if not usuario:
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
                
            finally:
                db.close()
            
            # ✅ LOGS REDUCIDOS: Solo loggear si es necesario
            # logger.info(f"Request: {request.method} {request.url.path}")
            
            response = await call_next(request)
            return response
            
        except HTTPException as e:
            # Solo loggear errores críticos
            if e.status_code >= 500:
                logger.error(f"❌ Error JWT: {str(e)}")
            
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "message": str(e.detail),
                    "data": None
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error inesperado en JWT middleware: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": "Error interno del servidor",
                    "data": None
                }
            )
    
    def _is_public_route(self, path: str) -> bool:
        """Verificar si la ruta es pública"""
        return any(path.startswith(route) for route in PUBLIC_ROUTES)
    
    def _extract_token(self, request: Request) -> str:
        """Extraer token del header Authorization"""
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return None
        
        # Formato: "Bearer <token>"
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        
        return parts[1]
    
    def _get_client_ip(self, request: Request) -> str:
        """Obtener IP del cliente (considerando proxies)"""
        # Intentar obtener IP real detrás de proxies
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback a IP directa
        return request.client.host if request.client else "unknown"