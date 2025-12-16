from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class EstadoSolicitudMasivaEnum(str, Enum):
    """Estados del flujo de aprobación de solicitudes masivas"""
    pendiente = "pendiente"        # Creada por profesor/admin
    recibida = "recibida"          # Recepcionista la recibió
    derivada = "derivada"          # Derivada al regente
    aprobada = "aprobada"          # Regente aprobó
    rechazada = "rechazada"        # Regente rechazó
    cancelada = "cancelada"        # Cancelada


class DetalleSolicitudMasivoCreateDTO(BaseModel):
    """DTO para agregar un estudiante a la solicitud masiva"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    observacion_individual: Optional[str] = Field(None, description="Observación para este estudiante")


class DetalleSolicitudMasivoResponseDTO(BaseModel):
    """DTO para respuesta de detalle de solicitud masiva"""
    id_detalle: int = Field(..., description="ID del detalle")
    id_solicitud_masiva: int = Field(..., description="ID de la solicitud masiva")
    id_estudiante: int = Field(..., description="ID del estudiante")
    observacion_individual: Optional[str] = Field(None, description="Observación individual")
    
    # Campos adicionales
    estudiante_nombre: Optional[str] = Field(None, description="Nombre del estudiante")
    estudiante_ci: Optional[str] = Field(None, description="CI del estudiante")
    curso_nombre: Optional[str] = Field(None, description="Curso del estudiante")
    
    class Config:
        from_attributes = True


class SolicitudRetiroMasivoCreateDTO(BaseModel):
    """DTO para crear una solicitud de retiro masivo"""
    id_motivo: int = Field(..., description="ID del motivo de retiro")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    foto_evidencia: str = Field(..., description="URL o path de la foto de evidencia (OBLIGATORIA)")
    observacion: Optional[str] = Field(None, description="Observaciones generales")
    estudiantes: List[DetalleSolicitudMasivoCreateDTO] = Field(..., description="Lista de estudiantes")


class SolicitudRetiroMasivoUpdateDTO(BaseModel):
    """DTO para actualizar una solicitud de retiro masivo"""
    id_motivo: Optional[int] = Field(None, description="ID del motivo de retiro")
    fecha_hora_salida: Optional[datetime] = Field(None, description="Fecha y hora de salida")
    fecha_hora_retorno: Optional[datetime] = Field(None, description="Fecha y hora de retorno estimado")
    observacion: Optional[str] = Field(None, description="Observaciones generales")
    estado: Optional[EstadoSolicitudMasivaEnum] = Field(None, description="Estado de la solicitud")


class RecibirSolicitudMasivaDTO(BaseModel):
    """DTO para recibir una solicitud masiva"""
    fecha_hora_recepcion: Optional[datetime] = Field(None, description="Fecha y hora de recepción (default: now)")


class DerivarSolicitudMasivaDTO(BaseModel):
    """DTO para derivar una solicitud masiva al regente"""
    id_regente: int = Field(..., description="ID del regente")
    observacion_derivacion: Optional[str] = Field(None, description="Observación de la derivación")


class AprobarRechazarSolicitudMasivaDTO(BaseModel):
    """DTO para aprobar o rechazar una solicitud masiva"""
    decision: str = Field(..., description="'aprobada' o 'rechazada'")
    motivo_rechazo: Optional[str] = Field(None, description="Motivo del rechazo (obligatorio si rechazada)")


class CancelarSolicitudMasivaDTO(BaseModel):
    """DTO para cancelar una solicitud masiva"""
    motivo_cancelacion: str = Field(..., description="Motivo de la cancelación")


class SolicitudRetiroMasivoResponseDTO(BaseModel):
    """DTO para respuesta de solicitud de retiro masivo"""
    id_solicitud: int = Field(..., description="ID de la solicitud")
    id_solicitante: int = Field(..., description="ID del solicitante (profesor/admin)")
    id_motivo: int = Field(..., description="ID del motivo")
    id_autorizacion: Optional[int] = Field(None, description="ID de la autorización")
    fecha_hora_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_hora_retorno: Optional[datetime] = Field(None, description="Fecha y hora de retorno")
    foto_evidencia: str = Field(..., description="URL de la foto de evidencia")
    observacion: Optional[str] = Field(None, description="Observaciones")
    fecha_hora_solicitud: datetime = Field(..., description="Fecha de creación")
    estado: str = Field(..., description="Estado actual de la solicitud")
    id_recepcionista: Optional[int] = Field(None, description="ID del usuario recepcionista")
    fecha_recepcion: Optional[datetime] = Field(None, description="Fecha de recepción")
    id_regente: Optional[int] = Field(None, description="ID del usuario regente")
    fecha_derivacion: Optional[datetime] = Field(None, description="Fecha de derivación")
    
    # Campos adicionales con información relacionada
    solicitante_nombre: Optional[str] = Field(None, description="Nombre completo del solicitante")
    motivo_nombre: Optional[str] = Field(None, description="Nombre del motivo")
    cantidad_estudiantes: Optional[int] = Field(None, description="Cantidad de estudiantes")
    
    class Config:
        from_attributes = True


class SolicitudRetiroMasivoDetalladaResponseDTO(SolicitudRetiroMasivoResponseDTO):
    """DTO para respuesta detallada de solicitud masiva (incluye lista de estudiantes)"""
    detalles: List[DetalleSolicitudMasivoResponseDTO] = Field(default_factory=list, description="Lista de estudiantes")
