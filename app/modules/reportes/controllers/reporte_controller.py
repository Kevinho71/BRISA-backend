"""Controlador (router) para el módulo de Reportes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Literal
from datetime import date

from app.core.extensions import get_db
from app.modules.reportes.services.reporte_service import ReporteService
from app.modules.reportes.dto.reporte_dto import RankingResponseDTO
from app.modules.usuarios.models.usuario_models import Usuario
from app.modules.auth.services.auth_service import get_current_user_dependency


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/ranking", response_model=RankingResponseDTO)
def obtener_ranking(
    metric: Literal["student", "course"] = Query(..., description="Métrica: 'student' o 'course'"),
    type: Optional[Literal["reconocimiento", "orientacion"]] = Query(None, description="Tipo de esquela (opcional)"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados"),
    from_date: Optional[date] = Query(None, alias="from", description="Fecha desde (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(None, alias="to", description="Fecha hasta (YYYY-MM-DD)"),
    registrador_id: Optional[int] = Query(None, description="ID del usuario (profesor/regente) para filtrar esquelas asignadas por él"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene ranking de estudiantes o cursos por cantidad de esquelas.
    
    **Parámetros:**
    - **metric**: 'student' para ranking por estudiante, 'course' para ranking por curso
    - **type**: Tipo de esquela ('reconocimiento', 'orientacion' o null para ambos)
    - **limit**: Cantidad máxima de resultados (por defecto 10, máximo 100)
    - **from**: Fecha desde (opcional, formato: YYYY-MM-DD)
    - **to**: Fecha hasta (opcional, formato: YYYY-MM-DD)
    - **registrador_id**: ID del usuario para filtrar solo las esquelas registradas/asignadas por él (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/ranking?metric=student&type=reconocimiento&limit=5
    GET /api/reports/ranking?metric=student&registrador_id=14
    GET /api/reports/ranking?metric=course&from=2024-01-01&to=2024-12-31
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "metric": "student",
        "type": "reconocimiento",
        "limit": 5,
        "data": [
            {
                "id": 123,
                "nombre": "Juan Pérez García",
                "total": 15,
                "reconocimiento": 10,
                "orientacion": 5,
                "posicion": 1
            },
            ...
        ]
    }
    ```
    """
    # Si no se especifica registrador_id y el usuario es profesor, filtrar por su ID
    if registrador_id is None and current_user.persona.tipo_persona == 'profesor':
        registrador_id = current_user.id_persona

    return ReporteService.obtener_ranking(
        db=db,
        metric=metric,
        tipo=type,
        limit=limit,
        fecha_desde=from_date,
        fecha_hasta=to_date,
        id_registrador=registrador_id
    )
