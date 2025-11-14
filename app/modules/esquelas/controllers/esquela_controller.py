"""Controlador (router) para el módulo de Esquelas."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

# Fuente correcta del dependency de BD
from app.core.database import get_db
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.decorators.auth_decorators import require_esquela_access, require_permissions
from app.shared.permission_mapper import puede_ver_todas_esquelas

from app.modules.esquelas.services.esquela_service import EsquelaService
from app.modules.esquelas.dto.esquela_dto import (
    EsquelaBaseDTO,
    EsquelaResponseDTO,
    EsquelaListResponseDTO,
    EsquelasAggregateByCourseDTO,
    EstudianteEsquelasDTO,
    EsquelaAggregateByYearDTO,
    EsquelaAggregateByMonthDTO
)


router = APIRouter(prefix="/esquelas", tags=["Esquelas"])


@router.get("/", response_model=EsquelaListResponseDTO)
@require_esquela_access(allow_owner=True)
async def listar_esquelas(
    name: Optional[str] = Query(None, description="Filtrar por nombre del estudiante"),
    course: Optional[int] = Query(None, description="Filtrar por ID de curso"),
    type: Optional[str] = Query(None, description="Filtrar por tipo: 'reconocimiento' u 'orientacion'"),
    from_date: Optional[date] = Query(None, alias="from", description="Fecha desde (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(None, alias="to", description="Fecha hasta (YYYY-MM-DD)"),
    year: Optional[int] = Query(None, description="Filtrar por año"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mes (1-12)"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Lista esquelas con filtros avanzados y paginación.
    
    **Permisos:**
    - **Admin/Regente**: Ve todas las esquelas
    - **Profesor**: Ve solo las esquelas que él asignó
    
    **Filtros disponibles:**
    - **name**: Busca por nombre, apellido paterno o materno del estudiante
    - **course**: ID del curso
    - **type**: Tipo de esquela ('reconocimiento' u 'orientacion')
    - **from**: Fecha desde (formato: YYYY-MM-DD)
    - **to**: Fecha hasta (formato: YYYY-MM-DD)
    - **year**: Año específico
    - **month**: Mes específico (1-12)
    - **page**: Número de página (por defecto 1)
    - **page_size**: Cantidad de resultados por página (por defecto 10, máximo 100)
    
    **Ejemplo:**
    ```
    GET /api/esquelas?name=Juan&course=5&year=2024&page=1&page_size=20
    ```
    """
    return EsquelaService.listar_esquelas_con_filtros(
        db=db,
        name=name,
        course_id=course,
        tipo=type,
        fecha_desde=from_date,
        fecha_hasta=to_date,
        year=year,
        month=month,
        page=page,
        page_size=page_size,
        current_user=current_user
    )


@router.get("/aggregate/by-course", response_model=List[EsquelasAggregateByCourseDTO])
def obtener_agregado_por_curso(
    year: Optional[int] = Query(None, description="Filtrar por año"),
    db: Session = Depends(get_db)
):
    """
    Obtiene la cantidad de esquelas de reconocimiento y orientación por curso.
    
    **Ejemplo de respuesta:**
    ```json
    [
        {
            "curso_id": 1,
            "curso": "1° A",
            "reconocimiento": 5,
            "orientacion": 2
        },
        {
            "curso_id": 2,
            "curso": "1° B",
            "reconocimiento": 3,
            "orientacion": 4
        }
    ]
    ```
    
    **Parámetros:**
    - **year**: Filtrar por año específico (opcional)
    """
    return EsquelaService.obtener_agregado_por_curso(db, year)


@router.get("/aggregate/by-period")
def obtener_agregado_por_periodo(
    group_by: str = Query("year", description="Agrupar por 'year' o 'month'"),
    db: Session = Depends(get_db)
):
    """
    Obtiene agregación de esquelas por año o mes.
    Útil para drilldown: año → mes.
    
    **Parámetros:**
    - **group_by**: 'year' para agrupar por año, 'month' para agrupar por año y mes
    
    **Ejemplo con group_by=year:**
    ```json
    [
        {"year": 2023, "total": 150},
        {"year": 2024, "total": 200}
    ]
    ```
    
    **Ejemplo con group_by=month:**
    ```json
    [
        {"year": 2024, "month": 1, "total": 15},
        {"year": 2024, "month": 2, "total": 18}
    ]
    ```
    """
    return EsquelaService.obtener_agregado_por_periodo(db, group_by)


@router.get("/{id}", response_model=EsquelaResponseDTO)
@require_esquela_access(allow_owner=True)
async def obtener_esquela(
    id: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Obtiene una esquela específica por ID.
    
    **Permisos:**
    - **Admin/Regente**: Puede ver cualquier esquela
    - **Profesor**: Solo puede ver esquelas que él asignó
    """
    return EsquelaService.obtener_esquela(db, id, current_user=current_user)


@router.post("/", response_model=EsquelaResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions('crear_esquela')
async def crear_esquela(
    esquela_data: EsquelaBaseDTO,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva esquela.
    
    **Permisos:**
    - **Admin/Regente**: Puede crear esquelas para cualquier profesor
    - **Profesor**: Solo puede crear esquelas en su propio nombre
    
    **Nota**: El profesor solo puede asignar esquelas donde él sea el id_profesor.
    """
    return EsquelaService.crear_esquela(db, esquela_data, current_user=current_user)


@router.delete("/{id}")
@require_permissions('eliminar_esquela')
async def eliminar_esquela(
    id: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Elimina una esquela por ID.
    
    **Permisos:**
    - Requiere permiso 'eliminar_esquela' (generalmente Admin/Regente)
    """
    return EsquelaService.eliminar_esquela(db, id)

