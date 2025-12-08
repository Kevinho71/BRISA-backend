# Excepciones personalizadas
from fastapi import HTTPException, status

class Unauthorized(HTTPException):
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class NotFound(HTTPException):
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} con ID {resource_id} no encontrado"
        )
