from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.modules.profesores.models.profesor_models import Profesor

# 👇 Importaciones explícitas de los modelos relacionados
from app.modules.estudiantes.models.Curso import Curso
from app.modules.estudiantes.models.Materia import Materia

class ProfesorCursoMateria(Base):
    """
    Modelo de Profesor-Curso-Materia (tabla intermedia)
    Relación entre profesores, cursos y materias que imparten
    """
    __tablename__ = "profesores_cursos_materias"
    __table_args__ = {"extend_existing": True}
    
    id_profesor = Column(Integer, ForeignKey("profesores.id_profesor", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_materia = Column(Integer, ForeignKey("materias.id_materia", ondelete="CASCADE"), primary_key=True, nullable=False)
    
    # Relaciones
    profesor = relationship(Profesor)
    # 👇 Se usa la clase Curso importada, no una cadena
    curso = relationship(Curso, back_populates="profesores_cursos_materias")
    # 👇 Se usa la clase Materia importada, no una cadena
    materia = relationship(Materia, back_populates="profesores_cursos_materias")
    
    def __repr__(self):
        return f"<ProfesorCursoMateria(profesor_id={self.id_profesor}, curso_id={self.id_curso}, materia_id={self.id_materia})>"