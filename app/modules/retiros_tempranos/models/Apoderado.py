from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Apoderado(Base):
    """
    Modelo de Apoderado
    Representa a los apoderados/tutores de los estudiantes
    """
    __tablename__ = "apoderados"
    __table_args__ = {'extend_existing': True}
    
    id_apoderado = Column(Integer, primary_key=True, autoincrement=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(50), nullable=True)
    direccion = Column(String(100), nullable=True)
    
    # Relaciones
    estudiantes_apoderados = relationship("EstudianteApoderado", back_populates="apoderado")
    solicitudes_retiro = relationship("SolicitudRetiro", back_populates="apoderado")
    
    def __repr__(self):
        return f"<Apoderado(id={self.id_apoderado}, nombres={self.nombres} {self.apellidos})>"

