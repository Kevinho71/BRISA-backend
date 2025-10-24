from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel



class AutorizacionRetiro(BaseModel):
    """
    Modelo de Autorización de Retiro
    Representa las autorizaciones para retiros tempranos
    """
    __tablename__ = "autorizacoin_retiro"  # Manteniendo el nombre del diagrama (con typo)
    
    id_autorizacion = Column(Integer, primary_key=True, autoincrement=True)
    decidido_por = Column(String(255), nullable=False)
    decision = Column(String(255), nullable=False)
    motivo_decision = Column(String(255), nullable=True)
    decidido_en = Column(String(255), nullable=False)
    
    # Relaciones
    solicitudes = relationship("SolicitudRetiro", back_populates="autorizacion")
    
    def __repr__(self):
        return f"<AutorizacionRetiro(id={self.id_autorizacion}, decision={self.decision})>"

