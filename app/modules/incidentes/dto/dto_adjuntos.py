# app\modules\incidentes\dto\dto_adjuntos.py
from pydantic import BaseModel
from datetime import datetime

class AdjuntoRead(BaseModel):
    id_adjunto: int
    id_incidente: int
    nombre_archivo: str | None
    ruta: str | None
    tipo_mime: str | None
    id_subido_por: int | None
    fecha_subida: datetime

    class Config:
        from_attributes = True
