from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegistroSalidaCreateDTO(BaseModel):
    """DTO para crear un registro de salida individual"""
    id_solicitud: int = Field(..., description="ID de la solicitud de retiro aprobada")
    fecha_hora_salida_real: Optional[datetime] = Field(None, description="Fecha y hora real de salida (default: now)")


class RegistroSalidaMasivoCreateDTO(BaseModel):
    """DTO para crear registros de salida masivos"""
    id_solicitud_masiva: int = Field(..., description="ID de la solicitud masiva aprobada")
    fecha_hora_salida_real: Optional[datetime] = Field(None, description="Fecha y hora real de salida (default: now)")


class RegistroSalidaUpdateDTO(BaseModel):
    """DTO para actualizar un registro de salida (solo retorno)"""
    fecha_hora_retorno_real: datetime = Field(..., description="Fecha y hora real de retorno")


class RegistroSalidaResponseDTO(BaseModel):
    """DTO para respuesta de registro de salida"""
    id_registro: int = Field(..., description="ID del registro")
    id_solicitud: Optional[int] = Field(None, description="ID de la solicitud de retiro individual")
    id_solicitud_masiva: Optional[int] = Field(None, description="ID de la solicitud de retiro masiva")
    id_estudiante: int = Field(..., description="ID del estudiante")
    tipo_registro: str = Field(..., description="Tipo de registro (individual/masivo)")
    fecha_hora_salida_real: datetime = Field(..., description="Fecha y hora real de salida")
    fecha_hora_retorno_real: Optional[datetime] = Field(None, description="Fecha y hora real de retorno")
    
    # Campos adicionales con información relacionada
    estudiante_nombre: Optional[str] = Field(None, description="Nombre completo del estudiante")
    estudiante_ci: Optional[str] = Field(None, description="CI del estudiante")
    
    class Config:
        from_attributes = True
