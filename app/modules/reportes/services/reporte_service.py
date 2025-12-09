# app/modules/reportes/services/reporte_service.py
from sqlalchemy.orm import Session
from app.modules.reportes.repositories.reporte_repository import ReporteRepository
from datetime import date
from typing import Optional, Literal


class ReporteService:

    @staticmethod
    def obtener_ranking(
        db: Session,
        metric: Literal["student", "course"],
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        id_registrador: Optional[int] = None
    ):
        """
        Obtiene ranking por estudiante o curso
        
        Args:
            metric: 'student' o 'course'
            tipo: 'reconocimiento', 'orientacion' o None (todos)
            limit: Cantidad máxima de resultados
            fecha_desde: Fecha desde (opcional)
            fecha_hasta: Fecha hasta (opcional)
            id_registrador: ID del usuario que registró la esquela (para filtrar "mis asignaciones")
        """
        if metric == "student":
            data = ReporteRepository.get_ranking_estudiantes(
                db, tipo, limit, fecha_desde, fecha_hasta, id_registrador
            )
        elif metric == "course":
            data = ReporteRepository.get_ranking_cursos(
                db, tipo, limit, fecha_desde, fecha_hasta
            )
        else:
            raise ValueError("metric debe ser 'student' o 'course'")

        return {
            "metric": metric,
            "type": tipo,
            "limit": limit,
            "data": data
        }

    # ================================
    # Servicios para Reportes de Estudiantes
    # ================================

    @staticmethod
    def obtener_listado_estudiantes(
        db: Session,
        id_curso: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene listado de estudiantes con filtros opcionales
        """
        estudiantes = ReporteRepository.get_estudiantes_por_filtros(
            db, id_curso, nivel, gestion
        )

        # Obtener información del filtro aplicado
        curso_info = None
        if id_curso:
            from app.modules.estudiantes.models.Curso import Curso
            curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
            if curso:
                curso_info = f"{curso.nombre_curso} ({curso.gestion})"

        return {
            "estudiantes": estudiantes,
            "total": len(estudiantes),
            "curso": curso_info,
            "nivel": nivel,
            "gestion": gestion
        }

    @staticmethod
    def obtener_estudiantes_por_apoderados(
        db: Session,
        con_apoderados: Optional[bool] = None
    ):
        """
        Obtiene estudiantes con o sin apoderados registrados
        """
        estudiantes = ReporteRepository.get_estudiantes_por_apoderados(
            db, con_apoderados
        )

        return {
            "estudiantes": estudiantes,
            "total": len(estudiantes),
            "con_apoderados": con_apoderados
        }

    @staticmethod
    def obtener_contactos_apoderados(
        db: Session,
        id_curso: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene datos de contacto de apoderados
        """
        contactos = ReporteRepository.get_contactos_apoderados(
            db, id_curso, nivel, gestion
        )

        return {
            "contactos": contactos,
            "total": len(contactos)
        }

    @staticmethod
    def obtener_distribucion_edad(
        db: Session,
        id_curso: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene distribución de estudiantes por rangos de edad
        """
        return ReporteRepository.get_distribucion_por_edad(
            db, id_curso, nivel, gestion
        )

    @staticmethod
    def obtener_historial_cursos(
        db: Session,
        id_estudiante: Optional[int] = None
    ):
        """
        Obtiene historial de cursos por estudiante
        """
        historiales = ReporteRepository.get_historial_cursos_estudiante(
            db, id_estudiante
        )

        return {
            "historiales": historiales,
            "total_estudiantes": len(historiales)
        }

    # ================================
    # Servicios para Reportes Académicos
    # ================================

    @staticmethod
    def obtener_profesores_asignados(
        db: Session,
        id_curso: Optional[int] = None,
        id_materia: Optional[int] = None,
        nivel: Optional[str] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene profesores asignados por curso y materia
        """
        profesores = ReporteRepository.get_profesores_asignados(
            db, id_curso, id_materia, nivel, gestion
        )

        # Obtener información de filtros aplicados
        curso_info = None
        materia_info = None

        if id_curso:
            from app.modules.estudiantes.models.Curso import Curso
            curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
            if curso:
                curso_info = f"{curso.nombre_curso} ({curso.gestion})"

        if id_materia:
            from app.modules.estudiantes.models.Materia import Materia
            materia = db.query(Materia).filter(Materia.id_materia == id_materia).first()
            if materia:
                materia_info = materia.nombre_materia

        return {
            "profesores": profesores,
            "total": len(profesores),
            "curso": curso_info,
            "materia": materia_info
        }

    @staticmethod
    def obtener_materias_por_nivel(
        db: Session,
        nivel: Optional[str] = None
    ):
        """
        Obtiene materias filtradas por nivel educativo
        """
        materias = ReporteRepository.get_materias_por_nivel(db, nivel)

        return {
            "materias": materias,
            "total": len(materias),
            "nivel": nivel
        }

    @staticmethod
    def obtener_carga_academica(
        db: Session,
        id_profesor: Optional[int] = None,
        gestion: Optional[str] = None
    ):
        """
        Obtiene carga académica de profesores
        """
        profesores = ReporteRepository.get_carga_academica_profesores(
            db, id_profesor, gestion
        )

        return {
            "profesores": profesores,
            "total_profesores": len(profesores)
        }

    @staticmethod
    def obtener_cursos_por_gestion(
        db: Session,
        gestion: Optional[str] = None,
        nivel: Optional[str] = None
    ):
        """
        Obtiene cursos por gestión
        """
        cursos = ReporteRepository.get_cursos_por_gestion(db, gestion, nivel)

        return {
            "cursos": cursos,
            "total": len(cursos),
            "gestion": gestion,
            "nivel": nivel
        }

    # ================================
    # Servicios para Reportes de Esquelas
    # ================================

    @staticmethod
    def obtener_esquelas_por_profesor(
        db: Session,
        id_profesor: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene esquelas agrupadas por profesor emisor
        """
        profesores = ReporteRepository.get_esquelas_por_profesor(
            db, id_profesor, fecha_desde, fecha_hasta
        )

        total_esquelas = sum(p["total_esquelas"] for p in profesores)

        return {
            "profesores": profesores,
            "total_profesores": len(profesores),
            "total_esquelas": total_esquelas
        }

    @staticmethod
    def obtener_esquelas_por_fecha(
        db: Session,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        tipo: Optional[str] = None
    ):
        """
        Obtiene esquelas por rango de fechas
        """
        resultado = ReporteRepository.get_esquelas_por_fecha(
            db, fecha_desde, fecha_hasta, tipo
        )

        return {
            "esquelas": resultado["esquelas"],
            "total": resultado["total"],
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "reconocimientos": resultado["reconocimientos"],
            "orientaciones": resultado["orientaciones"]
        }

    @staticmethod
    def obtener_codigos_frecuentes(
        db: Session,
        tipo: Optional[str] = None,
        limit: int = 10,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene códigos más frecuentemente aplicados
        """
        resultado = ReporteRepository.get_codigos_frecuentes(
            db, tipo, limit, fecha_desde, fecha_hasta
        )

        return {
            "codigos": resultado["codigos"],
            "total_codigos": len(resultado["codigos"]),
            "total_aplicaciones": resultado["total_aplicaciones"],
            "tipo": tipo
        }
