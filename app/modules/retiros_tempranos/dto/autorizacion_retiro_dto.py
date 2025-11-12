from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DecisionEnum(str, Enum):
    """Decisiones posibles para autorizaciones"""
    aprobado = "aprobado"
    rechazado = "rechazado"
    pendiente = "pendiente"


class AutorizacionRetiroCreateDTO(BaseModel):
    """DTO para crear una autorización de retiro"""
    id_solicitud: int = Field(..., description="ID de la solicitud que se está autorizando")
    decision: DecisionEnum = Field(..., description="Decisión tomada (aprobado/rechazado)")
    motivo_decision: Optional[str] = Field(None, max_length=255, description="Motivo de la decisión")


class AutorizacionRetiroUpdateDTO(BaseModel):
    """DTO para actualizar una autorización de retiro"""
    decidido_por: Optional[int] = Field(None, description="ID de la persona que autoriza/deniega")
    decision: Optional[DecisionEnum] = Field(None, description="Decisión tomada")
    motivo_decision: Optional[str] = Field(None, max_length=255, description="Motivo de la decisión")
    fecha_decision: Optional[datetime] = Field(None, description="Fecha y hora de la decisión")


class AutorizacionRetiroResponseDTO(BaseModel):
    """DTO para respuesta de autorización de retiro"""
    id_autorizacion: int = Field(..., description="ID de la autorización")
    decidido_por: int = Field(..., description="ID de la persona que decidió")
    decision: str = Field(..., description="Decisión tomada")
    motivo_decision: Optional[str] = Field(None, description="Motivo de la decisión")
    fecha_decision: datetime = Field(..., description="Fecha y hora de la decisión")
    
    class Config:
        from_attributes = True
