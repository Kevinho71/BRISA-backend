"""Controlador (router) para consultas de estudiantes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date


from app.core.database import get_db
from app.modules.esquelas.services.esquela_service import EsquelaService
from app.modules.esquelas.dto.esquela_dto import EstudianteEsquelasDTO


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/{student_id}/esquelas", response_model=EstudianteEsquelasDTO)
def obtener_esquelas_estudiante(
    student_id: int,
    from_date: Optional[date] = Query(None, alias="from", description="Fecha desde (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(None, alias="to", description="Fecha hasta (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las esquelas de un estudiante con conteo de códigos en un rango de fechas.
    
    **Retorna:**
    - **total**: Cantidad total de esquelas
    - **esquelas**: Lista de esquelas con detalles completos
    - **codigos_resumen**: Conteo de códigos por tipo
    
    **Ejemplo de respuesta:**
    ```json
    {
        "total": 7,
        "esquelas": [...],
        "codigos_resumen": {
            "reconocimiento": 5,
            "orientacion": 2
        }
    }
    ```
    
    **Parámetros:**
    - **student_id**: ID del estudiante
    - **from**: Fecha desde (opcional, formato: YYYY-MM-DD)
    - **to**: Fecha hasta (opcional, formato: YYYY-MM-DD)
    """
    return EsquelaService.obtener_esquelas_estudiante(
        db=db,
        student_id=student_id,
        fecha_desde=from_date,
        fecha_hasta=to_date
    )
