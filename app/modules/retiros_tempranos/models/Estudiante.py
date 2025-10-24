from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel


class Estudiante(BaseModel):
    """
    Modelo de Estudiante
    Representa la entidad estudiante con información personal y de contacto
    """
    __tablename__ = "estudiante"
    
    id_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    ci = Column(String(255), nullable=False, unique=True, index=True)
    nombres = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    telefono_contacto = Column(String(255), nullable=True)
    
    # Relaciones
    inscripciones = relationship("Inscripcion", back_populates="estudiante")
    solicitudes_retiro = relationship("SolicitudRetiro", back_populates="estudiante")
    registros_salida = relationship("RegistroSalida", back_populates="estudiante")
    apoderados = relationship("Apoderado", back_populates="estudiante")
    
    def __repr__(self):
        return f"<Estudiante(id={self.id_estudiante}, ci={self.ci}, nombres={self.nombres})>"
