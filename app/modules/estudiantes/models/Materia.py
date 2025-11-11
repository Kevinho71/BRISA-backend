from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel
import enum


class NivelEnum(str, enum.Enum):
    """Enumeración para niveles educativos"""
    INICIAL = "inicial"
    PRIMARIA = "primaria"
    SECUNDARIA = "secundaria"


class Materia(BaseModel):
    """
    Modelo de Materia
    Representa las materias académicas
    """
    __tablename__ = "materias"
    
    id_materia = Column(Integer, primary_key=True, autoincrement=True)
    nombre_materia = Column(String(50), nullable=False)
    nivel = Column(Enum(NivelEnum), nullable=False)
    
    # Relaciones
    profesores_cursos_materias = relationship("ProfesorCursoMateria", back_populates="materia")
    solicitudes_retiro_detalle = relationship("SolicitudRetiroDetalle", back_populates="materia")
    
    def __repr__(self):
        return f"<Materia(id={self.id_materia}, nombre={self.nombre_materia}, nivel={self.nivel})>"
