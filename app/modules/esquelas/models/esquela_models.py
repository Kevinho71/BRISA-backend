# app/modules/esquelas/models/esquela_models.py
##
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.modules.profesores.models.profesor_models import Profesor
from app.shared.models.persona import Persona


class CodigoEsquela(Base):
    __tablename__ = "codigos_esquelas"

    id_codigo = Column("id_codigo", Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    codigo = Column(String(10), nullable=False, unique=True)
    descripcion = Column(Text, nullable=False)

    # Relación hacia esquelas
    esquelas = relationship(
        "Esquela",
        secondary="esquelas_codigos",
        back_populates="codigos"
    )


class Esquela(Base):
    __tablename__ = "esquelas"

    id_esquela = Column("id_esquela", Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, ForeignKey("estudiantes.id_estudiante"), nullable=False, index=True)
    id_profesor = Column(Integer, ForeignKey("profesores.id_profesor"), nullable=False, index=True)
    id_registrador = Column(Integer, ForeignKey("profesores.id_profesor"), nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    observaciones = Column(Text)

    # Relaciones
    estudiante = relationship("Estudiante", back_populates="esquelas")

    # Relaciones a Profesor (tabla profesores)
    profesor_ref = relationship(Profesor, foreign_keys=[id_profesor])
    registrador_ref = relationship(Profesor, foreign_keys=[id_registrador])

    # Exponer Persona (datos de nombres) a través de profesores.id_persona
    profesor = relationship(
        Persona,
        secondary=Profesor.__table__,
        primaryjoin=id_profesor == Profesor.id_profesor,
        secondaryjoin=Profesor.id_persona == Persona.id_persona,
        viewonly=True,
        uselist=False,
    )
    registrador = relationship(
        Persona,
        secondary=Profesor.__table__,
        primaryjoin=id_registrador == Profesor.id_profesor,
        secondaryjoin=Profesor.id_persona == Persona.id_persona,
        viewonly=True,
        uselist=False,
    )

    # Relación hacia códigos usando la tabla intermedia
    codigos = relationship(
        "CodigoEsquela",
        secondary="esquelas_codigos",
        back_populates="esquelas"
    )



class EsquelaCodigo(Base):
    __tablename__ = "esquelas_codigos"

    id_esquela = Column(Integer, ForeignKey("esquelas.id_esquela"), primary_key=True)
    id_codigo = Column(Integer, ForeignKey("codigos_esquelas.id_codigo"), primary_key=True)

