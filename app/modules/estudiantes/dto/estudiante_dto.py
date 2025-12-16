"""DTOs para Estudiantes"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date
from enum import Enum


class EstadoEstudiante(str, Enum):
    """Estados válidos para un estudiante"""
    ACTIVO = "Activo"
    RETIRADO = "Retirado"
    ABANDONO = "Abandono"


# ============= DTOs Base =============

class EstudianteCreateDTO(BaseModel):
    """DTO para crear un estudiante"""
    nombres: str = Field(..., min_length=1, max_length=100, description="Nombres del estudiante")
    apellido_paterno: str = Field(..., min_length=1, max_length=100, description="Apellido paterno del estudiante")
    apellido_materno: Optional[str] = Field(None, max_length=100, description="Apellido materno del estudiante")
    ci: Optional[str] = Field(None, max_length=20, description="Cédula de identidad")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    direccion: Optional[str] = Field(None, description="Dirección del estudiante")
    estado: EstadoEstudiante = Field(default=EstadoEstudiante.ACTIVO, description="Estado del estudiante")
    
    # Información del padre
    nombre_padre: Optional[str] = Field(None, max_length=100, description="Nombre del padre")
    apellido_paterno_padre: Optional[str] = Field(None, max_length=100, description="Apellido paterno del padre")
    apellido_materno_padre: Optional[str] = Field(None, max_length=100, description="Apellido materno del padre")
    telefono_padre: Optional[str] = Field(None, max_length=15, description="Teléfono del padre")
    
    # Información de la madre
    nombre_madre: Optional[str] = Field(None, max_length=100, description="Nombre de la madre")
    apellido_paterno_madre: Optional[str] = Field(None, max_length=100, description="Apellido paterno de la madre")
    apellido_materno_madre: Optional[str] = Field(None, max_length=100, description="Apellido materno de la madre")
    telefono_madre: Optional[str] = Field(None, max_length=15, description="Teléfono de la madre")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombres": "Juan Carlos",
                "apellido_paterno": "Pérez",
                "apellido_materno": "González",
                "ci": "12345678",
                "fecha_nacimiento": "2010-05-15",
                "direccion": "Av. Principal #123",
                "estado": "Activo",
                "nombre_padre": "Carlos",
                "apellido_paterno_padre": "Pérez",
                "telefono_padre": "70123456",
                "nombre_madre": "María",
                "apellido_paterno_madre": "González",
                "telefono_madre": "70654321"
            }
        }


class EstudianteUpdateDTO(BaseModel):
    """DTO para actualizar un estudiante - todos los campos opcionales"""
    nombres: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido_paterno: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    ci: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    estado: Optional[EstadoEstudiante] = None
    
    # Información del padre
    nombre_padre: Optional[str] = Field(None, max_length=100)
    apellido_paterno_padre: Optional[str] = Field(None, max_length=100)
    apellido_materno_padre: Optional[str] = Field(None, max_length=100)
    telefono_padre: Optional[str] = Field(None, max_length=15)
    
    # Información de la madre
    nombre_madre: Optional[str] = Field(None, max_length=100)
    apellido_paterno_madre: Optional[str] = Field(None, max_length=100)
    apellido_materno_madre: Optional[str] = Field(None, max_length=100)
    telefono_madre: Optional[str] = Field(None, max_length=15)

    class Config:
        from_attributes = True


class CursoBasicoDTO(BaseModel):
    """DTO básico de curso para incluir en respuestas de estudiante"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str

    class Config:
        from_attributes = True


class EstudianteResponseDTO(BaseModel):
    """DTO para respuesta de estudiante con información completa"""
    id_estudiante: int
    ci: Optional[str]
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    estado: str
    
    # Información del padre
    nombre_padre: Optional[str]
    apellido_paterno_padre: Optional[str]
    apellido_materno_padre: Optional[str]
    telefono_padre: Optional[str]
    
    # Información de la madre
    nombre_madre: Optional[str]
    apellido_paterno_madre: Optional[str]
    apellido_materno_madre: Optional[str]
    telefono_madre: Optional[str]
    
    # Cursos asignados
    cursos: List[CursoBasicoDTO] = []

    class Config:
        from_attributes = True


class EstudianteListDTO(BaseModel):
    """DTO para lista de estudiantes con paginación"""
    total: int
    estudiantes: List[EstudianteResponseDTO]

    class Config:
        from_attributes = True


# ============= DTOs de Estados =============

class CambiarEstadoDTO(BaseModel):
    """DTO para cambiar el estado de un estudiante"""
    nuevo_estado: EstadoEstudiante = Field(..., description="Nuevo estado del estudiante")

    class Config:
        json_schema_extra = {
            "example": {
                "nuevo_estado": "Retirado"
            }
        }


class CambiarEstadoResponseDTO(BaseModel):
    """DTO de respuesta al cambiar estado"""
    mensaje: str
    id_estudiante: int
    estado_anterior: str
    estado_nuevo: str
    nombre_estudiante: str

    class Config:
        from_attributes = True


# ============= DTOs de Importación/Exportación =============

class EstudianteImportDTO(BaseModel):
    """DTO para importar estudiantes desde Excel"""
    ci: str = Field(..., description="Cédula de identidad (requerida para identificar duplicados)")
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    estado: Optional[str] = "Activo"
    nombre_padre: Optional[str] = None
    apellido_paterno_padre: Optional[str] = None
    apellido_materno_padre: Optional[str] = None
    telefono_padre: Optional[str] = None
    nombre_madre: Optional[str] = None
    apellido_paterno_madre: Optional[str] = None
    apellido_materno_madre: Optional[str] = None
    telefono_madre: Optional[str] = None


class ImportResultDTO(BaseModel):
    """DTO con el resultado de la importación"""
    total_procesados: int
    creados: int
    actualizados: int
    errores: int
    errores_detalle: List[str] = []
    mensaje: str

    class Config:
        json_schema_extra = {
            "example": {
                "total_procesados": 50,
                "creados": 30,
                "actualizados": 15,
                "errores": 5,
                "errores_detalle": [
                    "Fila 10: CI no proporcionado",
                    "Fila 25: Nombres no proporcionado"
                ],
                "mensaje": "Importación completada: 30 creados, 15 actualizados, 5 errores"
            }
        }
