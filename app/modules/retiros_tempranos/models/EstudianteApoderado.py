from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class EstudianteApoderado(Base):
    """
    Modelo de Estudiante-Apoderado (tabla intermedia)
    Relación N:N entre estudiantes y apoderados con información adicional
    """
    __tablename__ = "estudiantes_apoderados"
    __table_args__ = {'extend_existing': True}
    
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_apoderado = Column(Integer, ForeignKey("apoderados.id_apoderado", ondelete="CASCADE"), primary_key=True, nullable=False)
    parentesco = Column(String(50), nullable=False)
    es_contacto_principal = Column(Boolean, default=False, nullable=True)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="estudiantes_apoderados")
    apoderado = relationship("Apoderado", back_populates="estudiantes_apoderados")
    
    def __repr__(self):
        return f"<EstudianteApoderado(estudiante_id={self.id_estudiante}, apoderado_id={self.id_apoderado}, parentesco={self.parentesco})>"
