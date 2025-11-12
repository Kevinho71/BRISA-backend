from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.core.extensions import Base
import enum


class TipoPersonaEnum(str, enum.Enum):
    """Enumeración para tipos de persona"""
    profesor = "profesor"
    administrativo = "administrativo"


class Persona(Base):
    """
    Modelo de Persona
    Representa a profesores y personal administrativo
    """
    __tablename__ = "personas"
    
    id_persona = Column(Integer, primary_key=True, autoincrement=True)
    ci = Column(String(20), nullable=False)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    direccion = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(50), unique=True, nullable=True)
    tipo_persona = Column(Enum(TipoPersonaEnum), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relaciones
    # TODO: Descomentar cuando se implemente el módulo de autenticación
    # usuario = relationship("Usuario", back_populates="persona", uselist=False)
    autorizaciones_retiro = relationship("AutorizacionRetiro", back_populates="persona_decidio", foreign_keys="AutorizacionRetiro.decidido_por")
    profesores_cursos_materias = relationship("ProfesorCursoMateria", back_populates="profesor")
    
    def __repr__(self):
        return f"<Persona(id={self.id_persona}, nombres={self.nombres} {self.apellido_paterno}, tipo={self.tipo_persona})>"
