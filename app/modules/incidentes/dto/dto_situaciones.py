# app\modules\incidentes\dto\dto_situaciones.py
from pydantic import BaseModel

class SituacionCreateDTO(BaseModel):
    id_area: int
    nombre_situacion: str
    nivel_gravedad: str


class SituacionUpdateDTO(BaseModel):
    id_area: int | None = None
    nombre_situacion: str | None = None
    nivel_gravedad: str | None = None
