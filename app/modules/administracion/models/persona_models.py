# app/modules/administracion/models/persona_models.py
"""Modelos para estudiantes y personas (profesores/registradores)"""

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.extensions import Base


# Tabla intermedia para relación muchos-a-muchos entre estudiantes y cursos
estudiantes_cursos = Table(
    'estudiantes_cursos',
    Base.metadata,
    Column('id_estudiante', Integer, ForeignKey('estudiantes.id_estudiante'), primary_key=True),
    Column('id_curso', Integer, ForeignKey('cursos.id_curso'), primary_key=True)
)

# Tabla intermedia para relación muchos-a-muchos entre profesores, cursos y materias
profesores_cursos_materias = Table(
    'profesores_cursos_materias',
    Base.metadata,
    Column('id_profesor', Integer, ForeignKey('personas.id_persona'), primary_key=True),
    Column('id_curso', Integer, ForeignKey('cursos.id_curso'), primary_key=True),
    Column('id_materia', Integer, ForeignKey('materias.id_materia'), primary_key=True)
)


class Estudiante(Base):
    """Modelo para estudiantes - adaptado a la estructura existente"""
    __tablename__ = "estudiantes"

    id_estudiante = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)
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
    
    # Relaciones
    cursos = relationship("Curso", secondary=estudiantes_cursos, back_populates="estudiantes")
    esquelas = relationship("Esquela", back_populates="estudiante")
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo"""
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"



class Persona(Base):
    """Modelo para personas (profesores y administrativos)"""
    __tablename__ = "personas"

    id_persona = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    direccion = Column(Text, nullable=True)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(120), nullable=True)
    tipo_persona = Column(String(50), nullable=False)  # 'profesor' o 'administrativo'
    
    # Relaciones
    esquelas_profesor = relationship("Esquela", foreign_keys="Esquela.id_profesor", back_populates="profesor")
    esquelas_registrador = relationship("Esquela", foreign_keys="Esquela.id_registrador", back_populates="registrador")
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo"""
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


class Curso(Base):
    """Modelo para cursos"""
    __tablename__ = "cursos"

    id_curso = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)  # 'inicial', 'primaria', 'secundaria'
    gestion = Column(String(20), nullable=False)  # Año de gestión, ej: '2024'
    
    # Relaciones
    estudiantes = relationship("Estudiante", secondary=estudiantes_cursos, back_populates="cursos")
    # NOTA: No hay relación directa con esquelas porque id_curso no existe en tabla esquelas
    
    def __repr__(self):
        return f"<Curso {self.nombre_curso} - {self.gestion}>"


class Materia(Base):
    """Modelo para materias"""
    __tablename__ = "materias"

    id_materia = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)  # 'inicial', 'primaria', 'secundaria'
    
    def __repr__(self):
        return f"<Materia {self.nombre_materia}>"

