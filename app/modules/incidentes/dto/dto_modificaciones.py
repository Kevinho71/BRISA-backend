# app/modules/incidentes/dto/dto_modificaciones.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModificacionCreateDTO(BaseModel):
    id_incidente: int
    # ✅ puede ser None para no romper FK si no llega usuario válido
    id_usuario: Optional[int] = None
    campo_modificado: str
    valor_anterior: str | None = None
    valor_nuevo: str | None = None


class ModificacionResponseDTO(BaseModel):
    id_historial: int
    id_incidente: int
    # ✅ puede ser None si tu DB lo permite (si NO lo permite, te digo abajo qué hacer)
    id_usuario: Optional[int] = None
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

    # ✅ NO obligatorio + NO default 0
    id_usuario_modifica: Optional[int] = None

    class Config:
        from_attributes = True
