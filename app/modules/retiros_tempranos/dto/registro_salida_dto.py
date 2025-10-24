from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class RegistroSalidaCreateDTO(BaseModel):
    """DTO para crear un registro de salida"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    salida_en: date = Field(..., description="Fecha y hora de salida")
    retorno_en: Optional[date] = Field(None, description="Fecha y hora de retorno")


class RegistroSalidaUpdateDTO(BaseModel):
    """DTO para actualizar un registro de salida"""
    salida_en: Optional[date] = Field(None, description="Fecha y hora de salida")
    retorno_en: Optional[date] = Field(None, description="Fecha y hora de retorno")


class RegistroSalidaResponseDTO(BaseModel):
    """DTO para respuesta de registro de salida"""
    id_registro: int = Field(..., description="ID del registro")
    id_estudiante: int = Field(..., description="ID del estudiante")
    salida_en: date = Field(..., description="Fecha y hora de salida")
    retorno_en: Optional[date] = Field(None, description="Fecha y hora de retorno")
    
    class Config:
        from_attributes = True
