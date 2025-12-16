from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class SeveridadEnum(str, enum.Enum):
    """Enumeración para niveles de severidad de motivos"""
    leve = "leve"
    grave = "grave"
    muy_grave = "muy grave"


class MotivoRetiro(Base):
    """
    Modelo de Motivo de Retiro
    Catálogo de motivos para retiros tempranos
    """
    __tablename__ = "motivos_retiro"
    __table_args__ = {'extend_existing': True}
    
    id_motivo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    severidad = Column(Enum(SeveridadEnum), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    
    # Relaciones
    solicitudes_retiro = relationship("SolicitudRetiro", foreign_keys="SolicitudRetiro.id_motivo", viewonly=True)
    solicitudes_masivas = relationship("SolicitudRetiroMasivo", foreign_keys="SolicitudRetiroMasivo.id_motivo", viewonly=True)
    
    def __repr__(self):
        return f"<MotivoRetiro(id={self.id_motivo}, nombre={self.nombre}, severidad={self.severidad})>"

