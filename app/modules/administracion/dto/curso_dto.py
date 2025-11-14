# app/modules/administracion/dto/curso_dto.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CursoDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_curso: int
    nombre_curso: str
    nivel: str
    gestion: str


class EstudianteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_estudiante: int
    ci: Optional[str] = None
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    
    @property
    def nombre_completo(self) -> str:
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


class ProfesorDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_persona: int
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    
    @property
    def nombre_completo(self) -> str:
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


class EstudianteListResponseDTO(BaseModel):
    """DTO para respuesta paginada de estudiantes"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[EstudianteDTO]


class ProfesorListResponseDTO(BaseModel):
    """DTO para respuesta paginada de profesores"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[ProfesorDTO]
