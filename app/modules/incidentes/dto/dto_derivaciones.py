# app\modules\incidentes\dto\dto_derivaciones.py
from pydantic import BaseModel
from datetime import datetime

class DerivacionCreate(BaseModel):
    id_quien_deriva: int
    id_quien_recibe: int
    observaciones: str | None = None

class DerivacionRead(BaseModel):
    id_derivacion: int
    id_incidente: int
    id_quien_deriva: int
    id_quien_recibe: int
    fecha_derivacion: datetime
    observaciones: str | None

    class Config:
        orm_mode = True
