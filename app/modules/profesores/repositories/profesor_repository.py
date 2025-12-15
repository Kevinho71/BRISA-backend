# app/modules/profesores/repositories/profesor_repository.py
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.modules.profesores.models.profesor_models import Profesor
from app.shared.models.persona import Persona
from app.shared.models import ProfesorCursoMateria
from app.modules.estudiantes.models.Curso import Curso
from app.modules.estudiantes.models.Materia import Materia


class ProfesorRepository:
    """Repositorio para operaciones de base de datos de profesores"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Profesor]:
        """Obtiene todos los profesores con paginación"""
        return db.query(Profesor).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, id_profesor: int) -> Optional[Profesor]:
        """Obtiene un profesor por ID"""
        return db.query(Profesor).filter(Profesor.id_profesor == id_profesor).first()

    @staticmethod
    def get_by_persona_id(db: Session, id_persona: int) -> Optional[Profesor]:
        """Obtiene un profesor por ID de persona"""
        return db.query(Profesor).filter(Profesor.id_persona == id_persona).first()

    @staticmethod
    def get_persona_by_id(db: Session, id_persona: int) -> Optional[Persona]:
        """Obtiene una persona por ID"""
        return db.query(Persona).filter(Persona.id_persona == id_persona).first()

    @staticmethod
    def get_persona_by_ci(db: Session, ci: str) -> Optional[Persona]:
        """Obtiene una persona por CI"""
        return db.query(Persona).filter(Persona.ci == ci).first()

    @staticmethod
    def create_persona(db: Session, persona: Persona) -> Persona:
        """Crea una nueva persona"""
        db.add(persona)
        db.flush()  # Para obtener el ID sin hacer commit
        return persona

    @staticmethod
    def create_profesor(db: Session, profesor: Profesor) -> Profesor:
        """Crea un nuevo profesor"""
        db.add(profesor)
        db.flush()
        return profesor

    @staticmethod
    def update_persona(db: Session, persona: Persona) -> Persona:
        """Actualiza una persona"""
        db.flush()
        return persona

    @staticmethod
    def update_profesor(db: Session, profesor: Profesor) -> Profesor:
        """Actualiza un profesor"""
        db.flush()
        return profesor

    @staticmethod
    def delete(db: Session, profesor: Profesor):
     """Elimina un profesor eliminando su persona (cascada eliminará el profesor)"""
    # 1. Guardar el id_persona
     id_persona = profesor.id_persona
    
    # 2. Eliminar asignaciones primero (no hay FK CASCADE aquí)
     db.query(ProfesorCursoMateria).filter(
        ProfesorCursoMateria.id_profesor == profesor.id_profesor
     ).delete(synchronize_session=False)
    
    # 3. Eliminar la persona (esto eliminará el profesor por CASCADE)
     persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()
     if persona:
        db.delete(persona)
        db.flush()

    @staticmethod
    def get_profesores_activos(db: Session) -> List[Profesor]:
        """Obtiene todos los profesores activos"""
        return db.query(Profesor).join(Persona).filter(Persona.is_active == True).all()

    @staticmethod
    def get_profesores_por_nivel(db: Session, nivel: str) -> List[Profesor]:
        """Obtiene profesores por nivel de enseñanza"""
        return db.query(Profesor).filter(Profesor.nivel_enseñanza == nivel).all()

    # ==================== ASIGNACIÓN CURSO-MATERIA ====================

    @staticmethod
    def asignar_curso_materia(db: Session, asignacion: ProfesorCursoMateria) -> ProfesorCursoMateria:
        """Asigna un curso y materia a un profesor"""
        db.add(asignacion)
        db.flush()
        return asignacion

    @staticmethod
    def get_asignacion(db: Session, id_profesor: int, id_curso: int, id_materia: int) -> Optional[ProfesorCursoMateria]:
        """Obtiene una asignación específica"""
        return db.query(ProfesorCursoMateria).filter(
            ProfesorCursoMateria.id_profesor == id_profesor,
            ProfesorCursoMateria.id_curso == id_curso,
            ProfesorCursoMateria.id_materia == id_materia
        ).first()

    @staticmethod
    def get_asignaciones_profesor(db: Session, id_profesor: int) -> List[ProfesorCursoMateria]:
        """Obtiene todas las asignaciones de un profesor"""
        return db.query(ProfesorCursoMateria).filter(
            ProfesorCursoMateria.id_profesor == id_profesor
        ).all()

    @staticmethod
    def eliminar_asignacion(db: Session, id_profesor: int, id_curso: int, id_materia: int) -> int:
        """Elimina una asignación de curso-materia usando query directo"""
        # Usar delete directo en lugar de obtener primero y luego borrar
        result = db.query(ProfesorCursoMateria).filter(
            ProfesorCursoMateria.id_profesor == id_profesor,
            ProfesorCursoMateria.id_curso == id_curso,
            ProfesorCursoMateria.id_materia == id_materia
        ).delete(synchronize_session=False)
        
        db.flush()
        return result  # Retorna el número de filas eliminadas (0 si no encontró)

    @staticmethod
    def get_curso_by_id(db: Session, id_curso: int) -> Optional[Curso]:
        """Obtiene un curso por ID"""
        return db.query(Curso).filter(Curso.id_curso == id_curso).first()

    @staticmethod
    def get_materia_by_id(db: Session, id_materia: int) -> Optional[Materia]:
        """Obtiene una materia por ID"""
        return db.query(Materia).filter(Materia.id_materia == id_materia).first()

    @staticmethod
    def get_all_cursos(db: Session) -> List[Curso]:
        """Obtiene todos los cursos"""
        return db.query(Curso).all()

    @staticmethod
    def get_all_materias(db: Session) -> List[Materia]:
        """Obtiene todas las materias"""
        return db.query(Materia).all()

    @staticmethod
    def get_materias_por_nivel(db: Session, nivel: str) -> List[Materia]:
        """Obtiene materias por nivel"""
        return db.query(Materia).filter(Materia.nivel == nivel).all()