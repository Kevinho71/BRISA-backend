from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class EstadoSolicitudEnum(str, enum.Enum):
    """Estados del flujo de aprobación de solicitudes"""
    recibida = "recibida"                          # Recepcionista la recibió (estado inicial)
    derivada = "derivada"                          # Derivada al regente
    aprobada = "aprobada"                          # Regente aprobó
    rechazada = "rechazada"                        # Regente rechazó
    cancelada = "cancelada"                        # Cancelada


class SolicitudRetiro(Base):
    """
    Modelo de Solicitud de Retiro
    Representa las solicitudes de retiro temprano de los estudiantes
    """
    __tablename__ = "solicitudes_retiro"
    
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), nullable=False, index=True)
    id_apoderado = Column(Integer, ForeignKey("apoderados.id_apoderado", ondelete="SET NULL"), nullable=False, index=True)
    id_motivo = Column(Integer, ForeignKey("motivos_retiro.id_motivo", ondelete="SET NULL"), nullable=False)
    id_autorizacion = Column(Integer, ForeignKey("autorizaciones_retiro.id_autorizacion", ondelete="SET NULL"), unique=True, nullable=True)
    fecha_hora_salida = Column(DateTime, nullable=False, index=True)
    fecha_hora_retorno_previsto = Column(DateTime, nullable=True)
    observacion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, nullable=False)
    
    # Campos para el flujo de aprobación
    estado = Column(Enum(EstadoSolicitudEnum), nullable=False, default="pendiente_recepcion", index=True)
    recibido_por = Column(Integer, ForeignKey("personas.id_persona", ondelete="SET NULL"), nullable=True, index=True)
    fecha_recepcion = Column(DateTime, nullable=True)
    derivado_a = Column(Integer, ForeignKey("personas.id_persona", ondelete="SET NULL"), nullable=True, index=True)
    fecha_derivacion = Column(DateTime, nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="solicitudes_retiro")
    apoderado = relationship("Apoderado", back_populates="solicitudes_retiro")
    motivo = relationship("MotivoRetiro", back_populates="solicitudes_retiro")
    autorizacion = relationship("AutorizacionRetiro", back_populates="solicitud", uselist=False)  # Relación 1:1
    detalles = relationship("SolicitudRetiroDetalle", back_populates="solicitud", cascade="all, delete-orphan")
    registro_salida = relationship("RegistroSalida", back_populates="solicitud", uselist=False)
    persona_recibio = relationship("Persona", foreign_keys=[recibido_por])
    persona_revisa = relationship("Persona", foreign_keys=[derivado_a])
    
    def __repr__(self):
        return f"<SolicitudRetiro(id={self.id_solicitud}, estudiante_id={self.id_estudiante})>"

