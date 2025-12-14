from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel
from app.core.database import Base


class EstudianteCurso(Base):
    """
    Modelo de Estudiante-Curso (tabla intermedia)
    Relación N:N entre estudiantes y cursos
    """
    __tablename__ = "estudiantes_cursos"
    __table_args__ = {'extend_existing': True}

    id_estudiante = Column(Integer, ForeignKey(
        "estudiantes.id_estudiante", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso",
                      ondelete="CASCADE"), primary_key=True, nullable=False)

    # Relaciones
    estudiante = relationship(
        "Estudiante", back_populates="estudiantes_cursos", overlaps="cursos,estudiantes")
    curso = relationship(
        "Curso", back_populates="estudiantes_cursos", overlaps="cursos,estudiantes")

    def __repr__(self):
        return f"<EstudianteCurso(estudiante_id={self.id_estudiante}, curso_id={self.id_curso})>"
