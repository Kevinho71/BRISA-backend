# app/modules/esquelas/dto/esquela_dto.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class CodigoEsquelaDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_codigo: int
    tipo: str
    codigo: str
    descripcion: str

class EsquelaBaseDTO(BaseModel):
    id_estudiante: int
    id_profesor: int
    id_registrador: int
    fecha: datetime
    observaciones: Optional[str] = None
    codigos: List[int]

class EsquelaResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_esquela: int
    fecha: datetime
    observaciones: Optional[str]
    codigos: List[CodigoEsquelaDTO]
