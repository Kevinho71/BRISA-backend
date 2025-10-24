""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel


class MotivoRetiro(BaseModel):
    """
    Modelo de Motivo de Retiro
    Catálogo de motivos para retiros tempranos
    """
    __tablename__ = "motivo_retiro"
    
    id_motivo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    severidad = Column(String(255), nullable=False)
    activo = Column(String(1000), nullable=False, default='1')  # binary(1000) en MySQL
    descripcion = Column(String(255), nullable=True)
    
    # Relaciones
    solicitudes_retiro = relationship("SolicitudRetiro", back_populates="motivo")
    
    def __repr__(self):
        return f"<MotivoRetiro(id={self.id_motivo}, nombre={self.nombre}, severidad={self.severidad})>"

