# app\modules\incidentes\dto\dto_detalles.py

from pydantic import BaseModel
from datetime import datetime
from typing import List


class EstudianteItem(BaseModel):
    id_estudiante: int

    class Config:
        from_attributes = True


class ProfesorItem(BaseModel):
    id_persona: int

    class Config:
        from_attributes = True


class SituacionItem(BaseModel):
    id_situacion: int

    class Config:
        from_attributes = True


class IncidenteDetalles(BaseModel):
    id_incidente: int
    fecha: datetime
    antecedentes: str | None
    acciones_tomadas: str | None
    seguimiento: str | None
    estado: str
    id_responsable: int | None

    estudiantes: List[EstudianteItem]
    profesores: List[ProfesorItem]
    situaciones: List[SituacionItem]

    class Config:
        from_attributes = True
