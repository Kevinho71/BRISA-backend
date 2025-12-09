# app/modules/incidentes/dto/dto_modificaciones.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModificacionCreateDTO(BaseModel):
    id_incidente: int
    id_usuario: int
    campo_modificado: str
    valor_anterior: str | None = None
    valor_nuevo: str | None = None


class ModificacionResponseDTO(BaseModel):
    id_historial: int
    id_incidente: int
    id_usuario: int
    fecha_cambio: datetime
    campo_modificado: str
    valor_anterior: str | None
    valor_nuevo: str | None

    class Config:
        from_attributes = True


class IncidenteUpdateDTO(BaseModel):
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: Optional[str] = None
    id_responsable: Optional[int] = None

    id_usuario_modifica: int

    class Config:
        from_attributes = True
