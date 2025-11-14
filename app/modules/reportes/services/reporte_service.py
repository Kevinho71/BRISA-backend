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
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene ranking por estudiante o curso
        
        Args:
            metric: 'student' o 'course'
            tipo: 'reconocimiento', 'orientacion' o None (todos)
            limit: Cantidad máxima de resultados
            fecha_desde: Fecha desde (opcional)
            fecha_hasta: Fecha hasta (opcional)
        """
        if metric == "student":
            data = ReporteRepository.get_ranking_estudiantes(
                db, tipo, limit, fecha_desde, fecha_hasta
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
