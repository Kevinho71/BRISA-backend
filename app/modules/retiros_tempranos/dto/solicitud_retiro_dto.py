from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoSolicitudEnum(str, Enum):
    """Estados del flujo de aprobación de solicitudes"""
    recibida = "recibida"          # Recepcionista la recibió (estado inicial automático)
    derivada = "derivada"          # Derivada al regente
    aprobada = "aprobada"          # Regente aprobó
    rechazada = "rechazada"        # Regente rechazó
    cancelada = "cancelada"        # Cancelada


class SolicitudRetiroCreateDTO(BaseModel):
    """DTO para crear una solicitud de retiro (fecha_creacion automática)"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: int = Field(..., description="ID del apoderado")
    id_motivo: int = Field(..., description="ID del motivo de retiro")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, description="Observaciones adicionales")


class SolicitudRetiroUpdateDTO(BaseModel):
    """DTO para actualizar una solicitud de retiro"""
    id_apoderado: Optional[int] = Field(None, description="ID del apoderado")
    id_motivo: Optional[int] = Field(None, description="ID del motivo de retiro")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: Optional[datetime] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, description="Observaciones adicionales")
    estado: Optional[EstadoSolicitudEnum] = Field(None, description="Estado de la solicitud")


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
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    estado: str = Field(..., description="Estado actual de la solicitud")
    recibido_por: Optional[int] = Field(None, description="ID del recepcionista")
    fecha_recepcion: Optional[datetime] = Field(None, description="Fecha de recepción")
    derivado_a: Optional[int] = Field(None, description="ID del regente")
    fecha_derivacion: Optional[datetime] = Field(None, description="Fecha de derivación")
    
    class Config:
        from_attributes = True
