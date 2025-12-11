from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class EstadoSolicitudMasivaEnum(str, enum.Enum):
    """Estados del flujo de aprobación de solicitudes masivas"""
    pendiente = "pendiente"                        # Creada (estado inicial)
    recibida = "recibida"                          # Recepcionista la recibió
    derivada = "derivada"                          # Derivada al regente
    aprobada = "aprobada"                          # Regente aprobó
    rechazada = "rechazada"                        # Regente rechazó
    cancelada = "cancelada"                        # Cancelada


class SolicitudRetiroMasivo(Base):
    """
    Modelo de Solicitud de Retiro Masivo
    Representa las solicitudes de retiro temprano grupales (paseos, excursiones, etc.)
    """
    __tablename__ = "solicitudes_retiro_masivo"
    
    id_solicitud_masiva = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitante = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=False, index=True)
    id_motivo = Column(Integer, ForeignKey("motivos_retiro.id_motivo", ondelete="SET NULL"), nullable=False)
    id_autorizacion = Column(Integer, ForeignKey("autorizaciones_retiro.id_autorizacion", ondelete="SET NULL"), unique=True, nullable=True)
    
    fecha_hora_salida = Column(DateTime, nullable=False, index=True)
    fecha_hora_retorno = Column(DateTime, nullable=True)
    foto_evidencia = Column(String(500), nullable=False)  # URL o path de la foto (OBLIGATORIA)
    observacion = Column(Text, nullable=True)
    fecha_hora_solicitud = Column(DateTime, nullable=False)
    
    # Campos para el flujo de aprobación
    estado = Column(Enum(EstadoSolicitudMasivaEnum), nullable=False, default="pendiente", index=True)
    id_recepcionista = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True, index=True)
    fecha_recepcion = Column(DateTime, nullable=True)
    id_regente = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True, index=True)
    fecha_derivacion = Column(DateTime, nullable=True)
    
    # Relaciones
    solicitante = relationship("Usuario", foreign_keys=[id_solicitante], viewonly=True)
    motivo = relationship("MotivoRetiro", back_populates="solicitudes_masivas")
    autorizacion = relationship("AutorizacionRetiro", uselist=False, foreign_keys=[id_autorizacion])
    detalles = relationship("DetalleSolicitudRetiroMasivo", back_populates="solicitud", cascade="all, delete-orphan")
    registros_salida = relationship("RegistroSalida", back_populates="solicitud_masiva")
    recepcionista = relationship("Usuario", foreign_keys=[id_recepcionista], viewonly=True)
    regente = relationship("Usuario", foreign_keys=[id_regente], viewonly=True)
    
    def __repr__(self):
        return f"<SolicitudRetiroMasivo(id={self.id_solicitud_masiva}, solicitante_id={self.id_solicitante})>"
