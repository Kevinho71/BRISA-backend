"""
app/shared/permissions.py
Decorador para validar permisos en endpoints
"""
from functools import wraps
from fastapi import HTTPException, status
from typing import Callable
import inspect

from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.permission_mapper import tiene_permiso


def requires_permission(permission_name: str):
    """
    Decorador para validar que el usuario tiene un permiso específico
    
    Este decorador usa el sistema de mapeo para traducir permisos específicos
    (ej: "editar_usuario") a permisos genéricos de la BD (ej: "Modificar")
    
    Soporta tanto funciones async como síncronas.
    
    Uso:
        @router.put("/usuarios/{usuario_id}")
        @requires_permission("editar_usuario")
        async def actualizar_usuario(...):
            ...
        
        @router.get("/usuarios")
        @requires_permission("ver_usuario")
        def listar_usuarios(...):
            ...
    """
    def decorator(func: Callable):
        # Verificar si la función es async
        is_async = inspect.iscoroutinefunction(func)
        
        if is_async:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # Obtener parámetros de la función
                sig = inspect.signature(func)
                bound_args = sig.bind_partial(*args, **kwargs)
                bound_args.apply_defaults()
                
                # Buscar current_user en los argumentos
                current_user = bound_args.arguments.get('current_user')
                
                # Si no lo encontramos en bound_args, buscar en kwargs
                if current_user is None:
                    current_user = kwargs.get('current_user')
                
                # Verificar que tenemos un usuario
                if not current_user or not isinstance(current_user, Usuario):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado - Usuario no autenticado",
                        headers={"WWW-Authenticate": "Bearer"}
                    )
                
                # Verificar si el usuario tiene el permiso usando el mapeo
                if not tiene_permiso(current_user, permission_name):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"No tienes permiso para: {permission_name}"
                    )
                
                # Ejecutar la función original (async)
                return await func(*args, **kwargs)
            
            return async_wrapper
        else:
            @wraps(func)
            async def sync_wrapper(*args, **kwargs):
                # Obtener parámetros de la función
                sig = inspect.signature(func)
                bound_args = sig.bind_partial(*args, **kwargs)
                bound_args.apply_defaults()
                
                # Buscar current_user en los argumentos
                current_user = bound_args.arguments.get('current_user')
                
                # Si no lo encontramos en bound_args, buscar en kwargs
                if current_user is None:
                    current_user = kwargs.get('current_user')
                
                # Verificar que tenemos un usuario
                if not current_user or not isinstance(current_user, Usuario):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado - Usuario no autenticado",
                        headers={"WWW-Authenticate": "Bearer"}
                    )
                
                # Verificar si el usuario tiene el permiso usando el mapeo
                if not tiene_permiso(current_user, permission_name):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"No tienes permiso para: {permission_name}"
                    )
                
                # Ejecutar la función original (síncrona)
                return func(*args, **kwargs)
            
            return sync_wrapper
    return decorator


def check_permission(usuario: Usuario, permission_name: str) -> bool:
    """
    Función helper para verificar si un usuario tiene un permiso
    
    Usa el sistema de mapeo para traducir permisos específicos a genéricos
    
    Args:
        usuario: Instancia del usuario
        permission_name: Nombre del permiso a verificar (ej: "editar_usuario")
    
    Returns:
        bool: True si tiene el permiso, False si no
    """
    return tiene_permiso(usuario, permission_name)