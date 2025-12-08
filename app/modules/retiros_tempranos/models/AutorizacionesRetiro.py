from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class DecisionEnum(str, enum.Enum):
    """Enumeración para decisiones de autorización"""
    aprobado = "aprobado"
    rechazado = "rechazado"
    pendiente = "pendiente"


class AutorizacionRetiro(Base):
    """
    Modelo de Autorización de Retiro
    Representa las autorizaciones para retiros tempranos
    """
    __tablename__ = "autorizaciones_retiro"
    __table_args__ = {'extend_existing': True}
    
    id_autorizacion = Column(Integer, primary_key=True, autoincrement=True)
    decidido_por = Column(Integer, ForeignKey("personas.id_persona", ondelete="SET NULL"), nullable=False)
    decision = Column(Enum(DecisionEnum), nullable=False)
    motivo_decision = Column(String(255), nullable=True)
    fecha_decision = Column(DateTime, nullable=False)
    
    # Relaciones
    persona_decidio = relationship("Persona", foreign_keys=[decidido_por])
    solicitud = relationship("SolicitudRetiro", back_populates="autorizacion", uselist=False)  # Relación 1:1
    
    def __repr__(self):
        return f"<AutorizacionRetiro(id={self.id_autorizacion}, decision={self.decision})>"

