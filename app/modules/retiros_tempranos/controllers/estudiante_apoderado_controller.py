from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.estudiante_apoderado_service import EstudianteApoderadoService
from app.modules.retiros_tempranos.dto import (
    EstudianteApoderadoCreateDTO,
    EstudianteApoderadoUpdateDTO,
    EstudianteApoderadoResponseDTO
)
from app.core.database import get_db
from app.modules.retiros_tempranos.repositories import EstudianteApoderadoRepository

router = APIRouter(prefix="/api/estudiantes-apoderados", tags=["estudiantes-apoderados"])


def get_estudiante_apoderado_service(db: Session = Depends(get_db)) -> EstudianteApoderadoService:
    repo = EstudianteApoderadoRepository(db)
    return EstudianteApoderadoService(repo)


@router.post("/", response_model=EstudianteApoderadoResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_relacion(
    relacion_dto: EstudianteApoderadoCreateDTO,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> EstudianteApoderadoResponseDTO:
    """Crear una nueva relación estudiante-apoderado"""
    return service.create_relacion(relacion_dto)


@router.get("/estudiante/{id_estudiante}/apoderado/{id_apoderado}", response_model=EstudianteApoderadoResponseDTO)
async def get_relacion(
    id_estudiante: int,
    id_apoderado: int,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> EstudianteApoderadoResponseDTO:
    """Obtener una relación específica estudiante-apoderado"""
    return service.get_relacion(id_estudiante, id_apoderado)


@router.get("/estudiante/{id_estudiante}", response_model=List[EstudianteApoderadoResponseDTO])
async def get_apoderados_by_estudiante(
    id_estudiante: int,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> List[EstudianteApoderadoResponseDTO]:
    """Obtener todos los apoderados de un estudiante"""
    return service.get_apoderados_by_estudiante(id_estudiante)


@router.get("/apoderado/{id_apoderado}", response_model=List[EstudianteApoderadoResponseDTO])
async def get_estudiantes_by_apoderado(
    id_apoderado: int,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> List[EstudianteApoderadoResponseDTO]:
    """Obtener todos los estudiantes de un apoderado"""
    return service.get_estudiantes_by_apoderado(id_apoderado)


@router.get("/estudiante/{id_estudiante}/contacto-principal", response_model=EstudianteApoderadoResponseDTO)
async def get_contacto_principal(
    id_estudiante: int,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> EstudianteApoderadoResponseDTO:
    """Obtener el apoderado de contacto principal de un estudiante"""
    return service.get_contacto_principal(id_estudiante)


@router.put("/estudiante/{id_estudiante}/apoderado/{id_apoderado}/contacto-principal", response_model=EstudianteApoderadoResponseDTO)
async def set_contacto_principal(
    id_estudiante: int,
    id_apoderado: int,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> EstudianteApoderadoResponseDTO:
    """Establecer un apoderado como contacto principal"""
    return service.set_contacto_principal(id_estudiante, id_apoderado)


@router.put("/estudiante/{id_estudiante}/apoderado/{id_apoderado}", response_model=EstudianteApoderadoResponseDTO)
async def update_relacion(
    id_estudiante: int,
    id_apoderado: int,
    relacion_dto: EstudianteApoderadoUpdateDTO,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
) -> EstudianteApoderadoResponseDTO:
    """Actualizar una relación estudiante-apoderado"""
    return service.update_relacion(id_estudiante, id_apoderado, relacion_dto)


@router.delete("/estudiante/{id_estudiante}/apoderado/{id_apoderado}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relacion(
    id_estudiante: int,
    id_apoderado: int,
    service: EstudianteApoderadoService = Depends(get_estudiante_apoderado_service)
):
    """Eliminar una relación estudiante-apoderado"""
    if not service.delete_relacion(id_estudiante, id_apoderado):
        raise HTTPException(status_code=404, detail="Relación no encontrada")
