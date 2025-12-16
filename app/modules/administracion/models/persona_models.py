# app/modules/administracion/models/persona_models.py
"""Modelos para estudiantes y personas (profesores/registradores)"""

from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy import Table, ForeignKey
# Registrar tabla cargos en el metadata para resolver FK
from app.shared.models.cargo import Cargo  # noqa: F401
from sqlalchemy.orm import relationship
from app.core.database import Base
# Los imports de sqlalchemy.orm y sqlalchemy.Column están repetidos, los dejamos solo una vez arriba

# ============================================
# TABLAS INTERMEDIAS
# ============================================

# Relación muchos-a-muchos entre estudiantes y cursos
estudiantes_cursos = Table(
    'estudiantes_cursos',
    Base.metadata,
    Column('id_estudiante', Integer, ForeignKey(
        'estudiantes.id_estudiante'), primary_key=True),
    Column('id_curso', Integer, ForeignKey(
        'cursos.id_curso'), primary_key=True),
    extend_existing=True
)

# Relación muchos-a-muchos entre profesores, cursos y materias
profesores_cursos_materias = Table(
    'profesores_cursos_materias',
    Base.metadata,
    Column('id_profesor', Integer, ForeignKey(
        'profesores.id_profesor'), primary_key=True),
    Column('id_curso', Integer, ForeignKey(
        'cursos.id_curso'), primary_key=True),
    Column('id_materia', Integer, ForeignKey(
        'materias.id_materia'), primary_key=True),
    extend_existing=True
)


# ============================================
# MODELO: ESTUDIANTE
# ============================================
class Estudiante(Base):
    """Modelo para estudiantes - adaptado a la estructura existente"""
    __tablename__ = "estudiantes"
    __table_args__ = {'extend_existing': True}

    id_estudiante = Column(Integer, primary_key=True,
                           autoincrement=True, index=True)
    ci = Column(String(20), nullable=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(Text, nullable=True)
    nombre_padre = Column(String(100), nullable=True)
    apellido_paterno_padre = Column(String(100), nullable=True)
    apellido_materno_padre = Column(String(100), nullable=True)
    telefono_padre = Column(String(15), nullable=True)
    nombre_madre = Column(String(100), nullable=True)
    apellido_paterno_madre = Column(String(100), nullable=True)
    apellido_materno_madre = Column(String(100), nullable=True)
    telefono_madre = Column(String(15), nullable=True)
    estado = Column(String(20), nullable=False, default="Activo")  # Activo, Inactivo, Graduado, Retirado

    # Relaciones
    cursos = relationship("Curso", secondary=estudiantes_cursos,
                          back_populates="estudiantes", overlaps="estudiantes_cursos")
    estudiantes_cursos = relationship(
        "EstudianteCurso", back_populates="estudiante", overlaps="cursos")
    esquelas = relationship("Esquela", back_populates="estudiante")

    @property
    def nombre_completo(self):
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


# ============================================
# MODELO: PERSONA
# ============================================

# 

# ============================================
# MODELO: CURSO (Ya no está aquí, se eliminó)
# ============================================
# Curso class removed to avoid duplication with app.modules.estudiantes.models.Curso.Curso
# Please import Curso from app.modules.estudiantes.models.Curso

# ============================================
# MODELO: MATERIA (Ya no está aquí, se eliminó)
# ============================================