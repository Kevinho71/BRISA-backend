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
            from app.modules.administracion.models.persona_models import Curso
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
