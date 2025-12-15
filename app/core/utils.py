# app\core\utils.py
from datetime import datetime
from typing import Any, Dict, Optional, List

def success_response(data: Any = None, message: str = "Success") -> Dict:
    """
    Crear respuesta exitosa estándar para FastAPI
    
    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje descriptivo
    
    Returns:
        dict: Diccionario con la respuesta estructurada
    """
    response = {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }
    return response

def error_response(message: str = "Error", errors: Optional[List] = None) -> Dict:
    """
    Crear respuesta de error estándar para FastAPI
    
    Args:
        message: Mensaje de error
        errors: Lista de errores específicos
    
    Returns:
        dict: Diccionario con la respuesta de error estructurada
    """
    response = {
        'success': False,
        'message': message,
        'errors': errors or [],
        'timestamp': datetime.utcnow().isoformat()
    }
    return response

def paginated_response(data: List, total: int, page: int, page_size: int, message: str = "Success") -> Dict:
    """
    Crear respuesta paginada estándar
    
    Args:
        data: Lista de datos
        total: Total de registros
        page: Página actual
        page_size: Tamaño de página
        message: Mensaje descriptivo
    
    Returns:
        dict: Diccionario con respuesta paginada
    """
    total_pages = (total + page_size - 1) // page_size
    response = {
        'success': True,
        'message': message,
        'data': data,
        'pagination': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    return response