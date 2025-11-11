from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolicitudRetiroCreateDTO(BaseModel):
    """DTO para crear una solicitud de retiro"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: int = Field(..., description="ID del apoderado")
    id_motivo: int = Field(..., description="ID del motivo de retiro")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, description="Observaciones adicionales")
    foto_retirante_url: Optional[str] = Field(None, max_length=300, description="URL de foto del retirante")
    fecha_creacion: datetime = Field(..., description="Fecha de creación de la solicitud")


class SolicitudRetiroUpdateDTO(BaseModel):
    """DTO para actualizar una solicitud de retiro"""
    id_apoderado: Optional[int] = Field(None, description="ID del apoderado")
    id_motivo: Optional[int] = Field(None, description="ID del motivo de retiro")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: Optional[datetime] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, description="Observaciones adicionales")
    foto_retirante_url: Optional[str] = Field(None, max_length=300, description="URL de foto del retirante")


class SolicitudRetiroResponseDTO(BaseModel):
    """DTO para respuesta de solicitud de retiro"""
    id_solicitud: int = Field(..., description="ID de la solicitud")
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: int = Field(..., description="ID del apoderado")
    id_motivo: int = Field(..., description="ID del motivo")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno previsto")
    observacion: Optional[str] = Field(None, description="Observaciones")
    foto_retirante_url: Optional[str] = Field(None, description="URL de foto")
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    
    class Config:
        from_attributes = True
