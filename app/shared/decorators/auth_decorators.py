"""
app/shared/decorators/auth_decorators.py
Decoradores de autenticación y autorización - INTEGRADO CON SISTEMA REAL
"""
from functools import wraps
from fastapi import Depends, HTTPException, status, Request
from typing import Callable,List, Optional
from sqlalchemy.orm import Session
import logging
from app.modules.usuarios.models.usuario_models import Usuario
from app.core.database import get_db
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.shared.permission_mapper import tiene_permiso, puede_modificar_usuario, puede_eliminar_usuario



logger = logging.getLogger(__name__)


def _add_current_user_dependency(func: Callable):
    """
    Helper function to add current_user dependency to function signature.
    This allows FastAPI to inject the authenticated user.
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    
    # Check if current_user is already in parameters
    if 'current_user' not in sig.parameters:
        # Add current_user parameter with Depends(get_current_user)
        from inspect import Parameter
        current_user_param = Parameter(
            'current_user',
            Parameter.KEYWORD_ONLY,
            default=Depends(get_current_user),
            annotation=Usuario
        )
        params.append(current_user_param)
    
    return sig.replace(parameters=params)


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


# Obtener usuario actual (DEPENDENCY para FastAPI)
def get_current_user(request: Request) -> Usuario:
    """
    Dependency para FastAPI que extrae el usuario del request.state.
    El JWT middleware ya validó el token e inyectó el usuario.
    
    Esta función se ejecuta DESPUÉS del middleware, por lo que request.state.user ya existe.
    """
    # El usuario fue inyectado por JWTMiddleware
    if not hasattr(request.state, 'user') or request.state.user is None:
        logger.error("❌ CRITICAL: request.state.user es None - JWT middleware no ejecutado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado - token inválido o no proporcionado"
        )
    
    logger.info(f"✅ get_current_user: {request.state.user.usuario}")
    return request.state.user


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


# Decorador: require_permission


def require_permissions(*required_roles: str):
    """
    Decorador SIMPLIFICADO que verifica solo por nombre de rol.
    
    IMPORTANTE: El endpoint DEBE incluir:
        current_user: Usuario = Depends(get_current_user)
    
    Ejemplo:
        @router.get("/endpoint")
        @require_permissions('admin', 'regente', 'recepcion')
        async def mi_endpoint(current_user: Usuario = Depends(get_current_user)):
            ...
    
    Args:
        *required_roles: Nombres de roles permitidos (admin, regente, recepcion, profesor, apoderado)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # El current_user debe venir en kwargs desde Depends(get_current_user)
            current_user: Usuario = kwargs.get('current_user')
            
            if not current_user:
                logger.warning("current_user no encontrado en kwargs")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            # MAPEO SIMPLE: nombre usado en decorador -> nombre en BD
            ROLE_MAP = {
                "admin": ["Director", "Admin", "Administrador"],
                "regente": ["Regente"],
                "recepcion": ["Recepción", "Recepcionista"],
                "profesor": ["Profesor"],
                "apoderado": ["Apoderado"]
            }
            
            # Obtener roles del usuario
            user_roles = [r.nombre for r in current_user.roles if r.is_active]
            logger.info(f"Usuario {current_user.usuario} tiene roles: {user_roles}")
            
            # Verificar si tiene alguno de los roles requeridos
            tiene_acceso = False
            for rol_requerido in required_roles:
                nombres_validos = ROLE_MAP.get(rol_requerido.lower(), [rol_requerido])
                for rol_usuario in user_roles:
                    if rol_usuario in nombres_validos:
                        logger.info(f"✅ Acceso concedido: {current_user.usuario} con rol {rol_usuario}")
                        tiene_acceso = True
                        break
                if tiene_acceso:
                    break
            
            if not tiene_acceso:
                logger.warning(f"❌ Acceso denegado: {current_user.usuario} no tiene roles: {required_roles}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"No tiene permisos. Se requiere uno de estos roles: {', '.join(required_roles)}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator



def require_all_permissions(*required_permissions: str):
    """
    Decorador que requiere TODOS los permisos especificados.
    
    IMPORTANTE: El endpoint DEBE incluir:
        current_user: Usuario = Depends(get_current_user)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: Usuario = kwargs.get('current_user')
            
            if not current_user:
                logger.warning("current_user no encontrado en kwargs")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            # Verificar que tenga TODOS los permisos
            permisos_faltantes = []
            for permiso in required_permissions:
                if not tiene_permiso(current_user, permiso):
                    permisos_faltantes.append(permiso)
            
            if permisos_faltantes:
                logger.warning(
                    f"Usuario {current_user.usuario} sin permisos: {', '.join(permisos_faltantes)}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permisos faltantes: {', '.join(permisos_faltantes)}"
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
                    if rol.is_active:
                        roles_usuario.add(rol.nombre.lower())
            
            # Verificar si tiene al menos uno de los roles requeridos
            tiene_rol = any(
                rol.lower() in roles_usuario 
                for rol in required_roles
            )
            
            if not tiene_rol:
                logger.warning(
                    f"Usuario {current_user.usuario} sin rol requerido: {', '.join(required_roles)}"
                )
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
                logger.debug(f"Usuario {current_user.usuario} modificando su propio perfil")
                return await func(*args, **kwargs)
            
            # Si no es el mismo, verificar permiso usando permission_mapper
            if not tiene_permiso(current_user, permission):
                logger.warning(
                    f"Usuario {current_user.usuario} sin permiso para modificar usuario {target_user_id}"
                )
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
    
    ✅ USA permission_mapper para la validación
    """
    if not tiene_permiso(current_user, permiso_requerido):
        logger.warning(
            f"Usuario {current_user.usuario} sin permiso: {permiso_requerido}"
        )
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
                    permisos_usuario.add(permiso.nombre)
    
    return 'editar_usuario' in permisos_usuario or 'admin_usuarios' in permisos_usuario


def validar_puede_modificar_usuario(current_user: Usuario, target_user_id: int):
    """
    Valida si puede modificar usuario, lanza HTTPException si no puede.
    
    ✅ USA permission_mapper.puede_modificar_usuario
    """
    if not puede_modificar_usuario(current_user, target_user_id):
        logger.warning(
            f"Usuario {current_user.usuario} sin permiso para modificar usuario {target_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para modificar este usuario"
        )


def validar_puede_eliminar_usuario(current_user: Usuario, target_user_id: int):
    """
    Valida si puede eliminar usuario, lanza HTTPException si no puede.
    
    ✅ USA permission_mapper.puede_eliminar_usuario
    """
    if not puede_eliminar_usuario(current_user, target_user_id):
        logger.warning(
            f"Usuario {current_user.usuario} sin permiso para eliminar usuario {target_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para eliminar este usuario"
        )


def require_esquela_access(allow_owner: bool = True):
    """
    Decorador para validar acceso a esquelas.
    
    Args:
        allow_owner: Si True, permite al profesor ver sus propias esquelas
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener current_user de los kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No autenticado"
                )
            
            # Importar aquí para evitar circular import
            from app.shared.permission_mapper import puede_ver_todas_esquelas
            
            # Verificar si puede ver todas las esquelas
            if puede_ver_todas_esquelas(current_user):
                return await func(*args, **kwargs)
            
            # Si solo puede ver las propias, verificar que tenga el permiso básico
            if allow_owner:
                if not tiene_permiso(current_user, 'ver_esquela'):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tiene permisos para ver esquelas"
                    )
                # La validación específica se hará en el servicio
                return await func(*args, **kwargs)
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para esta operación"
            )
        
        return wrapper
    return decorator