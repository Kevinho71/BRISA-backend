"""Controlador (router) para el módulo de Reportes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Literal
from datetime import date


from app.core.database import get_db
from app.modules.reportes.services.reporte_service import ReporteService
from app.modules.reportes.dto.reporte_dto import (
    RankingResponseDTO,
    EstudianteListadoDTO,
    EstudiantesApoderadosResponseDTO,
    ContactosApoderadosResponseDTO,
    DistribucionEdadResponseDTO,
    HistorialCursosResponseDTO,
    ProfesoresAsignadosResponseDTO,
    MateriasPorNivelResponseDTO,
    CargaAcademicaResponseDTO,
    CursosPorGestionResponseDTO,
    EsquelasPorProfesorResponseDTO,
    EsquelasPorFechaResponseDTO,
    CodigosFrecuentesResponseDTO
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


# ================================
# Endpoints para Reportes Académicos
# ================================

@router.get("/academic/professors", response_model=ProfesoresAsignadosResponseDTO)
def obtener_profesores_asignados(
    curso_id: Optional[int] = Query(None, description="ID del curso"),
    materia_id: Optional[int] = Query(None, description="ID de la materia"),
    nivel: Optional[Literal["inicial", "primaria", "secundaria"]] = Query(None, description="Nivel educativo"),
    gestion: Optional[str] = Query(None, description="Año de gestión (ej: '2024')"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene profesores asignados por curso y materia.
    
    **Parámetros:**
    - **curso_id**: ID específico del curso (opcional)
    - **materia_id**: ID específico de la materia (opcional)
    - **nivel**: Nivel educativo ('inicial', 'primaria', 'secundaria') (opcional)
    - **gestion**: Año de gestión, ej: '2024' (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/academic/professors?curso_id=5
    GET /api/reports/academic/professors?materia_id=3&gestion=2024
    GET /api/reports/academic/professors?nivel=primaria
    GET /api/reports/academic/professors
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "profesores": [
            {
                "id_profesor": 10,
                "ci": "12345678",
                "nombre_completo": "Carlos Pérez López",
                "telefono": "70123456",
                "correo": "carlos@ejemplo.com",
                "curso": "5to A (2024)",
                "materia": "Matemáticas"
            }
        ],
        "total": 1,
        "curso": "5to A (2024)",
        "materia": "Matemáticas"
    }
    ```
    """

    return ReporteService.obtener_profesores_asignados(
        db=db,
        id_curso=curso_id,
        id_materia=materia_id,
        nivel=nivel,
        gestion=gestion
    )


@router.get("/academic/subjects", response_model=MateriasPorNivelResponseDTO)
def obtener_materias_por_nivel(
    nivel: Optional[Literal["inicial", "primaria", "secundaria"]] = Query(None, description="Nivel educativo"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene materias por nivel educativo.
    
    **Parámetros:**
    - **nivel**: Nivel educativo ('inicial', 'primaria', 'secundaria') (opcional)
        - Si se especifica: retorna solo materias de ese nivel
        - Si se omite: retorna todas las materias
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/academic/subjects?nivel=primaria
    GET /api/reports/academic/subjects
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "materias": [
            {
                "id_materia": 1,
                "nombre_materia": "Matemáticas",
                "nivel": "primaria"
            },
            {
                "id_materia": 2,
                "nombre_materia": "Lenguaje",
                "nivel": "primaria"
            }
        ],
        "total": 2,
        "nivel": "primaria"
    }
    ```
    """

    return ReporteService.obtener_materias_por_nivel(
        db=db,
        nivel=nivel
    )


@router.get("/academic/workload", response_model=CargaAcademicaResponseDTO)
def obtener_carga_academica(
    profesor_id: Optional[int] = Query(None, description="ID del profesor (opcional)"),
    gestion: Optional[str] = Query(None, description="Año de gestión (ej: '2024')"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene carga académica de profesores.
    
    Muestra las asignaciones de cada profesor (cursos y materias),
    con totales de asignaciones, cursos distintos y materias distintas.
    
    **Parámetros:**
    - **profesor_id**: ID específico del profesor (opcional)
        - Si se especifica: retorna solo la carga de ese profesor
        - Si se omite: retorna carga de todos los profesores
    - **gestion**: Año de gestión para filtrar asignaciones (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/academic/workload?profesor_id=10
    GET /api/reports/academic/workload?gestion=2024
    GET /api/reports/academic/workload
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "profesores": [
            {
                "id_profesor": 10,
                "ci": "12345678",
                "nombre_completo": "Carlos Pérez López",
                "telefono": "70123456",
                "correo": "carlos@ejemplo.com",
                "asignaciones": [
                    {
                        "curso": "5to A",
                        "nivel": "primaria",
                        "gestion": "2024",
                        "materia": "Matemáticas"
                    },
                    {
                        "curso": "5to B",
                        "nivel": "primaria",
                        "gestion": "2024",
                        "materia": "Matemáticas"
                    }
                ],
                "total_asignaciones": 2,
                "cursos_distintos": 2,
                "materias_distintas": 1
            }
        ],
        "total_profesores": 1
    }
    ```
    """
    return ReporteService.obtener_carga_academica(
        db=db,
        id_profesor=profesor_id,
        gestion=gestion
    )


@router.get("/academic/courses", response_model=CursosPorGestionResponseDTO)
def obtener_cursos_por_gestion(
    gestion: Optional[str] = Query(None, description="Año de gestión (ej: '2024')"),
    nivel: Optional[Literal["inicial", "primaria", "secundaria"]] = Query(None, description="Nivel educativo"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene cursos por gestión con cantidad de estudiantes.
    
    **Parámetros:**
    - **gestion**: Año de gestión, ej: '2024' (opcional)
    - **nivel**: Nivel educativo ('inicial', 'primaria', 'secundaria') (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/academic/courses?gestion=2024
    GET /api/reports/academic/courses?nivel=primaria&gestion=2024
    GET /api/reports/academic/courses
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "cursos": [
            {
                "id_curso": 5,
                "nombre_curso": "5to A",
                "nivel": "primaria",
                "gestion": "2024",
                "total_estudiantes": 25
            },
            {
                "id_curso": 6,
                "nombre_curso": "5to B",
                "nivel": "primaria",
                "gestion": "2024",
                "total_estudiantes": 23
            }
        ],
        "total": 2,
        "gestion": "2024",
        "nivel": "primaria"
    }
    ```
    """
    return ReporteService.obtener_cursos_por_gestion(
        db=db,
        gestion=gestion,
        nivel=nivel
    )


# ================================
# Endpoints para Reportes de Esquelas
# ================================

@router.get("/esquelas/by-professor", response_model=EsquelasPorProfesorResponseDTO)
def obtener_esquelas_por_profesor(
    profesor_id: Optional[int] = Query(None, description="ID del profesor (opcional)"),
    fecha_desde: Optional[date] = Query(None, alias="from", description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[date] = Query(None, alias="to", description="Fecha hasta (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene esquelas agrupadas por profesor emisor.
    
    Muestra todas las esquelas emitidas por cada profesor, con totales
    de reconocimientos y orientaciones.
    
    **Parámetros:**
    - **profesor_id**: ID específico del profesor (opcional)
        - Si se especifica: retorna solo esquelas de ese profesor
        - Si se omite: retorna esquelas de todos los profesores
    - **from**: Fecha desde (opcional, formato: YYYY-MM-DD)
    - **to**: Fecha hasta (opcional, formato: YYYY-MM-DD)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/esquelas/by-professor?profesor_id=10
    GET /api/reports/esquelas/by-professor?from=2024-01-01&to=2024-12-31
    GET /api/reports/esquelas/by-professor
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "profesores": [
            {
                "id_profesor": 10,
                "profesor_nombre": "Carlos Pérez López",
                "profesor_ci": "12345678",
                "total_esquelas": 25,
                "reconocimientos": 15,
                "orientaciones": 10,
                "esquelas": [
                    {
                        "id_esquela": 1,
                        "fecha": "2024-11-15",
                        "estudiante_nombre": "Juan García",
                        "estudiante_ci": "87654321",
                        "profesor_nombre": "Carlos Pérez López",
                        "registrador_nombre": "Ana Martínez",
                        "codigos": ["R01 - Buen comportamiento"],
                        "observaciones": "Excelente participación"
                    }
                ]
            }
        ],
        "total_profesores": 1,
        "total_esquelas": 25
    }
    ```
    """
    return ReporteService.obtener_esquelas_por_profesor(
        db=db,
        id_profesor=profesor_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )


@router.get("/esquelas/by-date", response_model=EsquelasPorFechaResponseDTO)
def obtener_esquelas_por_fecha(
    fecha_desde: Optional[date] = Query(None, alias="from", description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[date] = Query(None, alias="to", description="Fecha hasta (YYYY-MM-DD)"),
    tipo: Optional[Literal["reconocimiento", "orientacion"]] = Query(None, description="Tipo de esquela (opcional)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene esquelas por rango de fechas.
    
    **Parámetros:**
    - **from**: Fecha desde (opcional, formato: YYYY-MM-DD)
    - **to**: Fecha hasta (opcional, formato: YYYY-MM-DD)
    - **tipo**: Tipo de esquela ('reconocimiento', 'orientacion') (opcional)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/esquelas/by-date?from=2024-01-01&to=2024-12-31
    GET /api/reports/esquelas/by-date?tipo=reconocimiento
    GET /api/reports/esquelas/by-date
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "esquelas": [
            {
                "id_esquela": 1,
                "fecha": "2024-11-15",
                "estudiante_nombre": "Juan García Pérez",
                "estudiante_ci": "87654321",
                "profesor_nombre": "Carlos Pérez López",
                "registrador_nombre": "Ana Martínez",
                "codigos": ["R01 - Buen comportamiento"],
                "observaciones": "Excelente participación"
            }
        ],
        "total": 1,
        "fecha_desde": "2024-01-01",
        "fecha_hasta": "2024-12-31",
        "reconocimientos": 1,
        "orientaciones": 0
    }
    ```
    """
    return ReporteService.obtener_esquelas_por_fecha(
        db=db,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        tipo=tipo
    )


@router.get("/esquelas/frequent-codes", response_model=CodigosFrecuentesResponseDTO)
def obtener_codigos_frecuentes(
    tipo: Optional[Literal["reconocimiento", "orientacion"]] = Query(None, description="Tipo de código (opcional)"),
    limit: int = Query(10, ge=1, le=50, description="Cantidad máxima de códigos a retornar"),
    fecha_desde: Optional[date] = Query(None, alias="from", description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[date] = Query(None, alias="to", description="Fecha hasta (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene los códigos de esquelas más frecuentemente aplicados.
    
    **Parámetros:**
    - **tipo**: Tipo de código ('reconocimiento', 'orientacion') (opcional)
    - **limit**: Cantidad máxima de códigos a retornar (por defecto 10, máximo 50)
    - **from**: Fecha desde para filtrar aplicaciones (opcional, formato: YYYY-MM-DD)
    - **to**: Fecha hasta para filtrar aplicaciones (opcional, formato: YYYY-MM-DD)
    
    **Ejemplo de uso:**
    ```
    GET /api/reports/esquelas/frequent-codes?limit=5
    GET /api/reports/esquelas/frequent-codes?tipo=reconocimiento
    GET /api/reports/esquelas/frequent-codes?from=2024-01-01&to=2024-12-31
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
        "codigos": [
            {
                "id_codigo": 1,
                "codigo": "R01",
                "descripcion": "Buen comportamiento",
                "tipo": "reconocimiento",
                "total_aplicaciones": 150,
                "porcentaje": 35.5
            },
            {
                "id_codigo": 5,
                "codigo": "O02",
                "descripcion": "Falta de tarea",
                "tipo": "orientacion",
                "total_aplicaciones": 120,
                "porcentaje": 28.4
            }
        ],
        "total_codigos": 2,
        "total_aplicaciones": 270,
        "tipo": null
    }
    ```
    """
    return ReporteService.obtener_codigos_frecuentes(
        db=db,
        tipo=tipo,
        limit=limit,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
