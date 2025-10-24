from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel


class RegistroSalida(BaseModel):
    """
    Modelo de Registro de Salida
    Representa el registro de salidas efectivas de estudiantes
    """
    __tablename__ = "registro_salida"
    
    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante", ondelete="CASCADE"), nullable=False)
    salida_en = Column(Date, nullable=False)
    retorno_en = Column(Date, nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="registros_salida")
    solicitudes = relationship("SolicitudRetiro", back_populates="registro_salida")
    
    def __repr__(self):
        return f"<RegistroSalida(id={self.id_registro}, estudiante_id={self.id_estudiante})>"
