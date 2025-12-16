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
    
    # Información adicional del estudiante (computed fields)
    estudiante_nombre: Optional[str] = Field(None, description="Nombre completo del estudiante")
    estudiante_ci: Optional[str] = Field(None, description="CI del estudiante")
    
    class Config:
        from_attributes = True
    
    @classmethod
    def model_validate(cls, obj):
        """Override para agregar datos del estudiante desde la relación"""
        data = {
            'id_estudiante': obj.id_estudiante,
            'id_apoderado': obj.id_apoderado,
            'parentesco': obj.parentesco,
            'es_contacto_principal': obj.es_contacto_principal,
        }
        
        # Agregar datos del estudiante si están disponibles
        if hasattr(obj, 'estudiante') and obj.estudiante:
            est = obj.estudiante
            nombre_completo = f"{est.nombres} {est.apellido_paterno or ''} {est.apellido_materno or ''}".strip()
            data['estudiante_nombre'] = nombre_completo
            data['estudiante_ci'] = est.ci
        
        return super().model_validate(data)
