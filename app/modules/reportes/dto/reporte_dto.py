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


# ================================
# DTOs para Reportes Académicos
# ================================

class MateriaDTO(BaseModel):
    """DTO para información de materia"""
    id_materia: int
    nombre_materia: str
    nivel: str


class CursoAcademicoDTO(BaseModel):
    """DTO para información de curso"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str


class ProfesorAsignadoDTO(BaseModel):
    """DTO para profesor con sus asignaciones"""
    id_profesor: int
    ci: str
    nombre_completo: str
    telefono: Optional[str]
    correo: Optional[str]
    curso: str
    materia: str


class ProfesoresAsignadosResponseDTO(BaseModel):
    """DTO para respuesta de profesores asignados"""
    profesores: List[ProfesorAsignadoDTO]
    total: int
    curso: Optional[str]
    materia: Optional[str]


class MateriaPorNivelDTO(BaseModel):
    """DTO para materia por nivel educativo"""
    id_materia: int
    nombre_materia: str
    nivel: str


class MateriasPorNivelResponseDTO(BaseModel):
    """DTO para respuesta de materias por nivel"""
    materias: List[MateriaPorNivelDTO]
    total: int
    nivel: Optional[str]


class AsignacionProfesorDTO(BaseModel):
    """DTO para una asignación de profesor"""
    curso: str
    nivel: str
    gestion: str
    materia: str


class CargaAcademicaProfesorDTO(BaseModel):
    """DTO para carga académica de un profesor"""
    id_profesor: int
    ci: str
    nombre_completo: str
    telefono: Optional[str]
    correo: Optional[str]
    asignaciones: List[AsignacionProfesorDTO]
    total_asignaciones: int
    cursos_distintos: int
    materias_distintas: int


class CargaAcademicaResponseDTO(BaseModel):
    """DTO para respuesta de carga académica"""
    profesores: List[CargaAcademicaProfesorDTO]
    total_profesores: int


class CursoPorGestionDTO(BaseModel):
    """DTO para curso por gestión"""
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str
    total_estudiantes: int


class CursosPorGestionResponseDTO(BaseModel):
    """DTO para respuesta de cursos por gestión"""
    cursos: List[CursoPorGestionDTO]
    total: int
    gestion: Optional[str]
    nivel: Optional[str]
