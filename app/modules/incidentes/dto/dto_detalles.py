from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class EstudianteItem(BaseModel):
    id_estudiante: int
    nombre: str  # "Nombres Apellidos"

    class Config:
        from_attributes = True


class ProfesorItem(BaseModel):
    id_persona: int
    nombre: str  # "Nombres Apellidos"

    class Config:
        from_attributes = True


class SituacionItem(BaseModel):
    id_situacion: int
    nombre_situacion: str
    nivel_gravedad: str

    class Config:
        from_attributes = True


class IncidenteDetalles(BaseModel):
    id_incidente: int
    fecha: datetime
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: str
    id_responsable: Optional[int] = None

    estudiantes: List[EstudianteItem]
    profesores: List[ProfesorItem]
    situaciones: List[SituacionItem]

    class Config:
        from_attributes = True
