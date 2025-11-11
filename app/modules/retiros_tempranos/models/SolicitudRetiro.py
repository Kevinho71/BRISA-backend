from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel

class SolicitudRetiro(BaseModel):
    """
    Modelo de Solicitud de Retiro
    Representa las solicitudes de retiro temprano de los estudiantes
    """
    __tablename__ = "solicitudes_retiro"
    
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), nullable=False, index=True)
    id_apoderado = Column(Integer, ForeignKey("apoderados.id_apoderado", ondelete="SET NULL"), nullable=False, index=True)
    id_motivo = Column(Integer, ForeignKey("motivos_retiro.id_motivo", ondelete="SET NULL"), nullable=False)
    id_autorizacion = Column(Integer, ForeignKey("autorizaciones_retiro.id_autorizacion", ondelete="SET NULL"), nullable=True)
    fecha_hora_salida = Column(DateTime, nullable=False, index=True)
    fecha_hora_retorno_previsto = Column(DateTime, nullable=True)
    observacion = Column(Text, nullable=True)
    foto_retirante_url = Column(String(300), nullable=True)
    fecha_creacion = Column(DateTime, nullable=False)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="solicitudes_retiro")
    apoderado = relationship("Apoderado", back_populates="solicitudes_retiro")
    motivo = relationship("MotivoRetiro", back_populates="solicitudes_retiro")
    autorizacion = relationship("AutorizacionRetiro", back_populates="solicitudes")
    detalles = relationship("SolicitudRetiroDetalle", back_populates="solicitud", cascade="all, delete-orphan")
    registro_salida = relationship("RegistroSalida", back_populates="solicitud", uselist=False)
    
    def __repr__(self):
        return f"<SolicitudRetiro(id={self.id_solicitud}, estudiante_id={self.id_estudiante})>"

