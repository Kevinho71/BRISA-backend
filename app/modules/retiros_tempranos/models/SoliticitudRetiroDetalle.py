from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class SolicitudRetiroDetalle(Base):
    """
    Modelo de Detalle de Solicitud de Retiro
    Representa los detalles por materia/curso de una solicitud de retiro
    """
    __tablename__ = "solicitudes_retiro_detalle"
    __table_args__ = (
        UniqueConstraint('id_solicitud', 'id_curso', 'id_materia', name='uq_solicitud_curso_materia'),
    )
    
    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitud = Column(Integer, ForeignKey("solicitudes_retiro.id_solicitud", ondelete="CASCADE"), nullable=False)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso", ondelete="CASCADE"), nullable=False)
    id_materia = Column(Integer, ForeignKey("materias.id_materia", ondelete="CASCADE"), nullable=False)
    
    # Relaciones
    solicitud = relationship("SolicitudRetiro", back_populates="detalles")
    curso = relationship("Curso")
    materia = relationship("Materia")
    
    def __repr__(self):
        return f"<SolicitudRetiroDetalle(id={self.id_detalle}, solicitud_id={self.id_solicitud})>"

