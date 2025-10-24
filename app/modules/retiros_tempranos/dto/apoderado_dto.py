from pydantic import BaseModel, Field
from typing import Optional


class ApoderadoCreateDTO(BaseModel):
    """DTO para crear un apoderado"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    parentesco: str = Field(..., min_length=1, max_length=255, description="Relación de parentesco")
    nombres: str = Field(..., min_length=1, max_length=255, description="Nombres del apoderado")
    apellidos: str = Field(..., min_length=1, max_length=255, description="Apellidos del apoderado")
    ci: str = Field(..., min_length=1, max_length=255, description="Cédula de identidad del apoderado")
    telefono: str = Field(..., min_length=1, max_length=255, description="Teléfono de contacto")


class ApoderadoUpdateDTO(BaseModel):
    """DTO para actualizar un apoderado"""
    parentesco: Optional[str] = Field(None, min_length=1, max_length=255, description="Relación de parentesco")
    nombres: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombres del apoderado")
    apellidos: Optional[str] = Field(None, min_length=1, max_length=255, description="Apellidos del apoderado")
    ci: Optional[str] = Field(None, min_length=1, max_length=255, description="Cédula de identidad del apoderado")
    telefono: Optional[str] = Field(None, min_length=1, max_length=255, description="Teléfono de contacto")


class ApoderadoResponseDTO(BaseModel):
    """DTO para respuesta de apoderado"""
    id_apoderado: int = Field(..., description="ID del apoderado")
    id_estudiante: int = Field(..., description="ID del estudiante")
    parentesco: str = Field(..., description="Relación de parentesco")
    nombres: str = Field(..., description="Nombres del apoderado")
    apellidos: str = Field(..., description="Apellidos del apoderado")
    ci: str = Field(..., description="Cédula de identidad")
    telefono: str = Field(..., description="Teléfono de contacto")
    
    class Config:
        from_attributes = True
