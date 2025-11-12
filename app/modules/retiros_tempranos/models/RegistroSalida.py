from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.extensions import Base


class RegistroSalida(Base):
    """
    Modelo de Registro de Salida
    Representa el registro de salidas efectivas de estudiantes
    """
    __tablename__ = "registros_salida"
    
    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_solicitud = Column(Integer, ForeignKey("solicitudes_retiro.id_solicitud", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), nullable=False, index=True)
    fecha_hora_salida_real = Column(DateTime, nullable=False)
    fecha_hora_retorno_real = Column(DateTime, nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="registros_salida")
    solicitud = relationship("SolicitudRetiro", back_populates="registro_salida")
    
    def __repr__(self):
        return f"<RegistroSalida(id={self.id_registro}, estudiante_id={self.id_estudiante})>"
