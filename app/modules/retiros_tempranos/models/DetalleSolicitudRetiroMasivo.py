from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class DetalleSolicitudRetiroMasivo(Base):
    """
    Modelo de Detalle de Solicitud de Retiro Masivo
    Representa cada estudiante incluido en una solicitud masiva
    """
    __tablename__ = "detalle_solicitudes_retiro_masivo"
    
    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitud_masiva = Column(Integer, ForeignKey("solicitudes_retiro_masivo.id_solicitud_masiva", ondelete="CASCADE"), nullable=False, index=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), nullable=False, index=True)
    observacion_individual = Column(Text, nullable=True)  # Observación específica para este estudiante
    
    # Relaciones
    solicitud = relationship("SolicitudRetiroMasivo", back_populates="detalles")
    estudiante = relationship("Estudiante")
    
    def __repr__(self):
        return f"<DetalleSolicitudRetiroMasivo(id={self.id_detalle}, solicitud={self.id_solicitud_masiva}, estudiante={self.id_estudiante})>"
