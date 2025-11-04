"""
Decoradores compartidos para el sistema BRISA Backend
"""
from functools import wraps
from fastapi import Depends, HTTPException, status, Request
from typing import List, Optional

# Extraer token del header
async def get_token_from_request(request: Request) -> str:
    """Extrae el token JWT del header Authorization"""
    authorization = request.headers.get("Authorization")
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Obtener usuario actual
async def get_current_user(request: Request = None):
    """
    Dependency para obtener el usuario actual autenticado.
    Stub: reemplazar con AuthService real.
    """
    if request is None:
        raise HTTPException(status_code=401, detail="No request context")
    
    try:
        token = await get_token_from_request(request)
        # Stub: usuario simulado
        return {
            "id": 1,
            "email": "user@example.com",
            "roles": ["admin"],
            "permisos": ["ver_usuario", "crear_usuario", "generar_reportes"]
        }
    except HTTPException:
        raise


# Decorador: require_auth
def require_auth(func):
    """Decorador para requerir autenticación"""
    @wraps(func)
    async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
        return await func(*args, current_user=current_user, **kwargs)
    return wrapper


# Decorador: require_roles  <-- plural, así es como lo busca el verificador
def require_roles(*allowed_roles: str):
    """Decorador para requerir uno o más roles"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
            
            user_roles = current_user.get("roles", [])
            if not any(role in allowed_roles for role in user_roles):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permiso")
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


# Decorador: require_permissions
def require_permissions(*allowed_permissions: str):
    """Decorador para requerir permisos específicos"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
            
            user_permissions = current_user.get("permisos", [])
            if not all(p in user_permissions for p in allowed_permissions):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene los permisos necesarios")
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
