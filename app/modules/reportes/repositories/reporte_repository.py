# app/modules/reportes/repositories/reporte_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.modules.esquelas.models.esquela_models import Esquela, CodigoEsquela, EsquelaCodigo
from app.modules.administracion.models.persona_models import Estudiante, Curso, estudiantes_cursos
from datetime import date
from typing import Optional, Literal


class ReporteRepository:

    @staticmethod
    def get_ranking_estudiantes(
        db: Session,
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene ranking de estudiantes por cantidad de esquelas
        """
        # Join con esquelas_codigos explícitamente
        query = db.query(
            Estudiante.id_estudiante,
            Estudiante.nombres,
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno,
            func.count(func.distinct(Esquela.id_esquela)).label('total'),
            func.sum(
                case((CodigoEsquela.tipo == 'reconocimiento', 1), else_=0)
            ).label('reconocimiento'),
            func.sum(
                case((CodigoEsquela.tipo == 'orientacion', 1), else_=0)
            ).label('orientacion')
        ).join(
            Esquela, Estudiante.id_estudiante == Esquela.id_estudiante
        ).join(
            EsquelaCodigo, Esquela.id_esquela == EsquelaCodigo.id_esquela
        ).join(
            CodigoEsquela, EsquelaCodigo.id_codigo == CodigoEsquela.id_codigo
        )

        # Filtros de fecha
        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        # Filtro por tipo
        if tipo:
            query = query.filter(CodigoEsquela.tipo == tipo)

        query = query.group_by(
            Estudiante.id_estudiante,
            Estudiante.nombres,
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno
        ).order_by(func.count(func.distinct(Esquela.id_esquela)).desc()).limit(limit)

        results = query.all()

        # Formatear resultados
        ranking = []
        for idx, (id_est, nombres, ap_pat, ap_mat, total, reconocimiento, orientacion) in enumerate(results, 1):
            apellidos = f"{ap_pat} {ap_mat or ''}".strip()
            nombre_completo = f"{nombres} {apellidos}"
            ranking.append({
                "id": id_est,
                "nombre": nombre_completo,
                "total": int(total or 0),
                "reconocimiento": int(reconocimiento or 0),
                "orientacion": int(orientacion or 0),
                "posicion": idx
            })

        return ranking

    @staticmethod
    def get_ranking_cursos(
        db: Session,
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene ranking de cursos por cantidad de esquelas
        NOTA: Join a través de estudiantes_cursos porque no hay id_curso en esquelas
        """
        query = db.query(
            Curso.id_curso,
            Curso.nombre_curso,
            func.count(func.distinct(Esquela.id_esquela)).label('total'),
            func.sum(
                case((CodigoEsquela.tipo == 'reconocimiento', 1), else_=0)
            ).label('reconocimiento'),
            func.sum(
                case((CodigoEsquela.tipo == 'orientacion', 1), else_=0)
            ).label('orientacion')
        ).select_from(Curso).join(
            estudiantes_cursos, Curso.id_curso == estudiantes_cursos.c.id_curso
        ).join(
            Estudiante, Estudiante.id_estudiante == estudiantes_cursos.c.id_estudiante
        ).join(
            Esquela, Esquela.id_estudiante == Estudiante.id_estudiante
        ).join(
            EsquelaCodigo, Esquela.id_esquela == EsquelaCodigo.id_esquela
        ).join(
            CodigoEsquela, EsquelaCodigo.id_codigo == CodigoEsquela.id_codigo
        )

        # Filtros de fecha
        if fecha_desde:
            query = query.filter(Esquela.fecha >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Esquela.fecha <= fecha_hasta)

        # Filtro por tipo
        if tipo:
            query = query.filter(CodigoEsquela.tipo == tipo)

        query = query.group_by(
            Curso.id_curso,
            Curso.nombre_curso
        ).order_by(func.count(func.distinct(Esquela.id_esquela)).desc()).limit(limit)

        results = query.all()

        # Formatear resultados
        ranking = []
        for idx, (id_curso, nombre_curso, total, reconocimiento, orientacion) in enumerate(results, 1):
            ranking.append({
                "id": id_curso,
                "nombre": nombre_curso,
                "total": int(total or 0),
                "reconocimiento": int(reconocimiento or 0),
                "orientacion": int(orientacion or 0),
                "posicion": idx
            })

        return ranking

