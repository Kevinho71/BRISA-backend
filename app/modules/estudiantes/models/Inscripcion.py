from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel

class Inscripcion(BaseModel):
    """
    Modelo de Inscripción
    Representa la inscripción de un estudiante a un curso
    """
    __tablename__ = "inscripcion"
    
    id_inscripcion = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante", ondelete="CASCADE"), nullable=False)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="CASCADE"), nullable=False)
    fecha_inscripcion = Column(Date, nullable=False)
    estado = Column(String(255), nullable=False)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="inscripciones")
    curso = relationship("Curso", back_populates="inscripciones")
    
    def __repr__(self):
        return f"<Inscripcion(id={self.id_inscripcion}, estudiante_id={self.id_estudiante}, curso_id={self.id_curso})>"
