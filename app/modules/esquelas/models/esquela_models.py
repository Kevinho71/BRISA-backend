# app/modules/esquelas/models/esquela_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table
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
    # Campos opcionales para asignar la esquela después
    # TODO: Agregar ForeignKey cuando los módulos estudiantes, personas y usuarios estén implementados
    id_estudiante = Column(Integer, nullable=True)  # ForeignKey("estudiantes.id_estudiante")
    id_profesor = Column(Integer, nullable=True)  # ForeignKey("personas.id_persona")
    id_registrador = Column(Integer, nullable=True)  # ForeignKey("usuarios.id_usuario")
    fecha = Column(DateTime, nullable=False)
    observaciones = Column(Text)

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
