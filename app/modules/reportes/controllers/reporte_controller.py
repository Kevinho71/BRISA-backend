"""Controlador (router) para el módulo de Reportes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Literal
from datetime import date

from app.core.extensions import get_db
from app.modules.reportes.services.reporte_service import ReporteService
from app.modules.reportes.dto.reporte_dto import (
    RankingResponseDTO,
    EstudianteListadoDTO,
    EstudiantesApoderadosResponseDTO,
    ContactosApoderadosResponseDTO,
    DistribucionEdadResponseDTO,
    HistorialCursosResponseDTO
)
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


# ================================
# Endpoints para Reportes de Estudiantes
# ================================

@router.get("/students", response_model=EstudianteListadoDTO)
def obtener_listado_estudiantes(
    curso_id: Optional[int] = Query(None, description="ID del curso para filtrar"),
    nivel: Optional[Literal["inicial", "primaria", "secundaria"]] = Query(None, description="Nivel educativo"),
    gestion: Optional[str] = Query(None, description="Año de gestión (ej: '2024')"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene listado de estudiantes filtrado por curso, nivel y/o gestión.
    
    **Parámetros:**
    - **curso_id**: ID específico del curso (opcional)
    - **nivel**: Nivel educativo ('inicial', 'primaria', 'secundaria') (opcional)
    - **gestion**: Año de gestión, ej: '2024' (opcional)
    
    Si no se especifica ningún filtro, retorna todos los estudiantes.
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/students?nivel=primaria&gestion=2024
    GET /api/reports/students?curso_id=5
    GET /api/reports/students
    ```
    """

    return ReporteService.obtener_listado_estudiantes(
        db=db,
        id_curso=curso_id,
        nivel=nivel,
        gestion=gestion
    )


@router.get("/students/guardians", response_model=EstudiantesApoderadosResponseDTO)
def obtener_estudiantes_apoderados(
    con_apoderados: Optional[bool] = Query(None, description="True=con apoderados, False=sin apoderados, None=todos"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene estudiantes con o sin apoderados (padres/madres) registrados.
    
    **Parámetros:**
    - **con_apoderados**: 
        - `true`: Solo estudiantes con al menos un apoderado registrado
        - `false`: Solo estudiantes sin apoderados registrados
        - `null` (omitir): Todos los estudiantes con su estado de apoderados
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/students/guardians?con_apoderados=true
    GET /api/reports/students/guardians?con_apoderados=false
    GET /api/reports/students/guardians
    ```
    """

    return ReporteService.obtener_estudiantes_por_apoderados(
        db=db,
        con_apoderados=con_apoderados
    )


@router.get("/students/guardian-contacts", response_model=ContactosApoderadosResponseDTO)
def obtener_contactos_apoderados(
    curso_id: Optional[int] = Query(None, description="ID del curso para filtrar"),
    nivel: Optional[Literal["inicial", "primaria", "secundaria"]] = Query(None, description="Nivel educativo"),
    gestion: Optional[str] = Query(None, description="Año de gestión (ej: '2024')"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene datos de contacto de apoderados (padres/madres) con filtros opcionales.
    
    Retorna información de contacto tanto de padres como madres que tengan
    nombre y teléfono registrados.
    
    **Parámetros:**
    - **curso_id**: ID específico del curso (opcional)
    - **nivel**: Nivel educativo (opcional)
    - **gestion**: Año de gestión (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/students/guardian-contacts?nivel=primaria
    GET /api/reports/students/guardian-contacts?curso_id=5&gestion=2024
    GET /api/reports/students/guardian-contacts
    ```
    """

    return ReporteService.obtener_contactos_apoderados(
        db=db,
        id_curso=curso_id,
        nivel=nivel,
        gestion=gestion
    )


@router.get("/students/age-distribution", response_model=DistribucionEdadResponseDTO)
def obtener_distribucion_edad(
    curso_id: Optional[int] = Query(None, description="ID del curso para filtrar"),
    nivel: Optional[Literal["inicial", "primaria", "secundaria"]] = Query(None, description="Nivel educativo"),
    gestion: Optional[str] = Query(None, description="Año de gestión (ej: '2024')"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene distribución de estudiantes por rangos de edad.
    
    Los rangos de edad son:
    - 0-4 años
    - 5-7 años
    - 8-10 años
    - 11-13 años
    - 14-16 años
    - 17+ años
    - Sin fecha (estudiantes sin fecha de nacimiento registrada)
    
    **Parámetros:**
    - **curso_id**: ID específico del curso (opcional)
    - **nivel**: Nivel educativo (opcional)
    - **gestion**: Año de gestión (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/students/age-distribution?nivel=primaria
    GET /api/reports/students/age-distribution?gestion=2024
    GET /api/reports/students/age-distribution
    ```
    """
    print(ReporteService.obtener_distribucion_edad(
        db=db,
        id_curso=curso_id,
        nivel=nivel,
        gestion=gestion
    ))
    return ReporteService.obtener_distribucion_edad(
        db=db,
        id_curso=curso_id,
        nivel=nivel,
        gestion=gestion
    )


@router.get("/students/course-history", response_model=HistorialCursosResponseDTO)
def obtener_historial_cursos(
    estudiante_id: Optional[int] = Query(None, description="ID del estudiante (opcional, si no se especifica retorna todos)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene historial de cursos por estudiante.
    
    Muestra todos los cursos en los que ha estado inscrito cada estudiante,
    ordenados por gestión de manera descendente.
    
    **Parámetros:**
    - **estudiante_id**: ID específico del estudiante (opcional)
        - Si se especifica: retorna solo el historial de ese estudiante
        - Si se omite: retorna historial de todos los estudiantes
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/students/course-history?estudiante_id=123
    GET /api/reports/students/course-history
    ```
    """
    print(ReporteService.obtener_historial_cursos(
        db=db,
        id_estudiante=estudiante_id
    ))
    return ReporteService.obtener_historial_cursos(
        db=db,
        id_estudiante=estudiante_id
    )
