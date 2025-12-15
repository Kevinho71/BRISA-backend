from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.administracion.services.materia_service import MateriaService
from app.modules.administracion.dto.materia_dto import MateriaDTO, MateriaCreateDTO, MateriaUpdateDTO
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.modules.usuarios.models.usuario_models import Usuario

router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("/", response_model=List[MateriaDTO])
def listar_materias(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Lista todas las materias disponibles.
    """
    return MateriaService.listar_materias(db)

@router.get("/{materia_id}", response_model=MateriaDTO)
def obtener_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Obtiene una materia por su ID.
    """
    return MateriaService.obtener_materia(db, materia_id)

@router.post("/", response_model=MateriaDTO, status_code=status.HTTP_201_CREATED)
def crear_materia(
    materia: MateriaCreateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Crea una nueva materia.
    """
    return MateriaService.crear_materia(db, materia)

@router.put("/{materia_id}", response_model=MateriaDTO)
def actualizar_materia(
    materia_id: int,
    materia: MateriaUpdateDTO,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Actualiza una materia existente.
    """
    return MateriaService.actualizar_materia(db, materia_id, materia)

@router.delete("/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
):
    """
    Elimina una materia.
    """
    MateriaService.eliminar_materia(db, materia_id)
