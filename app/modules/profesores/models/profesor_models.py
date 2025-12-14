# app/modules/profesores/models/profesor_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Profesor(Base):
    """
    Modelo de Profesor
    Extiende la información de una Persona con datos específicos de docentes
    """
    __tablename__ = "profesores"
    __table_args__ = {"extend_existing": True}

    id_profesor = Column("id_profesor", Integer, primary_key=True, autoincrement=True, index=True)
    id_persona = Column("id_persona", Integer, ForeignKey("personas.id_persona", ondelete="CASCADE"), nullable=False, unique=True)
    especialidad = Column(String(100), nullable=True)
    titulo_academico = Column(String(100), nullable=True)
    nivel_enseñanza = Column(String(100), nullable=True, default="todos")
    observaciones = Column(Text, nullable=True)

    # Relaciones
    asignaciones = relationship("ProfesorCursoMateria", back_populates="profesor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Profesor(id={self.id_profesor}, id_persona={self.id_persona}, especialidad={self.especialidad})>"