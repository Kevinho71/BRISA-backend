from pydantic import BaseModel, Field
from typing import Optional


class MotivoRetiroCreateDTO(BaseModel):
    """DTO para crear un motivo de retiro"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del motivo")
    severidad: str = Field(..., min_length=1, max_length=255, description="Nivel de severidad del motivo")
    activo: str = Field(default='1', max_length=1000, description="Estado activo del motivo")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del motivo")


class MotivoRetiroUpdateDTO(BaseModel):
    """DTO para actualizar un motivo de retiro"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre del motivo")
    severidad: Optional[str] = Field(None, min_length=1, max_length=255, description="Nivel de severidad del motivo")
    activo: Optional[str] = Field(None, max_length=1000, description="Estado activo del motivo")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del motivo")


class MotivoRetiroResponseDTO(BaseModel):
    """DTO para respuesta de motivo de retiro"""
    id_motivo: int = Field(..., description="ID del motivo")
    nombre: str = Field(..., description="Nombre del motivo")
    severidad: str = Field(..., description="Nivel de severidad")
    activo: str = Field(..., description="Estado activo")
    descripcion: Optional[str] = Field(None, description="Descripción del motivo")
    
    class Config:
        from_attributes = True
