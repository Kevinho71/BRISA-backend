"""Controlador (router) para el módulo de Cursos."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.extensions import get_db
from app.modules.administracion.services.curso_service import CursoService
from app.modules.administracion.dto.curso_dto import (
    CursoDTO,
    EstudianteListResponseDTO,
    ProfesorListResponseDTO
)


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[CursoDTO])
def listar_cursos(db: Session = Depends(get_db)):
    """
    Lista todos los cursos disponibles.
    Útil para poblar selects en el frontend.
    """
    return CursoService.listar_cursos(db)


@router.get("/{curso_id}", response_model=CursoDTO)
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un curso específico por ID.
    """
    return CursoService.obtener_curso(db, curso_id)


@router.get("/{curso_id}/students", response_model=EstudianteListResponseDTO)
def listar_estudiantes_por_curso(
    curso_id: int,
    name: Optional[str] = Query(None, description="Filtrar por nombre del estudiante"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Session = Depends(get_db)
):
    """
    Lista estudiantes de un curso específico.
    
    Parámetros:
    - **name**: Filtro por nombre, apellido paterno o materno del estudiante
    - **page**: Número de página (por defecto 1)
    - **page_size**: Cantidad de resultados por página (por defecto 10, máximo 100)
    """
    return CursoService.listar_estudiantes_por_curso(db, curso_id, name, page, page_size)


@router.get("/{curso_id}/teachers", response_model=ProfesorListResponseDTO)
def listar_profesores_por_curso(
    curso_id: int,
    name: Optional[str] = Query(None, description="Filtrar por nombre del profesor"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Session = Depends(get_db)
):
    """
    Lista profesores de un curso específico.
    
    Parámetros:
    - **name**: Filtro por nombre, apellido paterno o materno del profesor
    - **page**: Número de página (por defecto 1)
    - **page_size**: Cantidad de resultados por página (por defecto 10, máximo 100)
    """
    return CursoService.listar_profesores_por_curso(db, curso_id, name, page, page_size)
