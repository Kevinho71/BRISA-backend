from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.retiros_tempranos.services.motivo_retiro_service import MotivoRetiroService
from app.modules.retiros_tempranos.dto import (
    MotivoRetiroCreateDTO,
    MotivoRetiroUpdateDTO,
    MotivoRetiroResponseDTO
)

router = APIRouter(prefix="/api/motivos-retiro", tags=["motivos-retiro"])


@router.post("/", response_model=MotivoRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_motivo(
    motivo_dto: MotivoRetiroCreateDTO,
    service: MotivoRetiroService = Depends()
) -> MotivoRetiroResponseDTO:
    """Crear un nuevo motivo de retiro"""
    return await service.create_motivo(motivo_dto)


@router.get("/{motivo_id}", response_model=MotivoRetiroResponseDTO)
async def get_motivo(
    motivo_id: int,
    service: MotivoRetiroService = Depends()
) -> MotivoRetiroResponseDTO:
    """Obtener un motivo de retiro por ID"""
    return await service.get_motivo(motivo_id)


@router.get("/", response_model=List[MotivoRetiroResponseDTO])
async def get_all_motivos(
    skip: int = 0,
    limit: int = 100,
    service: MotivoRetiroService = Depends()
) -> List[MotivoRetiroResponseDTO]:
    """Obtener todos los motivos de retiro con paginación"""
    return await service.get_all_motivos(skip=skip, limit=limit)


@router.get("/activos", response_model=List[MotivoRetiroResponseDTO])
async def get_motivos_activos(
    service: MotivoRetiroService = Depends()
) -> List[MotivoRetiroResponseDTO]:
    """Obtener los motivos de retiro activos"""
    return await service.get_motivos_activos()


@router.get("/severidad/{severidad}", response_model=List[MotivoRetiroResponseDTO])
async def get_motivos_by_severidad(
    severidad: str,
    service: MotivoRetiroService = Depends()
) -> List[MotivoRetiroResponseDTO]:
    """Obtener motivos de retiro por nivel de severidad"""
    return await service.get_motivos_by_severidad(severidad)


@router.put("/{motivo_id}", response_model=MotivoRetiroResponseDTO)
async def update_motivo(
    motivo_id: int,
    motivo_dto: MotivoRetiroUpdateDTO,
    service: MotivoRetiroService = Depends()
) -> MotivoRetiroResponseDTO:
    """Actualizar un motivo de retiro"""
    return await service.update_motivo(motivo_id, motivo_dto)


@router.delete("/{motivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_motivo(
    motivo_id: int,
    service: MotivoRetiroService = Depends()
):
    """Eliminar un motivo de retiro"""
    if not await service.delete_motivo(motivo_id):
        raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")