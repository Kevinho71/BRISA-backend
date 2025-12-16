# app\modules\retiros_tempranos\models\SolicitudRetiro.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class EstadoSolicitudEnum(str, enum.Enum):
    """Estados del flujo de aprobación de solicitudes"""
    recibida = "recibida"                          # Recepcionista la recibió
    derivada = "derivada"                          # Derivada al regente
    aprobada = "aprobada"                          # Regente aprobó
    rechazada = "rechazada"                        # Regente rechazó
    cancelada = "cancelada"                        # Cancelada


class TipoSolicitudEnum(str, enum.Enum):
    """Tipos de solicitud de retiro"""
    individual = "individual"                      # Apoderado para un estudiante
    masiva = "masiva"                             # Profesor/Admin para grupo


class SolicitudRetiro(Base):
    """
    Modelo de Solicitud de Retiro Individual
    Representa las solicitudes de retiro temprano individuales (apoderado -> estudiante)
    """
    __tablename__ = "solicitudes_retiro"
    __table_args__ = {'extend_existing': True}
    
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), nullable=False, index=True)
    id_apoderado = Column(Integer, ForeignKey("apoderados.id_apoderado", ondelete="SET NULL"), nullable=False, index=True)
    id_motivo = Column(Integer, ForeignKey("motivos_retiro.id_motivo", ondelete="SET NULL"), nullable=False)
    id_autorizacion = Column(Integer, ForeignKey("autorizaciones_retiro.id_autorizacion", ondelete="SET NULL"), unique=True, nullable=True)
    
    # NUEVOS CAMPOS
    tipo_solicitud = Column(Enum(TipoSolicitudEnum), nullable=False, default="individual", index=True)
    foto_evidencia = Column(String(500), nullable=False)  # URL o path de la foto (OBLIGATORIA)
    id_solicitante = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True, index=True)
    
    fecha_hora_salida = Column(DateTime, nullable=False, index=True)
    fecha_hora_retorno_previsto = Column(DateTime, nullable=True)
    observacion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, nullable=False)  # *** CAMBIADO de fecha_hora_solicitud ***
    
    # Campos para el flujo de aprobación
    estado = Column(Enum(EstadoSolicitudEnum), nullable=False, default="recibida", index=True)
    fecha_derivacion = Column(DateTime, nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", foreign_keys=[id_estudiante], viewonly=True)
    apoderado = relationship("Apoderado", foreign_keys=[id_apoderado], viewonly=True)
    motivo = relationship("MotivoRetiro", foreign_keys=[id_motivo], viewonly=True)
    autorizacion = relationship("AutorizacionRetiro", uselist=False, foreign_keys=[id_autorizacion], viewonly=True)
    registro_salida = relationship("RegistroSalida", uselist=False, viewonly=True)
    solicitante = relationship("Usuario", foreign_keys=[id_solicitante], viewonly=True)
    
    def __repr__(self):
        return f"<SolicitudRetiro(id={self.id_solicitud}, estudiante_id={self.id_estudiante})>"

