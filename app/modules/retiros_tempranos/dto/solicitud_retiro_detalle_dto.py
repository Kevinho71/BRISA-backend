from pydantic import BaseModel, Field


class SolicitudRetiroDetalleCreateDTO(BaseModel):
    """DTO para crear un detalle de solicitud de retiro"""
    id_solicitud: int = Field(..., description="ID de la solicitud de retiro")
    id_curso: int = Field(..., description="ID del curso")
    id_materia: int = Field(..., description="ID de la materia")


class SolicitudRetiroDetalleUpdateDTO(BaseModel):
    """DTO para actualizar un detalle de solicitud de retiro"""
    id_curso: int = Field(..., description="ID del curso")
    id_materia: int = Field(..., description="ID de la materia")


class SolicitudRetiroDetalleResponseDTO(BaseModel):
    """DTO para respuesta de detalle de solicitud de retiro"""
    id_detalle: int = Field(..., description="ID del detalle")
    id_solicitud: int = Field(..., description="ID de la solicitud de retiro")
    id_curso: int = Field(..., description="ID del curso")
    id_materia: int = Field(..., description="ID de la materia")
    
    class Config:
        from_attributes = True
