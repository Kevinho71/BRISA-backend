# app\modules\incidentes\dto\dto_notificaiones.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionBaseDTO(BaseModel):
    titulo: str
    mensaje: str
    id_incidente: Optional[int] = None
    id_derivacion: Optional[int] = None


class NotificacionCreateDTO(NotificacionBaseDTO):
    id_usuario: int   # usuario que recibirá la notificación


class NotificacionOutDTO(NotificacionBaseDTO):
    id_notificacion: int
    id_usuario: int
    leido: bool
    fecha: datetime

    class Config:
        from_attributes = True
