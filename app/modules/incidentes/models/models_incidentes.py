# app\modules\incidentes\models\models_incidentes.py

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Enum,
    ForeignKey, Table
)
from app.core.database import Base
from sqlalchemy import Text as SQLText
from sqlalchemy.orm import relationship
from datetime import datetime

# TABLAS INTERMEDIAS

incidentes_estudiantes = Table(
    'incidentes_estudiantes',
    Base.metadata,
    Column('id_incidente', Integer, ForeignKey('incidentes.id_incidente'), primary_key=True),
    Column('id_estudiante', Integer, ForeignKey('estudiantes.id_estudiante'), primary_key=True)
)

incidentes_profesores = Table(
    'incidentes_profesores',
    Base.metadata,
    Column('id_incidente', Integer, ForeignKey('incidentes.id_incidente'), primary_key=True),
    Column('id_profesor', Integer, ForeignKey('personas.id_persona'), primary_key=True)
)

incidentes_situaciones = Table(
    'incidentes_situaciones',
    Base.metadata,
    Column('id_incidente', Integer, ForeignKey('incidentes.id_incidente'), primary_key=True),
    Column('id_situacion', Integer, ForeignKey('situaciones_incidente.id_situacion'), primary_key=True)
)

# MODELOS

class AreaIncidente(Base):
    __tablename__ = "areas_incidente"

    id_area = Column(Integer, primary_key=True, autoincrement=True)
    nombre_area = Column(String(50), nullable=False)
    descripcion = Column(String(255))

    situaciones = relationship("SituacionIncidente", back_populates="area")


class SituacionIncidente(Base):
    __tablename__ = "situaciones_incidente"

    id_situacion = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey("areas_incidente.id_area"), nullable=False)
    nombre_situacion = Column(String(50), nullable=False)
    nivel_gravedad = Column(
        Enum("leve", "grave", "muy grave", name="nivel_gravedad"), nullable=False
    )

    area = relationship("AreaIncidente", back_populates="situaciones")
    incidentes = relationship(
        "Incidente",
        secondary=incidentes_situaciones,
        back_populates="situaciones"
    )

class Incidente(Base):
    __tablename__ = "incidentes"

    id_incidente = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    antecedentes = Column(Text)
    acciones_tomadas = Column(Text)
    seguimiento = Column(Text)

    estado = Column(
        Enum("abierto", "derivado", "cerrado", name="estado_incidente"),
        nullable=False
    )

    id_responsable = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    responsable = relationship(
        "Usuario",
        backref="incidentes_creados",
        foreign_keys=[id_responsable]
    )

    estudiantes = relationship(
        "Estudiante",
        secondary=incidentes_estudiantes,
        backref="incidentes"
    )

    profesores = relationship(
        "Persona",
        secondary=incidentes_profesores,
        backref="incidentes_asignados"
    )

    situaciones = relationship(
        "SituacionIncidente",
        secondary=incidentes_situaciones,
        back_populates="incidentes"
    )

    adjuntos = relationship(
        "Adjunto",
        back_populates="incidente",
        cascade="all, delete-orphan"
    )


class HistorialDeModificacion(Base):
    __tablename__ = "historial_de_modificaciones"

    id_historial = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    fecha_cambio = Column(DateTime, default=datetime.utcnow)
    campo_modificado = Column(String(100))
    valor_anterior = Column(SQLText, nullable=True)
    valor_nuevo = Column(SQLText, nullable=True)


class Derivacion(Base):
    __tablename__ = "derivaciones"

    id_derivacion = Column(Integer, primary_key=True, autoincrement=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)

    id_quien_deriva = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_quien_recibe = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    fecha_derivacion = Column(DateTime, default=datetime.utcnow)
    observaciones = Column(Text)

    incidente = relationship("Incidente", backref="derivaciones")


class Adjunto(Base):
    __tablename__ = "adjuntos"

    id_adjunto = Column(Integer, primary_key=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)

    nombre_archivo = Column(String(200))
    ruta = Column(String(300))
    tipo_mime = Column(String(50), nullable=True)

    id_subido_por = Column(Integer, ForeignKey("usuarios.id_usuario"))
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    incidente = relationship("Incidente", back_populates="adjuntos")
