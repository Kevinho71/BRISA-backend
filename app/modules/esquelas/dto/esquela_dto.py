# app/modules/esquelas/dto/esquela_dto.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import List, Optional


class CodigoEsquelaDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_codigo: int
    tipo: str
    codigo: str
    descripcion: str


class EstudianteSimpleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_estudiante: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    ci: Optional[str] = None
    
    @property
    def nombre_completo(self) -> str:
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


class ProfesorSimpleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_persona: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    
    @property
    def nombre_completo(self) -> str:
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


class CursoSimpleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str


class EsquelaBaseDTO(BaseModel):
    # Campos requeridos según la base de datos
    id_estudiante: int
    id_profesor: int
    id_registrador: int
    fecha: date
    observaciones: Optional[str] = None
    codigos: List[int]  # Lista de IDs de códigos


class EsquelaResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_esquela: int
    fecha: date
    observaciones: Optional[str]
    estudiante: Optional[EstudianteSimpleDTO] = None
    profesor: Optional[ProfesorSimpleDTO] = None
    # NOTA: No incluimos curso directamente porque no existe id_curso en esquelas
    codigos: List[CodigoEsquelaDTO]


class EsquelaListResponseDTO(BaseModel):
    """DTO para respuesta paginada de esquelas"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[EsquelaResponseDTO]


class EsquelasAggregateByCourseDTO(BaseModel):
    """DTO para agregación de esquelas por curso"""
    curso_id: int
    curso: str
    reconocimiento: int = 0
    orientacion: int = 0
    
    @property
    def resumen(self) -> str:
        """Formato: 5R, 2O"""
        return f"{self.reconocimiento}R, {self.orientacion}O"


class EstudianteEsquelasDTO(BaseModel):
    """DTO para esquelas de un estudiante con resumen"""
    total: int
    esquelas: List[EsquelaResponseDTO]
    codigos_resumen: dict = Field(default_factory=dict)


class EsquelaAggregateByYearDTO(BaseModel):
    """DTO para agregación por año"""
    year: int
    total: int


class EsquelaAggregateByMonthDTO(BaseModel):
    """DTO para agregación por año y mes"""
    year: int
    month: int
    total: int

