from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.models.base_models import BaseModel

class Apoderado(BaseModel):
    """
    Modelo de Apoderado
    Representa a los apoderados/tutores de los estudiantes
    """
    __tablename__ = "apoderado"
    
    id_apoderado = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante", ondelete="CASCADE"), nullable=False)
    parentesco = Column(String(255), nullable=False)
    nombres = Column(String(255), nullable=False)
    apellidos = Column(String(255), nullable=False)
    ci = Column(String(255), nullable=False)
    telefono = Column(String(255), nullable=False)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="apoderados")
    
    def __repr__(self):
        return f"<Apoderado(id={self.id_apoderado}, nombres={self.nombres} {self.apellidos})>"

