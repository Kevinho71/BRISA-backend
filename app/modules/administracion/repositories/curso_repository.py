# app/modules/administracion/repositories/curso_repository.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, text
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
    def get_by_profesor(db: Session, id_profesor: int):
        """Obtiene los cursos asignados a un profesor específico (usa `profesores.id_profesor`)."""
        rows = db.execute(
            text(
                """
                SELECT DISTINCT c.id_curso, c.nombre_curso, c.nivel, c.gestion
                FROM cursos c
                JOIN profesores_cursos_materias pcm ON pcm.id_curso = c.id_curso
                WHERE pcm.id_profesor = :id_profesor
                ORDER BY c.nombre_curso
                """
            ),
            {"id_profesor": id_profesor},
        ).mappings().all()

        # Devolver dicts compatibles con CursoDTO
        return [dict(r) for r in rows]
    

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
        # Consulta usando profesores_cursos_materias (id_profesor -> profesores.id_profesor)
        # y luego profesores.id_persona -> personas.id_persona
        from app.modules.administracion.models.persona_models import profesores_cursos_materias
        from app.modules.profesores.models.profesor_models import Profesor

        query = db.query(Persona).join(
            Profesor, Profesor.id_persona == Persona.id_persona
        ).join(
            profesores_cursos_materias, profesores_cursos_materias.c.id_profesor == Profesor.id_profesor
        ).filter(
            profesores_cursos_materias.c.id_curso == curso_id
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
        """Obtiene el curso de un estudiante.

        Nota: Históricamente se asumía 1 curso por estudiante. Si existen múltiples
        asignaciones en `estudiantes_cursos`, este método retorna uno de forma
        determinística (por id_curso asc). Para validar contra *todos* los cursos,
        usar `get_cursos_by_estudiante`.
        """
        from app.modules.administracion.models.persona_models import estudiantes_cursos
        
        curso = db.query(Curso).join(
            estudiantes_cursos,
            Curso.id_curso == estudiantes_cursos.c.id_curso
        ).filter(
            estudiantes_cursos.c.id_estudiante == id_estudiante
        ).order_by(Curso.id_curso.asc()).first()
        
        return curso

    @staticmethod
    def get_cursos_by_estudiante(db: Session, id_estudiante: int) -> list[Curso]:
        """Obtiene todos los cursos asociados a un estudiante."""
        from app.modules.administracion.models.persona_models import estudiantes_cursos

        return (
            db.query(Curso)
            .join(estudiantes_cursos, Curso.id_curso == estudiantes_cursos.c.id_curso)
            .filter(estudiantes_cursos.c.id_estudiante == id_estudiante)
            .order_by(Curso.id_curso.asc())
            .all()
        )
