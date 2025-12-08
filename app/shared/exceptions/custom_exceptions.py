"""
Excepciones personalizadas del sistema BRISA  y sus manejadores
app/shared/exceptions/custom_exceptions     actual
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse


# ==================== EXCEPCIONES ====================

class BRISAException(Exception):
    """Excepción base del sistema BRISA"""
    
    def __init__(self, message, error_code=None, status_code=400):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class ValidationException(BRISAException):
    """Excepción para errores de validación"""
    
    def __init__(self, message, errors=None):
        super().__init__(message, "VALIDATION_ERROR", 400)
        self.errors = errors or []


class NotFound(BRISAException):
    """Excepción para recursos no encontrados"""
    
    def __init__(self, resource_name, resource_id=None):
        message = f"{resource_name} not found"
        if resource_id:
            message += f" with id {resource_id}"
        super().__init__(message, "NOT_FOUND", 404)


class Unauthorized(BRISAException):
    """Excepción para acceso no autorizado"""
    
    def __init__(self, message="Access denied"):
        super().__init__(message, "UNAUTHORIZED", 401)


class Forbidden(BRISAException):
    """Excepción para acceso prohibido"""
    
    def __init__(self, message="Insufficient permissions"):
        super().__init__(message, "FORBIDDEN", 403)


class Conflict(BRISAException):
    """Excepción para conflictos (ej: duplicados)"""
    
    def __init__(self, message="Resource conflict"):
        super().__init__(message, "CONFLICT", 409)


class BusinessLogicException(BRISAException):
    """Excepción para errores de lógica de negocio"""
    
    def __init__(self, message):
        super().__init__(message, "BUSINESS_LOGIC_ERROR", 422)


class DatabaseException(BRISAException):
    """Excepción para errores de base de datos"""
    
    def __init__(self, message="Database operation failed"):
        super().__init__(message, "DATABASE_ERROR", 500)


class ExternalServiceException(BRISAException):
    """Excepción para errores de servicios externos"""
    
    def __init__(self, message="External service error"):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", 502)


class Forbidden(Exception):
    """Excepción para errores de permisos (403 Forbidden)"""
    def __init__(self, message: str = "No tienes permisos para realizar esta acción"):
        self.message = message
        super().__init__(self.message)


# ==================== MANEJADORES DE EXCEPCIONES ====================

async def brisa_exception_handler(request: Request, exc: BRISAException):
    """
    Manejador global para todas las excepciones BRISA
    Convierte las excepciones personalizadas en respuestas JSON apropiadas
    """
    from app.shared.response import ResponseModel
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel.error(
            message=exc.message,
            error_details=exc.error_code,
            status_code=exc.status_code
        )
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Manejador específico para ValidationException con detalles de errores"""
    from app.shared.response import ResponseModel
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ResponseModel.error(
            message=exc.message,
            error_details={"validation_errors": exc.errors},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    )


def register_exception_handlers(app):
    """
    Registra todos los manejadores de excepciones en la aplicación FastAPI
    
    Usage en main.py:
        from app.shared.exceptions.custom_exceptions import register_exception_handlers
        
        app = FastAPI(...)
        register_exception_handlers(app)
    """
    # Registrar manejador genérico para todas las excepciones BRISA
    # Esto captura NotFound, Unauthorized, Forbidden, etc. automáticamente
    app.add_exception_handler(BRISAException, brisa_exception_handler)
    
    # Manejador específico para validaciones (opcional)
    app.add_exception_handler(ValidationException, validation_exception_handler)