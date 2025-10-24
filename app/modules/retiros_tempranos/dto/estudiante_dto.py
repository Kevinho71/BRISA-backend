from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EstudianteCreateDTO(BaseModel):
    """DTO para crear un estudiante"""
    ci: str = Field(..., min_length=1, max_length=255, description="Cédula de identidad del estudiante")
    nombres: str = Field(..., min_length=1, max_length=255, description="Nombres del estudiante")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    telefono_contacto: Optional[str] = Field(None, max_length=255, description="Teléfono de contacto")


class EstudianteUpdateDTO(BaseModel):
    """DTO para actualizar un estudiante"""
    ci: Optional[str] = Field(None, min_length=1, max_length=255, description="Cédula de identidad del estudiante")
    nombres: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombres del estudiante")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    telefono_contacto: Optional[str] = Field(None, max_length=255, description="Teléfono de contacto")


class EstudianteResponseDTO(BaseModel):
    """DTO para respuesta de estudiante"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    ci: str = Field(..., description="Cédula de identidad")
    nombres: str = Field(..., description="Nombres del estudiante")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    telefono_contacto: Optional[str] = Field(None, description="Teléfono de contacto")
    
    class Config:
        from_attributes = True
