# app/modules/administracion/services/persona_service.py
"""Servicios para lógica de negocio de personas"""

from sqlalchemy.orm import Session
from typing import List
from app.modules.administracion.models.persona_models import Estudiante, Persona
from app.modules.administracion.repositories.persona_repository import (
    EstudianteRepository,
    PersonaRepository
)


class EstudianteService:
    """Servicio para lógica de negocio de estudiantes"""

    @staticmethod
    def listar_estudiantes(db: Session) -> List[Estudiante]:
        """Listar todos los estudiantes"""
        return EstudianteRepository.get_all(db)

    @staticmethod
    def obtener_estudiante(db: Session, id_estudiante: int):
        """Obtener un estudiante por ID"""
        return EstudianteRepository.get_by_id(db, id_estudiante)


class ProfesorService:
    """Servicio para lógica de negocio de profesores"""

    @staticmethod
    def listar_profesores(db: Session) -> List[Persona]:
        """Listar todos los profesores"""
        return PersonaRepository.get_profesores(db)

    @staticmethod
    def obtener_profesor(db: Session, id_persona: int):
        """Obtener un profesor por ID"""
        return PersonaRepository.get_by_id(db, id_persona)


class RegistradorService:
    """Servicio para lógica de negocio de registradores"""

    @staticmethod
    def listar_registradores(db: Session) -> List[Persona]:
        """Listar todos los registradores (administrativos)"""
        return PersonaRepository.get_administrativos(db)

    @staticmethod
    def obtener_registrador(db: Session, id_persona: int):
        """Obtener un registrador por ID"""
        return PersonaRepository.get_by_id(db, id_persona)
