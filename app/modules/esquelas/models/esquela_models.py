# app/modules/esquelas/models/esquela_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table, Date
from sqlalchemy.orm import relationship
from app.core.extensions import Base


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
    id_profesor = Column(Integer, ForeignKey("personas.id_persona"), nullable=False, index=True)
    id_registrador = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    observaciones = Column(Text)

    # Relaciones
    estudiante = relationship("Estudiante", back_populates="esquelas")
    profesor = relationship("Persona", foreign_keys=[id_profesor], back_populates="esquelas_profesor")
    registrador = relationship("Persona", foreign_keys=[id_registrador], back_populates="esquelas_registrador")
    
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
