

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel

class SolicitudRetiroDetalle(BaseModel):
    """
    Modelo de Detalle de Solicitud de Retiro
    Representa los detalles por materia/curso de una solicitud de retiro
    """
    __tablename__ = "solicitud_retiro_detalle"
    
    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitud = Column(Integer, ForeignKey("solicitud_retiro.id_solicitud", ondelete="CASCADE"), nullable=False)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="CASCADE"), nullable=True)
    id_materia = Column(Integer, ForeignKey("materia.id_materia", ondelete="CASCADE"), nullable=True)
    
    # Relaciones
    solicitud = relationship("SolicitudRetiro", back_populates="detalles")
    curso = relationship("Curso", back_populates="solicitudes_retiro_detalle")
    materia = relationship("Materia", back_populates="solicitudes_retiro_detalle")
    
    def __repr__(self):
        return f"<SolicitudRetiroDetalle(id={self.id_detalle}, solicitud_id={self.id_solicitud})>"

