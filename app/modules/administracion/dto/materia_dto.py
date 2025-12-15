from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class NivelEnum(str, Enum):
    inicial = "inicial"
    primaria = "primaria"
    secundaria = "secundaria"

class MateriaBaseDTO(BaseModel):
    nombre_materia: str = Field(..., min_length=1, max_length=50)
    nivel: NivelEnum

class MateriaCreateDTO(MateriaBaseDTO):
    pass

class MateriaUpdateDTO(MateriaBaseDTO):
    pass

class MateriaDTO(MateriaBaseDTO):
    id_materia: int

    model_config = ConfigDict(from_attributes=True)
