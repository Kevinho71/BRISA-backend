from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Profesor(Base):
    __tablename__ = "profesores"

    id_profesor = Column("id_profesor", Integer, primary_key=True, index=True)
    id_persona = Column("id_persona", Integer, ForeignKey(
        "personas.id_persona"), nullable=False, unique=True)
    especialidad = Column(String(100), nullable=True)
    titulo_academico = Column(String(100), nullable=True)
    nivel_enseñanza = Column(String(100), nullable=True)
