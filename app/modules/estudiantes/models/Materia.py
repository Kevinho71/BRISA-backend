
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel


class Materia(BaseModel):
    """
    Modelo de Materia
    Representa las materias académicas
    """
    __tablename__ = "materia"
    
    id_materia = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    area = Column(String(255), nullable=False)
    nivel = Column(String(255), nullable=False)
    
    # Relaciones
    solicitudes_retiro_detalle = relationship("SolicitudRetiroDetalle", back_populates="materia")
    
    def __repr__(self):
        return f"<Materia(id={self.id_materia}, nombre={self.nombre}, area={self.area})>"
