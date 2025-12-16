from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TipoRegistroEnum(str, enum.Enum):
    """Tipos de registro de salida"""
    individual = "individual"                      # Registro de una solicitud individual
    masivo = "masivo"                             # Registro de una solicitud masiva


class RegistroSalida(Base):
    """
    Modelo de Registro de Salida
    Representa el registro de salidas efectivas de estudiantes (individual o masivo)
    """
    __tablename__ = "registros_salida"
    __table_args__ = {'extend_existing': True}
    
    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitud = Column(Integer, ForeignKey("solicitudes_retiro.id_solicitud", ondelete="CASCADE"), nullable=True, index=True)  # Ahora nullable
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), nullable=False, index=True)
    
    # NUEVOS CAMPOS
    tipo_registro = Column(Enum(TipoRegistroEnum), nullable=False, default="individual", index=True)
    id_solicitud_masiva = Column(Integer, ForeignKey("solicitudes_retiro_masivo.id_solicitud_masiva", ondelete="CASCADE"), nullable=True, index=True)
    
    fecha_hora_salida_real = Column(DateTime, nullable=False)
    fecha_hora_retorno_real = Column(DateTime, nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", foreign_keys=[id_estudiante], viewonly=True)
    solicitud = relationship("SolicitudRetiro", foreign_keys=[id_solicitud], viewonly=True)
    solicitud_masiva = relationship("SolicitudRetiroMasivo", foreign_keys=[id_solicitud_masiva], viewonly=True)
    
    def __repr__(self):
        return f"<RegistroSalida(id={self.id_registro}, tipo={self.tipo_registro}, estudiante_id={self.id_estudiante})>"

