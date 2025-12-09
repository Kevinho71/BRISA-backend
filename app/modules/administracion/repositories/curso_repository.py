# app/modules/administracion/repositories/curso_repository.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.modules.administracion.models.persona_models import Estudiante
from app.modules.estudiantes.models.Curso import Curso
from app.shared.models.persona import Persona
from typing import Optional


class CursoRepository:

    @staticmethod
    def get_all(db: Session):
        """Obtiene todos los cursos"""
        return db.query(Curso).order_by(Curso.nombre_curso).all()

    @staticmethod
    def get_by_profesor(db: Session, id_persona: int):
        """Obtiene los cursos asignados a un profesor específico"""
        from app.shared.models.profesor_curso_materia import ProfesorCursoMateria
        return db.query(Curso).join(
            ProfesorCursoMateria
        ).filter(
            ProfesorCursoMateria.id_profesor == id_persona
        ).order_by(Curso.nombre_curso).all()
    

    def get_by_id(db: Session, curso_id: int):
        """Obtiene un curso por ID"""
        return db.query(Curso).filter(Curso.id_curso == curso_id).first()

    @staticmethod
    def get_estudiantes_by_curso(
        db: Session,
        curso_id: int,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ):
        """
        Obtiene los estudiantes de un curso con filtro opcional por nombre
        """
        from app.modules.administracion.models.persona_models import estudiantes_cursos
        
        # Primero verificar si hay registros en estudiantes_cursos
        count_ec = db.query(estudiantes_cursos).filter(
            estudiantes_cursos.c.id_curso == curso_id
        ).count()
        
        # Usar la tabla intermedia explícitamente
        query = db.query(Estudiante).join(
            estudiantes_cursos,
            Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
        ).filter(
            estudiantes_cursos.c.id_curso == curso_id
        )

        # Filtro por nombre
        if name:
            query = query.filter(
                or_(
                    Estudiante.nombres.ilike(f'%{name}%'),
                    Estudiante.apellido_paterno.ilike(f'%{name}%'),
                    Estudiante.apellido_materno.ilike(f'%{name}%')
                )
            )

        # Contar total
        total = query.count()

        # Paginación
        offset = (page - 1) * page_size
        estudiantes = query.order_by(
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno,
            Estudiante.nombres
        ).offset(offset).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "data": estudiantes
        }

    @staticmethod
    def get_profesores_by_curso(
        db: Session,
        curso_id: int,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ):
        """
        Obtiene los profesores de un curso con filtro opcional por nombre
        """
        # Consulta usando la tabla intermedia profesores_cursos_materias
        query = db.query(Persona).join(
            'profesores_cursos_materias'
        ).filter(
            Persona.tipo_persona == 'profesor'
        ).filter(
            db.query(Persona).join('profesores_cursos_materias').filter(
                db.text('profesores_cursos_materias.id_curso = :curso_id')
            ).exists()
        )

        # Filtro por nombre
        if name:
            query = query.filter(
                or_(
                    Persona.nombres.ilike(f'%{name}%'),
                    Persona.apellido_paterno.ilike(f'%{name}%'),
                    Persona.apellido_materno.ilike(f'%{name}%')
                )
            )

        # Contar total
        total = query.count()

        # Paginación
        offset = (page - 1) * page_size
        profesores = query.order_by(
            Persona.apellido_paterno,
            Persona.apellido_materno,
            Persona.nombres
        ).offset(offset).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "data": profesores
        }
    
    @staticmethod
    def get_curso_by_estudiante(db: Session, id_estudiante: int) -> Optional[Curso]:
        """Obtiene el curso de un estudiante (asume que el estudiante está en un solo curso)"""
        from app.modules.administracion.models.persona_models import estudiantes_cursos
        
        curso = db.query(Curso).join(
            estudiantes_cursos,
            Curso.id_curso == estudiantes_cursos.c.id_curso
        ).filter(
            estudiantes_cursos.c.id_estudiante == id_estudiante
        ).first()
        
        return curso
