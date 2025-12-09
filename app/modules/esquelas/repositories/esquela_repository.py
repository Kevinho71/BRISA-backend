# app/modules/esquelas/repositories/esquela_repository.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, func, and_, or_, extract
from app.modules.esquelas.models.esquela_models import Esquela, CodigoEsquela
from app.modules.administracion.models.persona_models import Estudiante, estudiantes_cursos
from app.shared.models.persona import Persona
from app.modules.estudiantes.models.Curso import Curso
from datetime import datetime, date
from typing import Optional, List, Dict, Any


class EsquelaRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Esquela).options(
            joinedload(Esquela.codigos),
            joinedload(Esquela.estudiante),
            joinedload(Esquela.profesor)
        ).all()

    @staticmethod
    def get_by_profesor(db: Session, id_profesor: int) -> List[Esquela]:
        """Obtiene todas las esquelas de un profesor específico"""
        return db.query(Esquela).options(
            joinedload(Esquela.codigos),
            joinedload(Esquela.estudiante),
            joinedload(Esquela.profesor)
        ).filter(
            Esquela.id_profesor == id_profesor
        ).order_by(Esquela.fecha.desc()).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Esquela).options(
            joinedload(Esquela.codigos),
            joinedload(Esquela.estudiante),
            joinedload(Esquela.profesor)
        ).filter(Esquela.id_esquela == id).first()

    @staticmethod
    def get_with_filters(
        db: Session,
        name: Optional[str] = None,
        course_id: Optional[int] = None,
        tipo: Optional[str] = None,  # 'reconocimiento' u 'orientacion'
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
        id_profesor: Optional[int] = None  # NUEVO: filtro por profesor
    ):
        """
        Obtiene esquelas con filtros avanzados y paginación
        NOTA: Filtrado por curso se hace a través de estudiantes_cursos
        
        Args:
            id_profesor: Si se proporciona, filtra por profesor específico
        """
        query = db.query(Esquela).options(
            joinedload(Esquela.codigos),
            joinedload(Esquela.estudiante),
            joinedload(Esquela.profesor)
        )

        # NUEVO: Filtro por profesor
        if id_profesor:
            query = query.filter(Esquela.id_profesor == id_profesor)

        # Filtro por nombre de estudiante
        if name:
            query = query.join(Esquela.estudiante).filter(
                or_(
                    Estudiante.nombres.ilike(f'%{name}%'),
                    Estudiante.apellido_paterno.ilike(f'%{name}%'),
                    Estudiante.apellido_materno.ilike(f'%{name}%')
                )
            )

        # Filtro por curso - a través de la tabla estudiantes_cursos
        if course_id:
            # Subquery para obtener IDs de estudiantes del curso
            estudiantes_del_curso = db.query(estudiantes_cursos.c.id_estudiante).filter(
                estudiantes_cursos.c.id_curso == course_id
            ).subquery()
            
            query = query.filter(Esquela.id_estudiante.in_(estudiantes_del_curso))

        # Filtro por tipo de esquela (reconocimiento u orientación)
        if tipo:
            query = query.join(Esquela.codigos).filter(
                CodigoEsquela.tipo == tipo
            ).distinct()

        # Filtros de fecha
        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        # Filtro por año
        if year:
            query = query.filter(extract('year', Esquela.fecha) == year)

        # Filtro por mes
        if month:
            query = query.filter(extract('month', Esquela.fecha) == month)

        # Contar total antes de paginar
        total = query.count()

        # Paginación
        offset = (page - 1) * page_size
        esquelas = query.order_by(Esquela.fecha.desc()).offset(offset).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
            "data": esquelas
        }

    @staticmethod
    def get_aggregate_by_course(db: Session, year: Optional[int] = None):
        """
        Obtiene la cantidad de esquelas de reconocimiento y orientación por curso
        Ejemplo: Curso 1A = 5R, 2O
        NOTA: Join a través de estudiantes → estudiantes_cursos → cursos
        """
        query = db.query(
            Curso.id_curso,
            Curso.nombre_curso,
            CodigoEsquela.tipo,
            func.count(Esquela.id_esquela).label('cantidad')
        ).select_from(Curso).join(
            estudiantes_cursos, Curso.id_curso == estudiantes_cursos.c.id_curso
        ).join(
            Estudiante, Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
        ).join(
            Esquela, Esquela.id_estudiante == Estudiante.id_estudiante
        ).join(
            Esquela.codigos
        )

        # Filtro por año si se proporciona
        if year:
            query = query.filter(extract('year', Esquela.fecha) == year)

        query = query.group_by(
            Curso.id_curso,
            Curso.nombre_curso,
            CodigoEsquela.tipo
        ).order_by(Curso.nombre_curso)

        results = query.all()

        # Transformar resultados al formato requerido
        curso_stats = {}
        for curso_id, nombre_curso, tipo, cantidad in results:
            if nombre_curso not in curso_stats:
                curso_stats[nombre_curso] = {
                    "curso_id": curso_id,
                    "curso": nombre_curso,
                    "reconocimiento": 0,
                    "orientacion": 0
                }
            
            if tipo == "reconocimiento":
                curso_stats[nombre_curso]["reconocimiento"] = cantidad
            elif tipo == "orientacion":
                curso_stats[nombre_curso]["orientacion"] = cantidad

        return list(curso_stats.values())

    @staticmethod
    def get_by_student_with_date_range(
        db: Session,
        student_id: int,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene todas las esquelas de un estudiante en un rango de fechas
        con conteo de códigos
        """
        query = db.query(Esquela).options(
            joinedload(Esquela.codigos),
            joinedload(Esquela.estudiante),
            joinedload(Esquela.profesor)
        ).filter(Esquela.id_estudiante == student_id)

        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        esquelas = query.order_by(Esquela.fecha.desc()).all()

        # Contar códigos por tipo usando subquery
        from app.modules.esquelas.models.esquela_models import EsquelaCodigo
        
        codigo_count_query = db.query(
            CodigoEsquela.tipo,
            func.count(CodigoEsquela.id_codigo).label('cantidad')
        ).select_from(Esquela).join(
            EsquelaCodigo, Esquela.id_esquela == EsquelaCodigo.id_esquela
        ).join(
            CodigoEsquela, EsquelaCodigo.id_codigo == CodigoEsquela.id_codigo
        ).filter(
            Esquela.id_estudiante == student_id
        )

        if fecha_desde:
            codigo_count_query = codigo_count_query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            codigo_count_query = codigo_count_query.filter(Esquela.fecha <= fecha_hasta)

        codigo_count = codigo_count_query.group_by(CodigoEsquela.tipo).all()

        codigos_resumen = {tipo: cantidad for tipo, cantidad in codigo_count}

        return {
            "total": len(esquelas),
            "esquelas": esquelas,
            "codigos_resumen": codigos_resumen
        }

    @staticmethod
    def get_aggregate_by_year_month(db: Session, group_by: str = "year"):
        """
        Obtiene agregación de esquelas por año o mes
        Para drilldown: año → mes
        """
        if group_by == "year":
            results = db.query(
                extract('year', Esquela.fecha).label('year'),
                func.count(Esquela.id_esquela).label('total')
            ).group_by(extract('year', Esquela.fecha)).order_by(extract('year', Esquela.fecha)).all()
            
            return [{"year": int(year), "total": total} for year, total in results]
            
        elif group_by == "month":
            results = db.query(
                extract('year', Esquela.fecha).label('year'),
                extract('month', Esquela.fecha).label('month'),
                func.count(Esquela.id_esquela).label('total')
            ).group_by(
                extract('year', Esquela.fecha),
                extract('month', Esquela.fecha)
            ).order_by(
                extract('year', Esquela.fecha),
                extract('month', Esquela.fecha)
            ).all()
            
            return [{"year": int(year), "month": int(month), "total": total} for year, month, total in results]
        else:
            return []

    @staticmethod
    def create(db: Session, esquela: Esquela, codigo_ids: list[int]):
        db.add(esquela)
        db.commit()
        db.refresh(esquela)

        # Insertar relaciones en la tabla intermedia usando SQL directo
        for cid in codigo_ids:
            db.execute(
                text("INSERT INTO esquelas_codigos (id_esquela, id_codigo) VALUES (:id_esquela, :id_codigo)"),
                {"id_esquela": esquela.id_esquela, "id_codigo": cid}
            )
        db.commit()
        db.refresh(esquela)  # Refrescar para cargar las relaciones
        return esquela

    @staticmethod
    def delete(db: Session, id: int):
        esquela = db.query(Esquela).filter(Esquela.id_esquela == id).first()
        if esquela:
            db.delete(esquela)
            db.commit()
        return esquela

