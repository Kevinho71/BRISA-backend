from datetime import datetime
import json

def success_response(data=None, message="Success", status_code=200):
    """
    Crear respuesta exitosa estándar
    
    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje descriptivo
        status_code: Código de estado HTTP
    
    Returns:
        tuple: (diccionario_respuesta, codigo_estado)
    """
    response = {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }
    return response, status_code

def error_response(message="Error", status_code=400, errors=None):
    """
    Crear respuesta de error estándar
    
    Args:
        message: Mensaje de error
        status_code: Código de estado HTTP
        errors: Lista de errores específicos
    
    Returns:
        tuple: (diccionario_respuesta, codigo_estado)
    """
    response = {
        'success': False,
        'message': message,
        'errors': errors or [],
        'timestamp': datetime.utcnow().isoformat()
    }
    return response, status_code

def validate_json(required_fields=None):
    """
    Decorador para validar campos requeridos en JSON
    
    Args:
        required_fields: Lista de campos requeridos
    
    Returns:
        function: Decorador
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return error_response("Request must be JSON", 400)
            
            data = request.get_json()
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return error_response(
                        f"Missing required fields: {', '.join(missing_fields)}", 
                        400
                    )
            
            return f(*args, **kwargs)
        
        wrapper.__name__ = f.__name__
        return wrapper
    
    return decorator

def paginate_query(query, page=1, per_page=10):
    """
    Paginar resultados de query
    
    Args:
        query: Query de SQLAlchemy
        page: Número de página
        per_page: Elementos por página
    
    Returns:
        dict: Datos paginados con metadatos
    """
    pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }