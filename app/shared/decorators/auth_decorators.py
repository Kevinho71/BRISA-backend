"""
app/shared/decorators/auth_decorato
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


"""
app/shared/decorators/auth_decorators.py
Decoradores de autenticación y autorización - INTEGRADO CON SISTEMA REAL
"""
from functools import wraps
from fastapi import Depends, HTTPException, status
from typing import Callable
from sqlalchemy.orm import Session

from app.modules.usuarios.models.usuario_models import Usuario
from app.core.database import get_db
from app.modules.auth.services.auth_service import get_current_user_dependency


def require_permissions(*required_permissions: str):
    """
    Decorador para validar que el usuario tenga los permisos requeridos.
    
    Uso en endpoints:
        @router.put("/usuarios/{id_usuario}")
        @require_permissions('editar_usuario')
        async def actualizar_usuario(...):
            ...
    
    Args:
        *required_permissions: Lista de NOMBRES de permisos requeridos (al menos uno)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # El current_user debe venir de los kwargs (inyectado por Depends)
            current_user: Usuario = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            # Obtener todos los permisos del usuario desde sus roles
            permisos_usuario = set()
            if current_user.roles:
                for rol in current_user.roles:
                    if rol.permisos:
                        for permiso in rol.permisos:
                            # ✅ USAR NOMBRE (no código, porque no existe en DB)
                            permisos_usuario.add(permiso.nombre.lower())
            
            # Verificar si tiene al menos uno de los permisos requeridos
            tiene_permiso = any(
                permiso.lower() in permisos_usuario 
                for permiso in required_permissions
            )
            
            if not tiene_permiso:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"No tiene permisos para realizar esta acción. Se requiere: {', '.join(required_permissions)}"
                )
            
            # Si pasa la validación, ejecutar la función
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_all_permissions(*required_permissions: str):
    """
    Decorador que requiere TODOS los permisos especificados.
    
    Similar a require_permissions pero más estricto.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: Usuario = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            permisos_usuario = set()
            if current_user.roles:
                for rol in current_user.roles:
                    if rol.permisos:
                        for permiso in rol.permisos:
                            permisos_usuario.add(permiso.codigo)
            
            # Verificar que tenga TODOS los permisos
            faltantes = [p for p in required_permissions if p not in permisos_usuario]
            
            if faltantes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permisos faltantes: {', '.join(faltantes)}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_roles(*required_roles: str):
    """
    Decorador para validar que el usuario tenga uno de los roles requeridos.
    
    Uso:
        @require_roles('admin', 'supervisor')
        async def funcion_protegida(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: Usuario = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            # Obtener roles del usuario
            roles_usuario = set()
            if current_user.roles:
                for rol in current_user.roles:
                    roles_usuario.add(rol.nombre.lower())
            
            # Verificar si tiene al menos uno de los roles requeridos
            tiene_rol = any(
                rol.lower() in roles_usuario 
                for rol in required_roles
            )
            
            if not tiene_rol:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Se requiere uno de estos roles: {', '.join(required_roles)}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def allow_self_or_permission(permission: str):
    """
    Decorador que permite la acción si:
    - El usuario se está modificando a sí mismo, O
    - El usuario tiene el permiso especificado
    
    Uso:
        @allow_self_or_permission('editar_usuario')
        async def actualizar_usuario(id_usuario: int, ..., current_user: Usuario):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: Usuario = kwargs.get('current_user')
            target_user_id: int = kwargs.get('id_usuario')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            # Si es el mismo usuario, permitir
            if current_user.id_usuario == target_user_id:
                return await func(*args, **kwargs)
            
            # Si no es el mismo, verificar permiso
            permisos_usuario = set()
            if current_user.roles:
                for rol in current_user.roles:
                    if rol.permisos:
                        for permiso in rol.permisos:
                            permisos_usuario.add(permiso.codigo)
            
            if permission not in permisos_usuario:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para modificar este usuario"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# Helpers para validación manual en servicios
def verificar_permiso(current_user: Usuario, permiso_requerido: str):
    """
    Helper para verificar permisos manualmente en servicios.
    Lanza HTTPException si no tiene el permiso.
    """
    permisos_usuario = set()
    if current_user.roles:
        for rol in current_user.roles:
            if rol.permisos:
                for permiso in rol.permisos:
                    permisos_usuario.add(permiso.codigo)
    
    if permiso_requerido not in permisos_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tiene el permiso requerido: {permiso_requerido}"
        )


def puede_modificar_usuario(current_user: Usuario, target_user_id: int) -> bool:
    """
    Helper para verificar si puede modificar un usuario.
    Retorna True si es el mismo usuario O tiene permiso 'editar_usuario'.
    """
    # Si es el mismo usuario
    if current_user.id_usuario == target_user_id:
        return True
    
    # Verificar permiso
    permisos_usuario = set()
    if current_user.roles:
        for rol in current_user.roles:
            if rol.permisos:
                for permiso in rol.permisos:
                    permisos_usuario.add(permiso.codigo)
    
    return 'editar_usuario' in permisos_usuario or 'admin_usuarios' in permisos_usuario


def validar_puede_modificar_usuario(current_user: Usuario, target_user_id: int):
    """
    Valida si puede modificar usuario, lanza HTTPException si no puede.
    """
    if not puede_modificar_usuario(current_user, target_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para modificar este usuario"
        )
    
