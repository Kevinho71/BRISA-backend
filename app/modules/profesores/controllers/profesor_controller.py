# app/modules/profesores/controllers/profesor_controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.profesores.services.profesor_service import ProfesorService
from app.modules.profesores.dto.profesor_dto import (
    ProfesorCreateDTO,
    ProfesorUpdateDTO,
    ProfesorResponseDTO,
    AsignarCursoMateriaDTO,
    ProfesorCursoMateriaResponseDTO
)

router = APIRouter()


@router.get("/profesores", response_model=List[ProfesorResponseDTO], status_code=status.HTTP_200_OK)
def get_all_profesores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los profesores con paginación
    """
    return ProfesorService.get_all_profesores(db, skip, limit)


@router.get("/profesores/{id_profesor}", response_model=ProfesorResponseDTO, status_code=status.HTTP_200_OK)
def get_profesor(
    id_profesor: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un profesor por ID
    """
    return ProfesorService.get_profesor_by_id(db, id_profesor)


@router.post("/profesores", response_model=ProfesorResponseDTO, status_code=status.HTTP_201_CREATED)
def create_profesor(
    data: ProfesorCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo profesor
    """
    return ProfesorService.create_profesor(db, data)


@router.put("/profesores/{id_profesor}", response_model=ProfesorResponseDTO, status_code=status.HTTP_200_OK)
def update_profesor(
    id_profesor: int,
    data: ProfesorUpdateDTO,
    db: Session = Depends(get_db)
):
    """
    Actualiza un profesor existente
    """
    return ProfesorService.update_profesor(db, id_profesor, data)


@router.delete("/profesores/{id_profesor}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profesor(
    id_profesor: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un profesor
    """
    ProfesorService.delete_profesor(db, id_profesor)
    return None


# ==================== ASIGNACIÓN CURSO-MATERIA ====================

@router.post("/profesores/asignar-curso-materia", response_model=ProfesorCursoMateriaResponseDTO, status_code=status.HTTP_201_CREATED)
def asignar_curso_materia(
    data: AsignarCursoMateriaDTO,
    db: Session = Depends(get_db)
):
    """
    Asigna un curso y materia a un profesor
    """
    return ProfesorService.asignar_curso_materia(db, data)


@router.get("/profesores/{id_profesor}/asignaciones", response_model=List[ProfesorCursoMateriaResponseDTO], status_code=status.HTTP_200_OK)
def get_asignaciones_profesor(
    id_profesor: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las asignaciones de curso-materia de un profesor
    """
    return ProfesorService.get_asignaciones_profesor(db, id_profesor)


@router.delete("/profesores/{id_profesor}/asignaciones/{id_curso}/{id_materia}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asignacion(
    id_profesor: int,
    id_curso: int,
    id_materia: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una asignación de curso-materia de un profesor
    """
    ProfesorService.eliminar_asignacion(db, id_profesor, id_curso, id_materia)
    return None