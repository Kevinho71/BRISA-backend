"""Controlador (Router) para Cursos"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.modules.cursos.services.curso_service import CursoService
from app.modules.cursos.dto.curso_dto import (
    CursoCreateDTO,
    CursoUpdateDTO,
    CursoResponseDTO,
    CursoListDTO,
    CopiarGestionDTO,
    CopiarGestionResponseDTO
)


router = APIRouter(prefix="/cursos", tags=["Cursos"])


# ============= CRUD Básico =============

@router.post("/", status_code=201, summary="RF-CUR-001: Crear Curso")
def crear_curso(
    datos: CursoCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo curso en el sistema.
    
    **Datos requeridos:**
    - nombre: Nombre del curso (ej: "1ro A", "Kinder Mañana")
    - nivel_educativo: Nivel educativo (Inicial, Primaria, Secundaria)
    - gestion: Gestión o año académico (ej: "2025", "2025-1")
    - capacidad_maxima: Número máximo de estudiantes (opcional, default: 30)
    """
    resultado = CursoService.crear_curso(db, datos)
    return ResponseModel.success(
        message="Curso creado exitosamente",
        data=resultado.model_dump()
    )


@router.get("/", summary="RF-CUR-002: Listar Todos los Cursos")
def listar_cursos(
    gestion: Optional[str] = Query(None, description="Gestión (año). Por defecto: año actual. Use 'all' para ver todos"),
    nivel: Optional[str] = Query(None, description="Nivel: inicial, primaria, secundaria"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de cursos con filtros opcionales.
    
    **Por defecto:** Filtra por año actual
    
    **Para ver todos los años:** Use gestion='all' o gestion='*'
    
    **Filtros opcionales:**
    - gestion: Año académico específico
    - nivel: inicial, primaria, secundaria
    """
    resultado = CursoService.obtener_todos(db, gestion, nivel, skip, limit)
    # Usar by_alias=True para aplicar los alias configurados (id, nombre, nivel_educativo)
    cursos_data = [curso.model_dump(by_alias=True) for curso in resultado.cursos]
    
    return ResponseModel.success(
        message=f"Lista de cursos obtenida exitosamente ({resultado.total} encontrados)",
        data=cursos_data
    )


@router.get("/{id_curso}", summary="RF-CUR-003: Obtener Curso por ID")
def obtener_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Obtener información detallada de un curso específico por su ID.
    
    Incluye la lista completa de estudiantes asignados.
    """
    resultado = CursoService.obtener_por_id(db, id_curso)
    return ResponseModel.success(
        message="Curso obtenido exitosamente",
        data=resultado.model_dump(by_alias=True)
    )


@router.put("/{id_curso}", summary="RF-CUR-004: Actualizar Curso")
def actualizar_curso(
    id_curso: int,
    datos: CursoUpdateDTO,
    db: Session = Depends(get_db)
):
    """
    Actualizar información de un curso existente.
    
    Todos los campos son opcionales - solo se actualizan los campos enviados.
    """
    resultado = CursoService.actualizar_curso(db, id_curso, datos)
    return ResponseModel.success(
        message="Curso actualizado exitosamente",
        data=resultado.model_dump(by_alias=True)
    )


@router.delete("/{id_curso}", summary="RF-CUR-005: Eliminar Curso")
def eliminar_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un curso del sistema de forma permanente.
    
    Se eliminan automáticamente todas las asignaciones de estudiantes (cascada).
    """
    return CursoService.eliminar_curso(db, id_curso)


# ============= Filtros Avanzados =============

@router.get("/gestion/{gestion}/nivel/{nivel}", summary="RF-CUR-006: Listar Cursos por Gestión y Nivel")
def listar_por_gestion_nivel(
    gestion: str,
    nivel: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Filtrar cursos por gestión y nivel educativo específicos.
    
    Incluye estudiantes asignados a cada curso.
    Resultados ordenados por nivel y nombre de curso.
    """
    resultado = CursoService.listar_por_gestion_nivel(db, gestion, nivel, skip, limit)
    # Agregar alias 'id' para compatibilidad con frontend
    cursos_data = []
    for curso in resultado.cursos:
        curso_dict = curso.model_dump(by_alias=True)
        cursos_data.append(curso_dict)
    
    return ResponseModel.success(
        message=f"Lista de cursos filtrada exitosamente ({resultado.total} encontrados)",
        data=cursos_data
    )


# ============= Gestión de Gestiones =============

@router.post("/copiar-gestion", summary="RF-CUR-007: Copiar Cursos entre Gestiones")
def copiar_cursos_entre_gestiones(
    datos: CopiarGestionDTO,
    db: Session = Depends(get_db)
):
    """
    Copiar estructura completa de cursos de una gestión a otra.
    
    **Comportamiento:**
    - Copia solo la estructura: nombre, nivel y nueva gestión
    - NO copia estudiantes
    - Valida que existan cursos en origen
    - Valida que NO existan cursos en destino
    
    **Caso de uso:** Inicio de año escolar - copiar estructura de cursos del año anterior.
    """
    resultado = CursoService.copiar_cursos_entre_gestiones(db, datos)
    return ResponseModel.success(
        message="Cursos copiados exitosamente entre gestiones",
        data=resultado.model_dump()
    )
