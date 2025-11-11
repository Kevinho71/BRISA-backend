from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ApoderadoCreateDTO(BaseModel):
    """DTO para crear un apoderado"""
    ci: str = Field(..., min_length=1, max_length=20, description="Cédula de identidad única del apoderado")
    nombres: str = Field(..., min_length=1, max_length=100, description="Nombres del apoderado")
    apellidos: str = Field(..., min_length=1, max_length=100, description="Apellidos del apoderado")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    correo: Optional[EmailStr] = Field(None, description="Correo electrónico")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección")


class ApoderadoUpdateDTO(BaseModel):
    """DTO para actualizar un apoderado"""
    ci: Optional[str] = Field(None, min_length=1, max_length=20, description="Cédula de identidad del apoderado")
    nombres: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombres del apoderado")
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100, description="Apellidos del apoderado")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    correo: Optional[EmailStr] = Field(None, description="Correo electrónico")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección")


class ApoderadoResponseDTO(BaseModel):
    """DTO para respuesta de apoderado"""
    id_apoderado: int = Field(..., description="ID del apoderado")
    ci: str = Field(..., description="Cédula de identidad")
    nombres: str = Field(..., description="Nombres del apoderado")
    apellidos: str = Field(..., description="Apellidos del apoderado")
    telefono: Optional[str] = Field(None, description="Teléfono de contacto")
    correo: Optional[str] = Field(None, description="Correo electrónico")
    direccion: Optional[str] = Field(None, description="Dirección")
    
    class Config:
        from_attributes = True
