from typing import Any, Optional

class ResponseModel:
    """Modelo de respuesta estándar para toda la API"""
    
    @staticmethod
    def success(message: str, data: Any = None, status_code: int = 200) -> dict:
        """Respuesta exitosa"""
        return {
            "status": "success",
            "message": message,
            "data": data,
            "status_code": status_code
        }
    
    @staticmethod
    def error(message: str, error_details: Optional[str] = None, status_code: int = 400) -> dict:
        """Respuesta con error"""
        response = {
            "status": "error",
            "message": message,
            "status_code": status_code
        }
        if error_details:
            response["error_details"] = error_details
        return response
