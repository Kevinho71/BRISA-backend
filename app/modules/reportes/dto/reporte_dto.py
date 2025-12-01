# app/modules/reportes/dto/reporte_dto.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class RankingItemDTO(BaseModel):
    """DTO para un item del ranking"""
    id: int
    nombre: str
    total: int
    reconocimiento: int = 0
    orientacion: int = 0
    posicion: int


class RankingResponseDTO(BaseModel):
    """DTO para respuesta de ranking"""
    metric: str  # 'student' o 'course'
    type: Optional[str] = None  # 'reconocimiento', 'orientacion' o None (todos)
    limit: int
    data: List[RankingItemDTO]


# ================================
# DTOs para Reportes de Estudiantes
# ================================

class EstudianteReporteDTO(BaseModel):
    """DTO para información básica de estudiante en reportes"""
    id_estudiante: int
    ci: Optional[str]
    nombre_completo: str
    fecha_nacimiento: Optional[date]
    edad: Optional[int]
    cursos: List[str]  # Lista de nombres de cursos


class EstudianteListadoDTO(BaseModel):
    """DTO para listado de estudiantes por curso/nivel/gestión"""
    estudiantes: List[EstudianteReporteDTO]
    total: int
    curso: Optional[str]
    nivel: Optional[str]
    gestion: Optional[str]


class ApoderadoDTO(BaseModel):
    """DTO para datos de apoderado (padre o madre)"""
    tipo: str  # 'padre' o 'madre'
    nombre_completo: Optional[str]
    telefono: Optional[str]


class EstudianteApoderadoDTO(BaseModel):
    """DTO para estudiante con información de apoderados"""
    id_estudiante: int
    ci: Optional[str]
    nombre_completo: str
    apoderados: List[ApoderadoDTO]
    tiene_apoderados: bool


class EstudiantesApoderadosResponseDTO(BaseModel):
    """DTO para respuesta de estudiantes con/sin apoderados"""
    estudiantes: List[EstudianteApoderadoDTO]
    total: int
    con_apoderados: Optional[bool]  # True=con apoderados, False=sin apoderados, None=todos


class ContactoApoderadoDTO(BaseModel):
    """DTO para contacto de apoderado"""
    id_estudiante: int
    estudiante_nombre: str
    estudiante_ci: Optional[str]
    tipo_apoderado: str  # 'padre' o 'madre'
    apoderado_nombre: str
    telefono: str


class ContactosApoderadosResponseDTO(BaseModel):
    """DTO para respuesta de contactos de apoderados"""
    contactos: List[ContactoApoderadoDTO]
    total: int


class DistribucionEdadDTO(BaseModel):
    """DTO para distribución por rango de edad"""
    rango_edad: str  # ej: "5-7 años", "8-10 años"
    cantidad: int
    porcentaje: float


class DistribucionEdadResponseDTO(BaseModel):
    """DTO para respuesta de distribución por edad"""
    distribucion: List[DistribucionEdadDTO]
    total_estudiantes: int


class CursoHistoricoDTO(BaseModel):
    """DTO para curso en historial"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str


class HistorialCursoEstudianteDTO(BaseModel):
    """DTO para historial de cursos de un estudiante"""
    id_estudiante: int
    nombre_completo: str
    ci: Optional[str]
    cursos: List[CursoHistoricoDTO]
    total_cursos: int


class HistorialCursosResponseDTO(BaseModel):
    """DTO para respuesta de historial de cursos"""
    historiales: List[HistorialCursoEstudianteDTO]
    total_estudiantes: int
