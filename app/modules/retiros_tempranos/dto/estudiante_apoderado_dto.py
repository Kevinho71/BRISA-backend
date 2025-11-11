from pydantic import BaseModel, Field
from typing import Optional


class EstudianteApoderadoCreateDTO(BaseModel):
    """DTO para asociar un apoderado con un estudiante"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: int = Field(..., description="ID del apoderado")
    parentesco: str = Field(..., min_length=1, max_length=50, description="Relación de parentesco")
    es_contacto_principal: Optional[bool] = Field(False, description="Indica si es el contacto principal")


class EstudianteApoderadoUpdateDTO(BaseModel):
    """DTO para actualizar la relación estudiante-apoderado"""
    parentesco: Optional[str] = Field(None, min_length=1, max_length=50, description="Relación de parentesco")
    es_contacto_principal: Optional[bool] = Field(None, description="Indica si es el contacto principal")


class EstudianteApoderadoResponseDTO(BaseModel):
    """DTO para respuesta de relación estudiante-apoderado"""
    id_estudiante: int = Field(..., description="ID del estudiante")
    id_apoderado: int = Field(..., description="ID del apoderado")
    parentesco: str = Field(..., description="Relación de parentesco")
    es_contacto_principal: Optional[bool] = Field(None, description="Es contacto principal")
    
    class Config:
        from_attributes = True
