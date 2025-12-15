from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.autorizacion_retiro_service import AutorizacionRetiroService
from app.modules.retiros_tempranos.dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO
)
from app.core.database import get_db
from app.modules.retiros_tempranos.repositories import AutorizacionRetiroRepository, SolicitudRetiroRepository
from app.shared.decorators.auth_decorators import require_permissions

router = APIRouter(prefix="/api/autorizaciones-retiro", tags=["autorizaciones-retiro"])


def get_autorizacion_retiro_service(db: Session = Depends(get_db)) -> AutorizacionRetiroService:
    repo = AutorizacionRetiroRepository(db)
    solicitud_repo = SolicitudRetiroRepository(db)
    return AutorizacionRetiroService(repo, solicitud_repo)


@router.post("/", response_model=AutorizacionRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("regente")
async def create_autorizacion(
    autorizacion_dto: AutorizacionRetiroCreateDTO,
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> AutorizacionRetiroResponseDTO:
    """**[REGENTE]** Crear una nueva autorización de retiro"""
    return service.create_autorizacion(autorizacion_dto)


@router.get("/{autorizacion_id}", response_model=AutorizacionRetiroResponseDTO)
@require_permissions("regente")
async def get_autorizacion(
    autorizacion_id: int,
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> AutorizacionRetiroResponseDTO:
    """**[REGENTE]** Obtener una autorización de retiro por ID"""
    return service.get_autorizacion(autorizacion_id)


@router.get("/", response_model=List[AutorizacionRetiroResponseDTO])
@require_permissions("regente")
async def get_all_autorizaciones(
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> List[AutorizacionRetiroResponseDTO]:
    """**[REGENTE]** Obtener todas las autorizaciones de retiro"""
    return service.get_all_autorizaciones()


@router.put("/{autorizacion_id}", response_model=AutorizacionRetiroResponseDTO)
@require_permissions("regente")
async def update_autorizacion(
    autorizacion_id: int,
    autorizacion_dto: AutorizacionRetiroUpdateDTO,
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> AutorizacionRetiroResponseDTO:
    """**[REGENTE]** Actualizar una autorización de retiro"""
    return service.update_autorizacion(autorizacion_id, autorizacion_dto)


@router.delete("/{autorizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_permissions("regente")
async def delete_autorizacion(
    autorizacion_id: int,
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
):
    """**[REGENTE]** Eliminar una autorización de retiro"""
    if not service.delete_autorizacion(autorizacion_id):
        raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
