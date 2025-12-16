from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoSolicitudEnum(str, Enum):
    """Estados del flujo de aprobación de solicitudes"""
    pendiente = "pendiente"        # Creada por apoderado
    recibida = "recibida"          # Recepcionista la recibió
    derivada = "derivada"          # Derivada al regente
    aprobada = "aprobada"          # Regente aprobó
    rechazada = "rechazada"        # Regente rechazó
    cancelada = "cancelada"        # Cancelada


class SolicitudRetiroCreateDTO(BaseModel):
    """DTO para crear una solicitud de retiro individual"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_motivo: int = Field(..., description="ID del motivo de retiro")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    foto_evidencia: str = Field(..., description="URL o path de la foto de evidencia (OBLIGATORIA)")
    observacion: Optional[str] = Field(None, description="Observaciones adicionales")


class SolicitudRetiroUpdateDTO(BaseModel):
    """DTO para actualizar una solicitud de retiro"""
    id_motivo: Optional[int] = Field(None, description="ID del motivo de retiro")
    fecha_hora_salida: Optional[datetime] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, description="Observaciones adicionales")
    estado: Optional[EstadoSolicitudEnum] = Field(None, description="Estado de la solicitud")


class RecibirSolicitudDTO(BaseModel):
    """DTO para recibir una solicitud"""
    fecha_hora_recepcion: Optional[datetime] = Field(None, description="Fecha y hora de recepción (default: now)")


class DerivarSolicitudDTO(BaseModel):
    """DTO para derivar una solicitud al regente"""
    observacion_derivacion: Optional[str] = Field(None, description="Observación de la derivación")


class AprobarRechazarSolicitudDTO(BaseModel):
    """DTO para aprobar o rechazar una solicitud"""
    decision: str = Field(..., description="'aprobada' o 'rechazada'")
    motivo_rechazo: Optional[str] = Field(None, description="Motivo del rechazo (obligatorio si rechazada)")


class CancelarSolicitudDTO(BaseModel):
    """DTO para cancelar una solicitud"""
    motivo_cancelacion: str = Field(..., description="Motivo de la cancelación")


class SolicitudRetiroResponseDTO(BaseModel):
    """DTO para respuesta de solicitud de retiro"""
    id_solicitud: int = Field(..., description="ID de la solicitud")
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: int = Field(..., description="ID del apoderado")
    id_motivo: int = Field(..., description="ID del motivo")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    tipo_solicitud: str = Field(..., description="Tipo de solicitud")
    foto_evidencia: str = Field(..., description="URL de la foto de evidencia")
    id_solicitante: Optional[int] = Field(None, description="ID del solicitante")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno_previsto: Optional[datetime] = Field(None, description="Fecha y hora de retorno previsto")
    observacion: Optional[str] = Field(None, description="Observaciones")
    fecha_creacion: datetime = Field(..., description="Fecha de creación de la solicitud")
    estado: str = Field(..., description="Estado actual de la solicitud")
    fecha_derivacion: Optional[datetime] = Field(None, description="Fecha de derivación")
    
    # Campos adicionales con información relacionada
    estudiante_nombre: Optional[str] = Field(None, description="Nombre completo del estudiante")
    apoderado_nombre: Optional[str] = Field(None, description="Nombre completo del apoderado")
    motivo_nombre: Optional[str] = Field(None, description="Nombre del motivo")
    curso_nombre: Optional[str] = Field(None, description="Nombre del curso")
    
    class Config:
        from_attributes = True

