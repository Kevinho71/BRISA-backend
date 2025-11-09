"""
app/shared/responses.py
Modelo de respuesta estándar para toda la API
Compatible con tests de seguridad
"""
from typing import Any, Optional, List


class ResponseModel:
    """Modelo de respuesta estándar para toda la API"""
    
    @staticmethod
    def success(
        message: str, 
        data: Any = None, 
        status_code: int = 200
    ) -> dict:
        """
        Respuesta exitosa
        
        Args:
            message: Mensaje descriptivo
            data: Datos a devolver (puede ser dict, list, etc.)
            status_code: Código HTTP (para FastAPI, no se incluye en body)
        
        Returns:
            dict: {"success": True, "message": "...", "data": {...}}
        """
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(
        message: str, 
        error_details: Optional[str] = None,
        errors: Optional[List[str]] = None,
        status_code: int = 400
    ) -> dict:
        """
        Respuesta con error
        
        Args:
            message: Mensaje de error principal
            error_details: Detalles específicos del error (string único)
            errors: Lista de errores (alternativa a error_details)
            status_code: Código HTTP
        
        Returns:
            dict: {"success": False, "message": "...", "errors": [...]}
        """
        response = {
            "success": False,
            "message": message
        }
        
        # Manejar errores como lista
        if errors:
            response["errors"] = errors
        elif error_details:
            response["errors"] = [error_details]
        
        return response
    
    @staticmethod
    def paginated(
        message: str,
        items: List[Any],
        total: int,
        page: int = 1,
        per_page: int = 50
    ) -> dict:
        """
        Respuesta paginada
        
        Args:
            message: Mensaje descriptivo
            items: Lista de items de la página actual
            total: Total de registros
            page: Número de página actual
            per_page: Items por página
        
        Returns:
            dict con estructura paginada
        """
        import math
        pages = math.ceil(total / per_page) if per_page > 0 else 0
        
        return {
            "success": True,
            "message": message,
            "data": items,
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages
            }
        }


# Alias para compatibilidad con código existente
class StandardResponse:
    """Alias para mantener compatibilidad"""
    
    @staticmethod
    def success(message: str, data: Any = None) -> dict:
        return ResponseModel.success(message, data)
    
    @staticmethod
    def error(message: str, errors: Optional[List[str]] = None) -> dict:
        return ResponseModel.error(message, errors=errors)