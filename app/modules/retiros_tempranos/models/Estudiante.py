from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel


class Estudiante(BaseModel):
    """
    Modelo de Estudiante
    Representa la entidad estudiante con información personal y de contacto
    """
    __tablename__ = "estudiantes"
    
    id_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    ci = Column(String(20), nullable=True)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(String(100), nullable=True)
    nombre_padre = Column(String(50), nullable=True)
    apellido_paterno_padre = Column(String(50), nullable=True)
    apellido_materno_padre = Column(String(50), nullable=True)
    telefono_padre = Column(String(20), nullable=True)
    nombre_madre = Column(String(50), nullable=True)
    apellido_paterno_madre = Column(String(50), nullable=True)
    apellido_materno_madre = Column(String(50), nullable=True)
    telefono_madre = Column(String(20), nullable=True)
    
    # Relaciones
    solicitudes_retiro = relationship("SolicitudRetiro", back_populates="estudiante")
    registros_salida = relationship("RegistroSalida", back_populates="estudiante")
    estudiantes_apoderados = relationship("EstudianteApoderado", back_populates="estudiante")
    estudiantes_cursos = relationship("EstudianteCurso", back_populates="estudiante")
    
    def __repr__(self):
        return f"<Estudiante(id={self.id_estudiante}, ci={self.ci}, nombres={self.nombres} {self.apellido_paterno})>"
