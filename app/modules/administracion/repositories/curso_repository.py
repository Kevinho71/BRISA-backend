# app/modules/administracion/repositories/curso_repository.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.modules.administracion.models.persona_models import Curso, Estudiante, Persona
from typing import Optional


class CursoRepository:

    @staticmethod
    def get_all(db: Session):
        """Obtiene todos los cursos"""
        return db.query(Curso).order_by(Curso.nombre_curso).all()

    @staticmethod
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
        query = db.query(Estudiante).join(
            Estudiante.cursos
        ).filter(Curso.id_curso == curso_id)

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
