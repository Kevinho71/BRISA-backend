# app\modules\incidentes\dto\dto_incidentes.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class IncidenteCreateDTO(BaseModel):
    fecha: datetime
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: str
    id_responsable: Optional[int] = None

    estudiantes: List[int] = []
    profesores: List[int] = []
    situaciones: List[int] = []

class IncidenteResponseDTO(BaseModel):
    id_incidente: int
    fecha: datetime
    antecedentes: Optional[str]
    acciones_tomadas: Optional[str]
    seguimiento: Optional[str]
    estado: str
    id_responsable: Optional[int]
    responsable_usuario: Optional[str] = None

    class Config:
        from_attributes = True
