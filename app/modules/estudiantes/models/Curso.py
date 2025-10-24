from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel

class Curso(BaseModel):
    """
    Modelo de Curso
    Representa los cursos disponibles en la institución
    """
    __tablename__ = "curso"
    
    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    nivel = Column(String(255), nullable=False)
    gestion = Column(String(255), nullable=False)
    paralelo = Column(String(255), nullable=False)
    
    # Relaciones
    inscripciones = relationship("Inscripcion", back_populates="curso")
    solicitudes_retiro_detalle = relationship("SolicitudRetiroDetalle", back_populates="curso")
    
    def __repr__(self):
        return f"<Curso(id={self.id_curso}, nombre={self.nombre}, nivel={self.nivel})>"

