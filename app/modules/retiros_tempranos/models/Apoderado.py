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
    id_persona = Column(Integer, ForeignKey("personas.id_persona", ondelete="SET NULL"), nullable=True, unique=True, index=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(50), nullable=True)
    direccion = Column(String(100), nullable=True)
    
    # Relaciones
    persona = relationship("Persona", foreign_keys=[id_persona], viewonly=True)
    estudiantes_apoderados = relationship("EstudianteApoderado", foreign_keys="EstudianteApoderado.id_apoderado", viewonly=True)
    solicitudes_retiro = relationship("SolicitudRetiro", foreign_keys="SolicitudRetiro.id_apoderado", viewonly=True)
    
    def __repr__(self):
        return f"<Apoderado(id={self.id_apoderado}, nombres={self.nombres} {self.apellidos})>"

