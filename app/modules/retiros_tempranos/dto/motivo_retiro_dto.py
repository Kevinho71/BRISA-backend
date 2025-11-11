from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SeveridadEnum(str, Enum):
    """Niveles de severidad para motivos de retiro"""
    LEVE = "leve"
    GRAVE = "grave"
    MUY_GRAVE = "muy grave"


class MotivoRetiroCreateDTO(BaseModel):
    """DTO para crear un motivo de retiro"""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre único del motivo")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del motivo")
    severidad: SeveridadEnum = Field(..., description="Nivel de severidad del motivo")
    activo: Optional[bool] = Field(True, description="Estado activo del motivo")


class MotivoRetiroUpdateDTO(BaseModel):
    """DTO para actualizar un motivo de retiro"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del motivo")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del motivo")
    severidad: Optional[SeveridadEnum] = Field(None, description="Nivel de severidad del motivo")
    activo: Optional[bool] = Field(None, description="Estado activo del motivo")


class MotivoRetiroResponseDTO(BaseModel):
    """DTO para respuesta de motivo de retiro"""
    id_motivo: int = Field(..., description="ID del motivo")
    nombre: str = Field(..., description="Nombre del motivo")
    descripcion: Optional[str] = Field(None, description="Descripción del motivo")
    severidad: str = Field(..., description="Nivel de severidad")
    activo: bool = Field(..., description="Estado activo")
    
    class Config:
        from_attributes = True
