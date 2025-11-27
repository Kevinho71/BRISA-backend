# app\modules\incidentes\dto\dto_areas.py
from pydantic import BaseModel

class AreaCreateDTO(BaseModel):
    nombre_area: str
    descripcion: str | None = None


class AreaUpdateDTO(BaseModel):
    nombre_area: str
    descripcion: str | None = None
