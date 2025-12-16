"""DTOs para Cursos"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum


class NivelEducativo(str, Enum):
    """Niveles educativos válidos"""
    INICIAL = "Inicial"
    PRIMARIA = "Primaria"
    SECUNDARIA = "Secundaria"


# ============= DTOs Base =============

class CursoCreateDTO(BaseModel):
    """DTO para crear un curso"""
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del curso (ej: '1ro A', 'Kinder Mañana')")
    nivel_educativo: NivelEducativo = Field(..., description="Nivel educativo: Inicial, Primaria, Secundaria")
    gestion: str = Field(..., min_length=4, max_length=20, description="Gestión o año académico (ej: '2025', '2025-1')")
    capacidad_maxima: Optional[int] = Field(30, ge=1, le=100, description="Capacidad máxima de estudiantes")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombre": "1ro A",
                "nivel_educativo": "Primaria",
                "gestion": "2025",
                "capacidad_maxima": 30
            }
        }


class CursoUpdateDTO(BaseModel):
    """DTO para actualizar un curso - todos los campos opcionales"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    nivel_educativo: Optional[NivelEducativo] = None
    gestion: Optional[str] = Field(None, min_length=4, max_length=20)
    capacidad_maxima: Optional[int] = Field(None, ge=1, le=100)

    class Config:
        from_attributes = True


class EstudianteBasicoDTO(BaseModel):
    """DTO básico de estudiante para incluir en respuestas de curso"""
    id_estudiante: int
    ci: Optional[str]
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    estado: str

    class Config:
        from_attributes = True


class CursoResponseDTO(BaseModel):
    """DTO para respuesta de curso con información completa"""
    id: int
    nombre: str
    nivel_educativo: str
    gestion: str
    capacidad_maxima: Optional[int] = 30
    estudiantes: List[EstudianteBasicoDTO] = []

    class Config:
        from_attributes = True


class CursoListDTO(BaseModel):
    """DTO para lista de cursos con paginación"""
    total: int
    cursos: List[CursoResponseDTO]

    class Config:
        from_attributes = True


# ============= DTOs para Copia de Gestiones =============

class CopiarGestionDTO(BaseModel):
    """DTO para copiar cursos entre gestiones"""
    gestion_origen: str = Field(..., description="Gestión de origen (ej: '2024')")
    gestion_destino: str = Field(..., description="Gestión de destino (ej: '2025')")

    class Config:
        json_schema_extra = {
            "example": {
                "gestion_origen": "2024",
                "gestion_destino": "2025"
            }
        }


class CopiarGestionResponseDTO(BaseModel):
    """DTO de respuesta al copiar gestión"""
    mensaje: str
    gestion_origen: str
    gestion_destino: str
    cursos_copiados: int

    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Se copiaron 15 cursos de la gestión 2024 a 2025",
                "gestion_origen": "2024",
                "gestion_destino": "2025",
                "cursos_copiados": 15
            }
        }
