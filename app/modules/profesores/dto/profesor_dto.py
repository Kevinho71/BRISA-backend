# app/modules/profesores/dtos/profesor_dto.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from enum import Enum


class NivelEnsenanzaEnum(str, Enum):
    """Enumeración para niveles de enseñanza"""
    foundation = "foundation"
    primary = "primary"
    secondary = "secondary"
    todos = "todos"


class EstadoLaboralEnum(str, Enum):
    """Estados laborales"""
    activo = "activo"
    retirado = "retirado"
    licencia = "licencia"
    suspendido = "suspendido"


class ProfesorCreateDTO(BaseModel):
    """DTO para crear un profesor"""
    # Datos de Persona
    ci: str = Field(..., min_length=5, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=100)
    apellido_paterno: str = Field(..., min_length=2, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=120)
    id_cargo: Optional[int] = None
    estado_laboral: Optional[EstadoLaboralEnum] = EstadoLaboralEnum.activo
    anos_experiencia: Optional[int] = Field(0, ge=0)
    fecha_ingreso: Optional[date] = None
    
    # Datos específicos de Profesor
    especialidad: Optional[str] = Field(None, max_length=100)
    titulo_academico: Optional[str] = Field(None, max_length=100)
    nivel_enseñanza: Optional[NivelEnsenanzaEnum] = NivelEnsenanzaEnum.todos
    observaciones: Optional[str] = None

    @validator('correo')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Correo electrónico inválido')
        return v

    class Config:
        from_attributes = True


class ProfesorUpdateDTO(BaseModel):
    """DTO para actualizar un profesor"""
    # Datos de Persona (todos opcionales para actualización)
    ci: Optional[str] = Field(None, min_length=5, max_length=20)
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido_paterno: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=120)
    id_cargo: Optional[int] = None
    estado_laboral: Optional[EstadoLaboralEnum] = None
    anos_experiencia: Optional[int] = Field(None, ge=0)
    fecha_ingreso: Optional[date] = None
    fecha_retiro: Optional[date] = None
    motivo_retiro: Optional[str] = None
    is_active: Optional[bool] = None
    
    # Datos específicos de Profesor
    especialidad: Optional[str] = Field(None, max_length=100)
    titulo_academico: Optional[str] = Field(None, max_length=100)
    nivel_enseñanza: Optional[NivelEnsenanzaEnum] = None
    observaciones: Optional[str] = None

    @validator('correo')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Correo electrónico inválido')
        return v

    class Config:
        from_attributes = True


class ProfesorResponseDTO(BaseModel):
    """DTO para respuesta de profesor"""
    id_profesor: int
    id_persona: int
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    direccion: Optional[str]
    telefono: Optional[str]
    correo: Optional[str]
    id_cargo: Optional[int]
    estado_laboral: Optional[str]
    anos_experiencia: Optional[int]
    fecha_ingreso: Optional[date]
    fecha_retiro: Optional[date]
    motivo_retiro: Optional[str]
    is_active: bool
    especialidad: Optional[str]
    titulo_academico: Optional[str]
    nivel_enseñanza: Optional[str]
    observaciones: Optional[str]

    class Config:
        from_attributes = True


class AsignarCursoMateriaDTO(BaseModel):
    """DTO para asignar curso y materia a profesor"""
    id_profesor: int
    id_curso: int
    id_materia: int

    class Config:
        from_attributes = True


class ProfesorCursoMateriaResponseDTO(BaseModel):
    """DTO para respuesta de asignación profesor-curso-materia"""
    id_profesor: int
    id_curso: int
    id_materia: int
    nombre_profesor: str
    nombre_curso: str
    nombre_materia: str

    class Config:
        from_attributes = True