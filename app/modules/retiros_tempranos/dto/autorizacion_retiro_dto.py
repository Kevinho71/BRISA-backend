from pydantic import BaseModel, Field
from typing import Optional


class AutorizacionRetiroCreateDTO(BaseModel):
    """DTO para crear una autorización de retiro"""
    decidido_por: str = Field(..., min_length=1, max_length=255, description="Persona que autoriza/deniega")
    decision: str = Field(..., min_length=1, max_length=255, description="Decisión tomada (aprobado/rechazado)")
    motivo_decision: Optional[str] = Field(None, max_length=255, description="Motivo de la decisión")
    decidido_en: str = Field(..., min_length=1, max_length=255, description="Fecha/hora de la decisión")


class AutorizacionRetiroUpdateDTO(BaseModel):
    """DTO para actualizar una autorización de retiro"""
    decidido_por: Optional[str] = Field(None, min_length=1, max_length=255, description="Persona que autoriza/deniega")
    decision: Optional[str] = Field(None, min_length=1, max_length=255, description="Decisión tomada")
    motivo_decision: Optional[str] = Field(None, max_length=255, description="Motivo de la decisión")
    decidido_en: Optional[str] = Field(None, min_length=1, max_length=255, description="Fecha/hora de la decisión")


class AutorizacionRetiroResponseDTO(BaseModel):
    """DTO para respuesta de autorización de retiro"""
    id_autorizacion: int = Field(..., description="ID de la autorización")
    decidido_por: str = Field(..., description="Persona que autorizó/denegó")
    decision: str = Field(..., description="Decisión tomada")
    motivo_decision: Optional[str] = Field(None, description="Motivo de la decisión")
    decidido_en: str = Field(..., description="Fecha/hora de la decisión")
    
    class Config:
        from_attributes = True
