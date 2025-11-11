from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel
import enum


class SeveridadEnum(str, enum.Enum):
    """Enumeración para niveles de severidad de motivos"""
    LEVE = "leve"
    GRAVE = "grave"
    MUY_GRAVE = "muy grave"


class MotivoRetiro(BaseModel):
    """
    Modelo de Motivo de Retiro
    Catálogo de motivos para retiros tempranos
    """
    __tablename__ = "motivos_retiro"
    
    id_motivo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    severidad = Column(Enum(SeveridadEnum), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    
    # Relaciones
    solicitudes_retiro = relationship("SolicitudRetiro", back_populates="motivo")
    
    def __repr__(self):
        return f"<MotivoRetiro(id={self.id_motivo}, nombre={self.nombre}, severidad={self.severidad})>"

