"""
Decoradores compartidos para el sistema BRISA
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.core.utils import error_response
from app.shared.exceptions.custom_exceptions import Unauthorized, Forbidden, ValidationException

def require_permissions(*permissions):
    """
    Decorador para requerir permisos específicos
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            
            # TODO: Implementar verificación de permisos
            # user_permissions = get_user_permissions(current_user_id)
            # 
            # for permission in permissions:
            #     if permission not in user_permissions:
            #         raise Forbidden(f"Permission required: {permission}")
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_roles(*roles):
    """
    Decorador para requerir roles específicos
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            
            # TODO: Implementar verificación de roles
            # user_roles = get_user_roles(current_user_id)
            # 
            # if not any(role in user_roles for role in roles):
            #     raise Forbidden(f"Role required: {' or '.join(roles)}")
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def validate_json_schema(schema_class):
    """
    Decorador para validar JSON con schema de marshmallow
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return error_response("Request must be JSON", 400)
            
            try:
                schema = schema_class()
                data = schema.load(request.get_json())
                request.validated_data = data
            except Exception as e:
                return error_response("Validation failed", 400, [str(e)])
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def validate_query_params(schema_class):
    """
    Decorador para validar parámetros de query
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema = schema_class()
                data = schema.load(request.args.to_dict())
                request.validated_params = data
            except Exception as e:
                return error_response("Invalid query parameters", 400, [str(e)])
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def handle_exceptions(f):
    """
    Decorador para manejar excepciones automáticamente
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationException as e:
            return error_response(e.message, e.status_code, e.errors)
        except (Unauthorized, Forbidden) as e:
            return error_response(e.message, e.status_code)
        except Exception as e:
            # Log del error en producción
            return error_response("Internal server error", 500)
    
    return decorated_function

def log_activity(action_type):
    """
    Decorador para registrar actividad del usuario
    """
    def decorator(f):
        @wraps(f)
        @jwt_required(optional=True)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            
            # Ejecutar función
            result = f(*args, **kwargs)
            
            # TODO: Implementar logging de actividad
            # log_user_activity(user_id, action_type, request.endpoint, request.method)
            
            return result
        
        return decorated_function
    return decorator

def rate_limit(max_requests=100, window_minutes=60):
    """
    Decorador para limitar tasa de requests (básico)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO: Implementar rate limiting real con Redis
            # client_ip = request.remote_addr
            # if is_rate_limited(client_ip, max_requests, window_minutes):
            #     return error_response("Rate limit exceeded", 429)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator