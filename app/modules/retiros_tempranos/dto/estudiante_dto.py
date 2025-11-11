from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EstudianteCreateDTO(BaseModel):
    """DTO para crear un estudiante"""
    ci: Optional[str] = Field(None, max_length=20, description="Cédula de identidad del estudiante")
    nombres: str = Field(..., min_length=1, max_length=50, description="Nombres del estudiante")
    apellido_paterno: str = Field(..., min_length=1, max_length=50, description="Apellido paterno")
    apellido_materno: str = Field(..., min_length=1, max_length=50, description="Apellido materno")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección")
    nombre_padre: Optional[str] = Field(None, max_length=50, description="Nombre del padre")
    apellido_paterno_padre: Optional[str] = Field(None, max_length=50, description="Apellido paterno del padre")
    apellido_materno_padre: Optional[str] = Field(None, max_length=50, description="Apellido materno del padre")
    telefono_padre: Optional[str] = Field(None, max_length=20, description="Teléfono del padre")
    nombre_madre: Optional[str] = Field(None, max_length=50, description="Nombre de la madre")
    apellido_paterno_madre: Optional[str] = Field(None, max_length=50, description="Apellido paterno de la madre")
    apellido_materno_madre: Optional[str] = Field(None, max_length=50, description="Apellido materno de la madre")
    telefono_madre: Optional[str] = Field(None, max_length=20, description="Teléfono de la madre")


class EstudianteUpdateDTO(BaseModel):
    """DTO para actualizar un estudiante"""
    ci: Optional[str] = Field(None, max_length=20, description="Cédula de identidad del estudiante")
    nombres: Optional[str] = Field(None, min_length=1, max_length=50, description="Nombres del estudiante")
    apellido_paterno: Optional[str] = Field(None, min_length=1, max_length=50, description="Apellido paterno")
    apellido_materno: Optional[str] = Field(None, min_length=1, max_length=50, description="Apellido materno")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección")
    nombre_padre: Optional[str] = Field(None, max_length=50, description="Nombre del padre")
    apellido_paterno_padre: Optional[str] = Field(None, max_length=50, description="Apellido paterno del padre")
    apellido_materno_padre: Optional[str] = Field(None, max_length=50, description="Apellido materno del padre")
    telefono_padre: Optional[str] = Field(None, max_length=20, description="Teléfono del padre")
    nombre_madre: Optional[str] = Field(None, max_length=50, description="Nombre de la madre")
    apellido_paterno_madre: Optional[str] = Field(None, max_length=50, description="Apellido paterno de la madre")
    apellido_materno_madre: Optional[str] = Field(None, max_length=50, description="Apellido materno de la madre")
    telefono_madre: Optional[str] = Field(None, max_length=20, description="Teléfono de la madre")


class EstudianteResponseDTO(BaseModel):
    """DTO para respuesta de estudiante"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    ci: Optional[str] = Field(None, description="Cédula de identidad")
    nombres: str = Field(..., description="Nombres del estudiante")
    apellido_paterno: str = Field(..., description="Apellido paterno")
    apellido_materno: str = Field(..., description="Apellido materno")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    direccion: Optional[str] = Field(None, description="Dirección")
    nombre_padre: Optional[str] = Field(None, description="Nombre del padre")
    apellido_paterno_padre: Optional[str] = Field(None, description="Apellido paterno del padre")
    apellido_materno_padre: Optional[str] = Field(None, description="Apellido materno del padre")
    telefono_padre: Optional[str] = Field(None, description="Teléfono del padre")
    nombre_madre: Optional[str] = Field(None, description="Nombre de la madre")
    apellido_paterno_madre: Optional[str] = Field(None, description="Apellido paterno de la madre")
    apellido_materno_madre: Optional[str] = Field(None, description="Apellido materno de la madre")
    telefono_madre: Optional[str] = Field(None, description="Teléfono de la madre")
    
    class Config:
        from_attributes = True
