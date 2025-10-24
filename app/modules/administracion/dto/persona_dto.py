# app/modules/administracion/dto/persona_dto.py
"""DTOs para estudiantes, profesores y registradores"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class EstudianteResponseDTO(BaseModel):
    """DTO para respuesta de estudiante"""
    model_config = ConfigDict(from_attributes=True)
    
    id_estudiante: int
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    nombre_completo: str


class PersonaResponseDTO(BaseModel):
    """DTO para respuesta de persona (profesor o administrativo)"""
    model_config = ConfigDict(from_attributes=True)
    
    id_persona: int
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    tipo_persona: str
    nombre_completo: str
