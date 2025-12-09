from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Estudiante(Base):
    """Modelo de Estudiante alineado al esquema actual."""
    __tablename__ = "estudiantes"
    __table_args__ = {"extend_existing": True}
    
    id_estudiante = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ci = Column(String(20), nullable=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(Text, nullable=True)
    nombre_padre = Column(String(100), nullable=True)
    apellido_paterno_padre = Column(String(100), nullable=True)
    apellido_materno_padre = Column(String(100), nullable=True)
    telefono_padre = Column(String(15), nullable=True)
    nombre_madre = Column(String(100), nullable=True)
    apellido_paterno_madre = Column(String(100), nullable=True)
    apellido_materno_madre = Column(String(100), nullable=True)
    telefono_madre = Column(String(15), nullable=True)
    
    # Relaciones
    inscripciones = relationship("Inscripcion", back_populates="estudiante")
    solicitudes_retiro = relationship("SolicitudRetiro", back_populates="estudiante")
    registros_salida = relationship("RegistroSalida", back_populates="estudiante")
    apoderados = relationship("EstudianteApoderado", back_populates="estudiante")
    esquelas = relationship("Esquela", back_populates="estudiante")
    cursos = relationship("Curso", secondary="estudiantes_cursos", back_populates="estudiantes")
    estudiantes_cursos = relationship("EstudianteCurso", back_populates="estudiante")
    
    def __repr__(self):
        return f"<Estudiante(id={self.id_estudiante}, ci={self.ci}, nombres={self.nombres})>"
