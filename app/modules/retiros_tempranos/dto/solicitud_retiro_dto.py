from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class SolicitudRetiroCreateDTO(BaseModel):
    """DTO para crear una solicitud de retiro"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: Optional[int] = Field(None, description="ID del apoderado")
    id_motivo: Optional[int] = Field(None, description="ID del motivo de retiro")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: Optional[date] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno: Optional[date] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, max_length=255, description="Observaciones adicionales")
    foto_retirante_url: Optional[str] = Field(None, max_length=255, description="URL de foto del retirante")
    id_registro_salida: Optional[int] = Field(None, description="ID del registro de salida")


class SolicitudRetiroUpdateDTO(BaseModel):
    """DTO para actualizar una solicitud de retiro"""
    id_apoderado: Optional[int] = Field(None, description="ID del apoderado")
    id_motivo: Optional[int] = Field(None, description="ID del motivo de retiro")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: Optional[date] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno: Optional[date] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, max_length=255, description="Observaciones adicionales")
    foto_retirante_url: Optional[str] = Field(None, max_length=255, description="URL de foto del retirante")
    id_registro_salida: Optional[int] = Field(None, description="ID del registro de salida")


class SolicitudRetiroResponseDTO(BaseModel):
    """DTO para respuesta de solicitud de retiro"""
    id_solicitud: int = Field(..., description="ID de la solicitud")
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: Optional[int] = Field(None, description="ID del apoderado")
    id_motivo: Optional[int] = Field(None, description="ID del motivo")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: Optional[date] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno: Optional[date] = Field(None, description="Fecha y hora de retorno")
    observacion: Optional[str] = Field(None, description="Observaciones")
    foto_retirante_url: Optional[str] = Field(None, description="URL de foto")
    creada_en: Optional[date] = Field(None, description="Fecha de creación")
    id_registro_salida: Optional[int] = Field(None, description="ID del registro de salida")
    
    class Config:
        from_attributes = True
