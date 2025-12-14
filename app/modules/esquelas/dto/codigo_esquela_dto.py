# app/modules/esquelas/dto/codigo_esquela_dto.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CodigoEsquelaCreateDTO(BaseModel):
    """DTO para crear un nuevo código de esquela"""
    tipo: str = Field(..., description="Tipo: 'reconocimiento' u 'orientacion'")
    codigo: str = Field(..., max_length=10, description="Código único (ej: R01, O01)")
    descripcion: str = Field(..., description="Descripción del código")


class CodigoEsquelaUpdateDTO(BaseModel):
    """DTO para actualizar un código de esquela"""
    tipo: Optional[str] = None
    codigo: Optional[str] = None
    descripcion: Optional[str] = None


class CodigoEsquelaResponseDTO(BaseModel):
    """DTO para respuesta de código de esquela"""
    model_config = ConfigDict(from_attributes=True)
    
    id_codigo: int
    tipo: str
    codigo: str
    descripcion: str
