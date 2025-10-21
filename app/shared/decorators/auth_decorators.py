"""
Decoradores compartidos para el sistema BRISA Backend

Estos decoradores proporcionan funcionalidad común de autenticación y autorización.
Los equipos implementarán la lógica específica según sus necesidades.

Nota: El equipo del Módulo 1 (Usuarios) implementará la lógica completa
      de autenticación JWT y verificación de permisos/roles.
"""

from functools import wraps
from typing import Callable, List, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# ============================================================================
# DECORADORES PARA FASTAPI (Dependencies)
# ============================================================================

def require_permissions(*permissions: str):
    """
    Dependency para requerir permisos específicos en endpoints FastAPI.
    
    Usage:
        from fastapi import Depends
        
        @router.get("/admin", dependencies=[Depends(require_permissions("admin.access"))])
        async def admin_endpoint():
            return {"message": "Admin access granted"}
    
    Args:
        permissions: Lista de permisos requeridos (el usuario debe tener TODOS)
    
    Note:
        El equipo del Módulo 1 implementará la lógica de verificación de permisos.
        Por ahora es un stub que siempre permite el acceso.
    
    TODO (Módulo 1):
        - Extraer y validar token JWT
        - Obtener permisos del usuario desde BD
        - Verificar que el usuario tenga TODOS los permisos requeridos
        - Lanzar HTTPException(403) si faltan permisos
    """
    async def dependency():
        # TODO: Implementar verificación real de permisos
        # Ejemplo de implementación:
        # token = await get_token_from_request()
        # user = await get_user_from_token(token)
        # user_permissions = await get_user_permissions(user.id)
        # 
        # for permission in permissions:
        #     if permission not in user_permissions:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN,
        #             detail=f"Permission required: {permission}"
        #         )
        
        # Por ahora, stub que permite todo
        pass
    
    return dependency


def require_roles(*roles: str):
    """
    Dependency para requerir roles específicos en endpoints FastAPI.
    
    Usage:
        from fastapi import Depends
        
        @router.get("/manager", dependencies=[Depends(require_roles("manager", "admin"))])
        async def manager_endpoint():
            return {"message": "Manager access granted"}
    
    Args:
        roles: Lista de roles permitidos (el usuario debe tener AL MENOS UNO)
    
    Note:
        El equipo del Módulo 1 implementará la lógica de verificación de roles.
        Por ahora es un stub que siempre permite el acceso.
    
    TODO (Módulo 1):
        - Extraer y validar token JWT
        - Obtener roles del usuario desde BD
        - Verificar que el usuario tenga al menos uno de los roles
        - Lanzar HTTPException(403) si no tiene ningún rol válido
    """
    async def dependency():
        # TODO: Implementar verificación real de roles
        # Ejemplo de implementación:
        # token = await get_token_from_request()
        # user = await get_user_from_token(token)
        # user_roles = await get_user_roles(user.id)
        # 
        # if not any(role in user_roles for role in roles):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail=f"Role required: {' or '.join(roles)}"
        #     )
        
        # Por ahora, stub que permite todo
        pass
    
    return dependency


async def get_current_user():
    """
    Dependency para obtener el usuario actual autenticado.
    
    Usage:
        from fastapi import Depends
        
        @router.get("/me")
        async def get_me(current_user = Depends(get_current_user)):
            return {"user": current_user}
    
    Returns:
        Usuario actual autenticado
    
    Raises:
        HTTPException 401: Si no hay token o token inválido
    
    Note:
        El equipo del Módulo 1 implementará esta función.
        Por ahora retorna un usuario de prueba.
    
    TODO (Módulo 1):
        - Extraer token del header Authorization
        - Validar token JWT
        - Obtener usuario desde BD
        - Retornar objeto usuario
        - Lanzar HTTPException(401) si falla la autenticación
    """
    # TODO: Implementar obtención real del usuario
    # Ejemplo de implementación:
    # token = await get_token_from_request()
    # 
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    #     user_id = payload.get("sub")
    #     user = await get_user_by_id(user_id)
    #     
    #     if not user:
    #         raise HTTPException(status_code=401, detail="User not found")
    #     
    #     return user
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    
    # Por ahora, stub que retorna usuario de prueba
    return {
        "id": 1,
        "nombre": "Usuario de Prueba",
        "email": "test@example.com",
        "roles": ["user"]
    }


async def require_auth():
    """
    Dependency simple para verificar que el usuario esté autenticado.
    
    Usage:
        @router.get("/protected", dependencies=[Depends(require_auth)])
        async def protected_endpoint():
            return {"message": "You are authenticated"}
    
    Raises:
        HTTPException 401: Si no hay token o token inválido
    
    Note:
        El equipo del Módulo 1 implementará esta función.
        Por ahora es un stub que siempre permite el acceso.
    
    TODO (Módulo 1):
        - Extraer token del header Authorization
        - Validar token JWT
        - Lanzar HTTPException(401) si el token es inválido o no existe
    """
    # TODO: Implementar verificación real de autenticación
    # Ejemplo de implementación:
    # token = await get_token_from_request()
    # 
    # try:
    #     jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # except JWTError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not authenticated",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    # Por ahora, stub que permite todo
    pass


# ============================================================================
# UTILIDADES PARA TOKENS JWT (A implementar por Módulo 1)
# ============================================================================

async def get_token_from_request(request: Request) -> str:
    """
    Extrae el token JWT del header Authorization.
    
    Args:
        request: Request object de FastAPI
    
    Returns:
        Token JWT sin el prefijo "Bearer"
    
    Raises:
        HTTPException 401: Si no hay token
    
    TODO (Módulo 1): Implementar extracción de token
    """
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


# ============================================================================
# NOTAS PARA LOS EQUIPOS
# ============================================================================

"""
IMPLEMENTACIÓN SUGERIDA PARA EL MÓDULO 1 (Usuarios):

1. Instalar python-jose para JWT:
   pip install python-jose[cryptography]

2. Crear funciones de utilidad JWT:
   - create_access_token(data: dict) -> str
   - verify_token(token: str) -> dict
   - get_token_payload(token: str) -> dict

3. Implementar las funciones de este archivo:
   - get_current_user(): Extraer usuario desde token
   - require_auth(): Verificar que el token sea válido
   - require_permissions(): Verificar permisos del usuario
   - require_roles(): Verificar roles del usuario

4. Ejemplo de uso completo:

from fastapi import APIRouter, Depends
from app.shared.decorators.auth_decorators import (
    get_current_user, 
    require_permissions,
    require_roles
)

router = APIRouter()

# Endpoint que requiere autenticación
@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user

# Endpoint que requiere rol específico
@router.get("/admin", dependencies=[Depends(require_roles("admin"))])
async def admin_panel():
    return {"message": "Welcome admin"}

# Endpoint que requiere permiso específico
@router.post("/users", dependencies=[Depends(require_permissions("users.create"))])
async def create_user(user_data: dict):
    return {"message": "User created"}

5. Estructura de token JWT sugerida:
   {
       "sub": "user_id",
       "email": "user@example.com",
       "roles": ["admin", "user"],
       "permissions": ["users.read", "users.write"],
       "exp": timestamp
   }
"""
