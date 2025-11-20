"""
app/core/middleware/jwt_middleware.py
✅ FIX: Permitir peticiones OPTIONS (CORS preflight) sin autenticación
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging

from app.modules.auth.services.auth_service import AuthService
from app.core.database import get_db

logger = logging.getLogger(__name__)

# Rutas públicas que NO requieren autenticación
PUBLIC_ROUTES = [
    "/api/auth/login",
    # "/api/auth/registro",  # Comentado - ahora requiere autenticación
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/",  # Root
]


class JWTMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validar JWT en todas las rutas protegidas
    
    - Intercepta TODAS las requests
    - ✅ Permite peticiones OPTIONS (CORS preflight) sin validación
    - Valida token JWT si la ruta NO es pública
    - Inyecta usuario autenticado en request.state
    - Registra IP del cliente
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Procesar request y validar JWT"""
        
        # ✅ CRÍTICO: Permitir peticiones OPTIONS sin autenticación (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # 1. Verificar si la ruta es pública
        if self._is_public_route(request.url.path):
            return await call_next(request)
        
        # 2. Extraer token del header Authorization
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
        
        # 3. Validar token y obtener usuario
        request.state.token = token
        request.state.client_ip = self._get_client_ip(request)
        
        # 4. Continuar con la request
        response = await call_next(request)
        return response
    
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