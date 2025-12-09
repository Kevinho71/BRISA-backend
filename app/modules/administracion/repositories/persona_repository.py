# app/modules/administracion/repositories/persona_repository.py
"""Repositorios para acceso a datos de personas"""

from sqlalchemy.orm import Session
from typing import List
from app.modules.administracion.models.persona_models import Estudiante
from app.shared.models.persona import Persona


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
    
    @staticmethod
    def get_cursos_by_profesor(db: Session, id_persona: int) -> List:
        """Obtiene los cursos donde el profesor imparte clases"""
        from app.modules.administracion.models.persona_models import Curso, profesores_cursos_materias
        
        # Query usando la tabla intermedia
        cursos = db.query(Curso).join(
            profesores_cursos_materias,
            Curso.id_curso == profesores_cursos_materias.c.id_curso
        ).filter(
            profesores_cursos_materias.c.id_profesor == id_persona
        ).distinct().order_by(Curso.nombre_curso).all()
        
        return cursos
    
    @staticmethod
    def es_profesor_del_curso(db: Session, id_profesor: int, id_curso: int) -> bool:
        """Verifica si el profesor imparte clases en el curso especificado"""
        from app.modules.administracion.models.persona_models import profesores_cursos_materias
        
        result = db.query(profesores_cursos_materias).filter(
            profesores_cursos_materias.c.id_profesor == id_profesor,
            profesores_cursos_materias.c.id_curso == id_curso
        ).first()
        
        return result is not None
