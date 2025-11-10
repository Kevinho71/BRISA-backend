"""
DTOs base compartidos por todos los módulos
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional, List, Any, Dict

class BaseSchema(BaseModel):
    """Schema base con campos comunes"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = True
    
    model_config = {"from_attributes": True}

class PersonaBaseSchema(BaseSchema):
    """Schema base para personas"""
    ci: str = Field(..., min_length=7, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=50)
    apellido_paterno: str = Field(..., min_length=2, max_length=50)
    apellido_materno: str = Field(..., min_length=2, max_length=50)
    direccion: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    tipo_persona: str = Field(..., pattern="^(profesor|administrativo)$")

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

class PaginationSchema(BaseModel):
    """Schema para paginación"""
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)
    sort_by: str = "id"
    sort_order: str = "asc"

class ResponseSchema(BaseModel):
    """Schema para respuestas estandarizadas"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    timestamp: datetime

class PaginatedResponseSchema(ResponseSchema):
    """Schema para respuestas paginadas"""
    pagination: Optional[Dict[str, Any]] = None

class ErrorResponseSchema(BaseModel):
    """Schema para respuestas de error"""
    success: bool = False
    message: str
    errors: List[str] = []
    error_code: Optional[str] = None
    timestamp: datetime
