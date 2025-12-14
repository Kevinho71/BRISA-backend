# app/shared/models/profesor_curso_materia.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProfesorCursoMateria(Base):
    """
    Modelo de Profesor-Curso-Materia (tabla intermedia)
    Relación entre profesores, cursos y materias que imparten
    """
    __tablename__ = "profesores_cursos_materias"
    __table_args__ = {"extend_existing": True}
    
    # Define las columnas sin usar Column() en el nombre de variable
    id_profesor = Column("id_profesor", Integer, ForeignKey("profesores.id_profesor", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_curso = Column("id_curso", Integer, ForeignKey("cursos.id_curso", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_materia = Column("id_materia", Integer, ForeignKey("materias.id_materia", ondelete="CASCADE"), primary_key=True, nullable=False)
    
    # Relaciones usando strings para lazy loading
    profesor = relationship("Profesor", back_populates="asignaciones")
    curso = relationship("Curso", back_populates="profesores_cursos_materias")
    materia = relationship("Materia", back_populates="profesores_cursos_materias")
    
    def __repr__(self):
        return f"<ProfesorCursoMateria(profesor_id={self.id_profesor}, curso_id={self.id_curso}, materia_id={self.id_materia})>"