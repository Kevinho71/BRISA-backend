from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.retiros_tempranos.services.autorizacion_retiro_service import AutorizacionRetiroService
from app.modules.retiros_tempranos.dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO
)

router = APIRouter(prefix="/api/autorizaciones-retiro", tags=["autorizaciones-retiro"])


@router.post("/", response_model=AutorizacionRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_autorizacion(
    autorizacion_dto: AutorizacionRetiroCreateDTO,
    service: AutorizacionRetiroService = Depends()
) -> AutorizacionRetiroResponseDTO:
    """Crear una nueva autorización de retiro"""
    return await service.create_autorizacion(autorizacion_dto)


@router.get("/{autorizacion_id}", response_model=AutorizacionRetiroResponseDTO)
async def get_autorizacion(
    autorizacion_id: int,
    service: AutorizacionRetiroService = Depends()
) -> AutorizacionRetiroResponseDTO:
    """Obtener una autorización de retiro por ID"""
    return await service.get_autorizacion(autorizacion_id)


@router.get("/", response_model=List[AutorizacionRetiroResponseDTO])
async def get_all_autorizaciones(
    service: AutorizacionRetiroService = Depends()
) -> List[AutorizacionRetiroResponseDTO]:
    """Obtener todas las autorizaciones de retiro"""
    return await service.get_all_autorizaciones()


@router.put("/{autorizacion_id}", response_model=AutorizacionRetiroResponseDTO)
async def update_autorizacion(
    autorizacion_id: int,
    autorizacion_dto: AutorizacionRetiroUpdateDTO,
    service: AutorizacionRetiroService = Depends()
) -> AutorizacionRetiroResponseDTO:
    """Actualizar una autorización de retiro"""
    return await service.update_autorizacion(autorizacion_id, autorizacion_dto)


@router.delete("/{autorizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_autorizacion(
    autorizacion_id: int,
    service: AutorizacionRetiroService = Depends()
):
    """Eliminar una autorización de retiro"""
    if not await service.delete_autorizacion(autorizacion_id):
        raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")