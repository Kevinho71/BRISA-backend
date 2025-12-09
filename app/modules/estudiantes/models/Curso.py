from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Curso(Base):
    """
    Modelo de Curso
    Representa los cursos disponibles en la institución
    """
    __tablename__ = "cursos"
    
    __table_args__ = {"extend_existing": True}

    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nombre_curso = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)
    gestion = Column(String(20), nullable=False)
    
    # Relaciones
    estudiantes = relationship("Estudiante", secondary="estudiantes_cursos", back_populates="cursos")
    estudiantes_cursos = relationship("EstudianteCurso", back_populates="curso")
    profesores_cursos_materias = relationship("ProfesorCursoMateria", back_populates="curso")
    solicitudes_retiro_detalle = relationship("SolicitudRetiroDetalle", back_populates="curso")
    
    def __repr__(self):
        return f"<Curso(id={self.id_curso}, nombre={self.nombre_curso}, nivel={self.nivel})>"

