# app/modules/administracion/repositories/persona_repository.py
"""Repositorios para acceso a datos de personas"""

from sqlalchemy.orm import Session
from typing import List
from app.modules.administracion.models.persona_models import Estudiante, Persona


class EstudianteRepository:
    """Repositorio para operaciones CRUD de Estudiantes"""

    @staticmethod
    def get_all(db: Session) -> List[Estudiante]:
        """Obtener todos los estudiantes"""
        return db.query(Estudiante).all()

    @staticmethod
    def get_by_id(db: Session, id_estudiante: int):
        """Obtener un estudiante por ID"""
        return db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()


class PersonaRepository:
    """Repositorio para operaciones CRUD de Personas (profesores y administrativos)"""

    @staticmethod
    def get_profesores(db: Session) -> List[Persona]:
        """Obtener todos los profesores"""
        return db.query(Persona).filter(Persona.tipo_persona == 'profesor').all()

    @staticmethod
    def get_administrativos(db: Session) -> List[Persona]:
        """Obtener todos los administrativos (registradores)"""
        return db.query(Persona).filter(Persona.tipo_persona == 'administrativo').all()

    @staticmethod
    def get_by_id(db: Session, id_persona: int):
        """Obtener una persona por ID"""
        return db.query(Persona).filter(Persona.id_persona == id_persona).first()
