# app\shared\models\persona.py
##
from sqlalchemy import Column, Integer, String, Boolean, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
# Garantizamos que la tabla cargos esté registrada en el metadata
from app.shared.models.cargo import Cargo  # noqa: F401
import enum


class TipoPersonaEnum(str, enum.Enum):
    """Enumeración para tipos de persona"""
    profesor = "profesor"
    administrativo = "administrativo"
    apoderado = "apoderado"


class EstadoLaboralEnum(str, enum.Enum):
    """Estados laborales compatibles con la tabla `personas`."""
    activo = "activo"
    retirado = "retirado"
    licencia = "licencia"
    suspendido = "suspendido"


class Persona(Base):
    """
    Modelo de Persona
    Representa a profesores y personal administrativo
    """
    __tablename__ = "personas"
    __table_args__ = {"extend_existing": True}
    
    id_persona = Column(Integer, primary_key=True, autoincrement=True)
    ci = Column(String(20), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(120), nullable=True)
    tipo_persona = Column(Enum(TipoPersonaEnum), nullable=False)
    id_cargo = Column(Integer, ForeignKey("cargos.id_cargo"), nullable=True)
    estado_laboral = Column(Enum(EstadoLaboralEnum), nullable=True, default=EstadoLaboralEnum.activo)
    # El nombre real de la columna en BD usa "ñ"
    anos_experiencia = Column("años_experiencia", Integer, nullable=True, default=0)
    fecha_ingreso = Column(Date, nullable=True)
    fecha_retiro = Column(Date, nullable=True)
    motivo_retiro = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relaciones
    # Nota: las asignaciones profesor-curso-materia se enlazan desde la tabla `profesores`
    # (porque `profesores_cursos_materias.id_profesor` referencia `profesores.id_profesor`).
    
    def __repr__(self):
        return f"<Persona(id={self.id_persona}, nombres={self.nombres} {self.apellido_paterno}, tipo={self.tipo_persona})>"
