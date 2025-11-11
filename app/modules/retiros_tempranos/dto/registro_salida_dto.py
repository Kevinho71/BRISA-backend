from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegistroSalidaCreateDTO(BaseModel):
    """DTO para crear un registro de salida"""
    id_solicitud: int = Field(..., description="ID de la solicitud de retiro")
    id_estudiante: int = Field(..., description="ID del estudiante")
    fecha_hora_salida_real: datetime = Field(..., description="Fecha y hora real de salida")
    fecha_hora_retorno_real: Optional[datetime] = Field(None, description="Fecha y hora real de retorno")


class RegistroSalidaUpdateDTO(BaseModel):
    """DTO para actualizar un registro de salida"""
    fecha_hora_salida_real: Optional[datetime] = Field(None, description="Fecha y hora real de salida")
    fecha_hora_retorno_real: Optional[datetime] = Field(None, description="Fecha y hora real de retorno")


class RegistroSalidaResponseDTO(BaseModel):
    """DTO para respuesta de registro de salida"""
    id_registro: int = Field(..., description="ID del registro")
    id_solicitud: int = Field(..., description="ID de la solicitud de retiro")
    id_estudiante: int = Field(..., description="ID del estudiante")
    fecha_hora_salida_real: datetime = Field(..., description="Fecha y hora real de salida")
    fecha_hora_retorno_real: Optional[datetime] = Field(None, description="Fecha y hora real de retorno")
    
    class Config:
        from_attributes = True
