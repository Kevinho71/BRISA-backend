# app/modules/administracion/models/persona_models.py
"""Modelos para estudiantes y personas (profesores/registradores)"""

from sqlalchemy import Column, Integer, String, Date, Text
from app.core.database import Base

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
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo"""
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"


class Persona(Base):
    """Modelo para personas (profesores y administrativos)"""
    __tablename__ = "personas"
    __table_args__ = {'extend_existing': True} 
    id_persona = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    direccion = Column(Text, nullable=True)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(120), nullable=True)
    tipo_persona = Column(String(50), nullable=False)  # 'profesor' o 'administrativo'
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo"""
        apellidos = f"{self.apellido_paterno} {self.apellido_materno or ''}".strip()
        return f"{self.nombres} {apellidos}"
