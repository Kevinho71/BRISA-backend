"""Controlador (Router) para Estudiantes"""

from fastapi import APIRouter, Depends, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.modules.estudiantes.services.estudiante_service import EstudianteService
from app.modules.estudiantes.dto.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO,
    EstudianteListDTO,
    CambiarEstadoDTO,
    CambiarEstadoResponseDTO,
    ImportResultDTO
)


router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


# ============= CRUD Básico =============

@router.post("/", response_model=EstudianteResponseDTO, status_code=201, summary="RF-EST-001: Crear Estudiante")
def crear_estudiante(
    datos: EstudianteCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo estudiante en el sistema.
    
    **Datos requeridos:**
    - Nombres
    - Apellido paterno
    - Apellido materno
    
    **Datos opcionales:**
    - CI, fecha de nacimiento, dirección, estado
    - Información completa del padre y madre
    """
    return EstudianteService.crear_estudiante(db, datos)


@router.get("/", response_model=EstudianteListDTO, summary="RF-EST-002: Listar Todos los Estudiantes")
def listar_estudiantes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista completa de todos los estudiantes con paginación.
    
    Incluye la lista de cursos asignados a cada estudiante.
    """
    return EstudianteService.obtener_todos(db, skip, limit)


@router.get("/{id_estudiante}", response_model=EstudianteResponseDTO, summary="RF-EST-003: Obtener Estudiante por ID")
def obtener_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Obtener información detallada de un estudiante específico por su ID.
    
    Incluye la lista completa de cursos asignados.
    """
    return EstudianteService.obtener_por_id(db, id_estudiante)


@router.put("/{id_estudiante}", response_model=EstudianteResponseDTO, summary="RF-EST-004: Actualizar Estudiante")
def actualizar_estudiante(
    id_estudiante: int,
    datos: EstudianteUpdateDTO,
    db: Session = Depends(get_db)
):
    """
    Actualizar información de un estudiante existente.
    
    Todos los campos son opcionales - solo se actualizan los campos enviados.
    """
    return EstudianteService.actualizar_estudiante(db, id_estudiante, datos)


@router.delete("/{id_estudiante}", summary="RF-EST-005: Eliminar Estudiante")
def eliminar_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un estudiante del sistema de forma permanente.
    
    Se eliminan automáticamente todas sus asignaciones a cursos (cascada).
    """
    return EstudianteService.eliminar_estudiante(db, id_estudiante)


# ============= Gestión de Estados =============

@router.patch("/{id_estudiante}/estado", response_model=CambiarEstadoResponseDTO, summary="RF-EST-006: Cambiar Estado de Estudiante")
def cambiar_estado_estudiante(
    id_estudiante: int,
    datos: CambiarEstadoDTO,
    db: Session = Depends(get_db)
):
    """
    Cambiar el estado de un estudiante.
    
    **Estados válidos:**
    - Activo
    - Retirado
    - Abandono
    """
    return EstudianteService.cambiar_estado(db, id_estudiante, datos)


@router.get("/estado/{estado}", response_model=EstudianteListDTO, summary="RF-EST-007: Listar Estudiantes por Estado")
def listar_por_estado(
    estado: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Filtrar estudiantes por estado (Activo, Retirado, Abandono).
    
    Incluye información completa y cursos de cada estudiante.
    """
    return EstudianteService.listar_por_estado(db, estado, skip, limit)


# ============= Filtros por Gestión =============

@router.get("/gestion/{gestion}", summary="RF-EST-008: Listar Estudiantes por Gestión")
def listar_por_gestion(
    gestion: str,
    nivel: Optional[str] = Query(None, description="Nivel educativo: inicial, primaria, secundaria"),
    id_curso: Optional[int] = Query(None, description="ID de curso específico"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Obtener estudiantes inscritos en cursos de una gestión específica.
    
    Muestra SOLO los cursos de la gestión especificada.
    
    **Filtros opcionales:**
    - nivel: inicial, primaria, secundaria
    - id_curso: Curso específico
    """
    resultado = EstudianteService.listar_por_gestion(db, gestion, nivel, id_curso, skip, limit)
    # Devolver el array de estudiantes directamente en data para que frontend pueda hacer .filter()
    # Agregar alias 'id' para compatibilidad con frontend
    estudiantes_data = []
    for est in resultado.estudiantes:
        est_dict = est.model_dump()
        est_dict['id'] = est_dict['id_estudiante']  # Alias para compatibilidad
        estudiantes_data.append(est_dict)
    
    return ResponseModel.success(
        message=f"Lista de estudiantes de la gestión {gestion} obtenida exitosamente ({resultado.total} encontrados)",
        data=estudiantes_data
    )


# ============= Importación/Exportación Excel =============

@router.get("/exportar/todos", summary="RF-EST-009: Exportar Todos los Estudiantes a Excel")
def exportar_todos_excel(db: Session = Depends(get_db)):
    """
    Descargar archivo Excel con todos los estudiantes registrados.
    
    Incluye todas las columnas de información con formato profesional.
    """
    output = EstudianteService.exportar_todos_excel(db)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"estudiantes_todos_{timestamp}.xlsx"
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/exportar/{id_estudiante}", summary="RF-EST-010: Exportar Estudiante Individual a Excel")
def exportar_estudiante_excel(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Descargar archivo Excel con información de un estudiante específico.
    
    Incluye dos hojas:
    - Estudiante: información personal
    - Cursos: lista de cursos asignados
    """
    output = EstudianteService.exportar_estudiante_excel(db, id_estudiante)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"estudiante_{id_estudiante}_{timestamp}.xlsx"
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/importar", response_model=ImportResultDTO, summary="RF-EST-011: Importar Estudiantes desde Excel")
async def importar_estudiantes_excel(
    file: UploadFile = File(..., description="Archivo Excel (.xlsx o .xls) con estudiantes"),
    db: Session = Depends(get_db)
):
    """
    Cargar masivamente estudiantes desde un archivo Excel.
    
    **Comportamiento:**
    - Si el CI existe: actualiza el estudiante
    - Si el CI no existe: crea nuevo estudiante
    
    **Validaciones:**
    - Formato: .xlsx o .xls
    - Tamaño máximo: 50 MB
    - Filas máximas: 10,000
    
    **Columnas requeridas:**
    - CI, Nombres, Apellido Paterno, Apellido Materno
    
    **Retorna:**
    - Resumen con cantidad de creados, actualizados y errores
    """
    return await EstudianteService.importar_estudiantes_excel(db, file)


@router.get("/plantilla/excel", summary="RF-EST-012: Descargar Plantilla de Importación")
def descargar_plantilla(db: Session = Depends(get_db)):
    """
    Descargar plantilla Excel con el formato correcto para importar estudiantes.
    
    Incluye:
    - Hoja "Estudiantes" con ejemplo de datos
    - Hoja "Instrucciones" con guía detallada de uso
    """
    output = EstudianteService.descargar_plantilla_excel()
    
    filename = "plantilla_importacion_estudiantes.xlsx"
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
