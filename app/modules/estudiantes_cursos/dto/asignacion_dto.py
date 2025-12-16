"""DTOs para Asignaciones Estudiante-Curso"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ============= DTOs para Asignaciones Individuales =============

class AsignarEstudianteDTO(BaseModel):
    """DTO para asignar un estudiante a un curso"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_curso: int = Field(..., description="ID del curso")

    class Config:
        json_schema_extra = {
            "example": {
                "id_estudiante": 1,
                "id_curso": 5
            }
        }


class AsignacionResponseDTO(BaseModel):
    """DTO de respuesta al asignar/desasignar"""
    mensaje: str
    id_estudiante: int
    id_curso: int
    nombre_estudiante: str
    nombre_curso: str

    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Estudiante asignado exitosamente al curso",
                "id_estudiante": 1,
                "id_curso": 5,
                "nombre_estudiante": "Juan Pérez",
                "nombre_curso": "1ro A"
            }
        }


class EstudianteBasicoAsignacionDTO(BaseModel):
    """DTO básico de estudiante para asignaciones"""
    id_estudiante: int
    ci: Optional[str]
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    estado: str

    class Config:
        from_attributes = True


class CursoBasicoAsignacionDTO(BaseModel):
    """DTO básico de curso para asignaciones"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str

    class Config:
        from_attributes = True


class EstudiantesDeCursoDTO(BaseModel):
    """DTO para listar estudiantes de un curso"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str
    total_estudiantes: int
    estudiantes: List[EstudianteBasicoAsignacionDTO]

    class Config:
        from_attributes = True


class CursosDeEstudianteDTO(BaseModel):
    """DTO para listar cursos de un estudiante"""
    id_estudiante: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    estado: str
    total_cursos: int
    cursos: List[CursoBasicoAsignacionDTO]

    class Config:
        from_attributes = True


# ============= DTOs para Inscripción Masiva =============

class GestionDTO(BaseModel):
    """DTO para lista de gestiones"""
    gestion: str

    class Config:
        from_attributes = True


class GestionesDisponiblesDTO(BaseModel):
    """DTO para listar gestiones disponibles"""
    total: int
    gestiones: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "total": 3,
                "gestiones": ["2025", "2024", "2023"]
            }
        }


class CursoParaInscripcionDTO(BaseModel):
    """DTO de curso para proceso de inscripción"""
    id: int = Field(alias="id_curso")
    nombre: str = Field(alias="nombre_curso")
    nivel_educativo: str = Field(alias="nivel")

    class Config:
        from_attributes = True
        populate_by_name = True


class CursosPorGestionDTO(BaseModel):
    """DTO para listar cursos de una gestión"""
    gestion: str
    total: int
    cursos: List[CursoParaInscripcionDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "gestion": "2025",
                "total": 15,
                "cursos": [
                    {"id": 1, "nombre": "1ro A", "nivel_educativo": "Primaria"},
                    {"id": 2, "nombre": "2do A", "nivel_educativo": "Primaria"}
                ]
            }
        }


class EstudianteParaInscripcionDTO(BaseModel):
    """DTO de estudiante con indicador de inscripción"""
    id_estudiante: int
    ci: Optional[str]
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    ya_inscrito: bool = Field(..., description="Indica si ya está inscrito en la gestión destino")

    class Config:
        from_attributes = True


class EstudiantesParaInscripcionDTO(BaseModel):
    """DTO para listar estudiantes disponibles para inscripción masiva"""
    id_curso_origen: int
    nombre_curso_origen: str
    gestion_origen: str
    gestion_destino: str
    total_estudiantes: int
    estudiantes: List[EstudianteParaInscripcionDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "id_curso_origen": 5,
                "nombre_curso_origen": "1ro A",
                "gestion_origen": "2024",
                "gestion_destino": "2025",
                "total_estudiantes": 25,
                "estudiantes": [
                    {
                        "id_estudiante": 1,
                        "ci": "12345678",
                        "nombres": "Juan",
                        "apellido_paterno": "Pérez",
                        "apellido_materno": "González",
                        "ya_inscrito": False
                    }
                ]
            }
        }


class InscripcionMasivaDTO(BaseModel):
    """DTO para inscribir múltiples estudiantes a un curso"""
    id_curso_destino: int = Field(..., description="ID del curso destino")
    ids_estudiantes: List[int] = Field(..., min_items=1, description="Lista de IDs de estudiantes a inscribir")

    class Config:
        json_schema_extra = {
            "example": {
                "id_curso_destino": 10,
                "ids_estudiantes": [1, 2, 3, 4, 5]
            }
        }


class InscripcionMasivaResponseDTO(BaseModel):
    """DTO de respuesta de inscripción masiva"""
    mensaje: str
    id_curso_destino: int
    nombre_curso_destino: str
    total_procesados: int
    inscritos_exitosamente: int
    ya_inscritos: int

    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Inscripción masiva completada",
                "id_curso_destino": 10,
                "nombre_curso_destino": "2do A - 2025",
                "total_procesados": 25,
                "inscritos_exitosamente": 23,
                "ya_inscritos": 2
            }
        }
