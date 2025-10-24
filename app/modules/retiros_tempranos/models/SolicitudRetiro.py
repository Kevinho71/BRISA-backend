

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel

class SolicitudRetiro(BaseModel):
    """
    Modelo de Solicitud de Retiro
    Representa las solicitudes de retiro temprano de los estudiantes
    """
    __tablename__ = "solicitud_retiro"
    
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante", ondelete="CASCADE"), nullable=False)
    id_apoderado = Column(Integer, ForeignKey("apoderado.id_apoderado", ondelete="SET NULL"), nullable=True)
    id_motivo = Column(Integer, ForeignKey("motivo_retiro.id_motivo", ondelete="SET NULL"), nullable=True)
    id_autorizacion = Column(Integer, ForeignKey("autorizacoin_retiro.id_autorizacion", ondelete="SET NULL"), nullable=True)
    fecha_hora_salida = Column(Date, nullable=True)
    fecha_hora_retorno = Column(Date, nullable=True)
    observacion = Column(String(255), nullable=True)
    foto_retirante_url = Column(String(255), nullable=True)
    creada_en = Column(Date, nullable=True)
    id_registro_salida = Column(Integer, ForeignKey("registro_salida.id_registro", ondelete="SET NULL"), nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="solicitudes_retiro")
    apoderado = relationship("Apoderado")
    motivo = relationship("MotivoRetiro", back_populates="solicitudes_retiro")
    autorizacion = relationship("AutorizacionRetiro", back_populates="solicitudes")
    registro_salida = relationship("RegistroSalida", back_populates="solicitudes")
    detalles = relationship("SolicitudRetiroDetalle", back_populates="solicitud")
    
    def __repr__(self):
        return f"<SolicitudRetiro(id={self.id_solicitud}, estudiante_id={self.id_estudiante})>"

