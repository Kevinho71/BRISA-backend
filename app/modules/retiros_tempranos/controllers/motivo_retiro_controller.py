from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.motivo_retiro_service import MotivoRetiroService
from app.modules.retiros_tempranos.dto import (
    MotivoRetiroCreateDTO,
    MotivoRetiroUpdateDTO,
    MotivoRetiroResponseDTO
)
from app.core.database import get_db
from app.modules.retiros_tempranos.repositories import MotivoRetiroRepository
from app.shared.decorators.auth_decorators import require_permissions, get_current_user
from app.modules.usuarios.models.usuario_models import Usuario

router = APIRouter(prefix="/api/motivos-retiro", tags=["motivos-retiro"])


def get_motivo_retiro_service(db: Session = Depends(get_db)) -> MotivoRetiroService:
    repo = MotivoRetiroRepository(db)
    return MotivoRetiroService(repo)


@router.post("/", response_model=MotivoRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("admin", "regente", "recepcion")
async def create_motivo(
    motivo_dto: MotivoRetiroCreateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
) -> MotivoRetiroResponseDTO:
    """**[DIRECTOR/REGENTE/RECEPCIÓN]** Crear un nuevo motivo de retiro"""
    return service.create_motivo(motivo_dto)


@router.get("/", response_model=List[MotivoRetiroResponseDTO])
@require_permissions("admin", "regente", "recepcion", "profesor", "apoderado")
async def get_all_motivos(
    current_user: Usuario = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
) -> List[MotivoRetiroResponseDTO]:
    """**[TODOS]** Obtener todos los motivos de retiro con paginación"""
    return service.get_all_motivos(skip=skip, limit=limit)


@router.get("/activos", response_model=List[MotivoRetiroResponseDTO])
@require_permissions("admin", "regente", "recepcion", "profesor", "apoderado")
async def get_motivos_activos(
    current_user: Usuario = Depends(get_current_user),
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
) -> List[MotivoRetiroResponseDTO]:
    """**[TODOS]** Obtener los motivos de retiro activos"""
    return service.get_motivos_activos()


@router.get("/severidad/{severidad}", response_model=List[MotivoRetiroResponseDTO])
@require_permissions("admin", "regente", "recepcion", "profesor", "apoderado")
async def get_motivos_by_severidad(
    severidad: str,
    current_user: Usuario = Depends(get_current_user),
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
) -> List[MotivoRetiroResponseDTO]:
    """**[TODOS]** Obtener motivos de retiro por nivel de severidad"""
    return service.get_motivos_by_severidad(severidad)


@router.get("/{motivo_id:int}", response_model=MotivoRetiroResponseDTO)
@require_permissions("admin", "regente", "recepcion", "profesor", "apoderado")
async def get_motivo(
    motivo_id: int,
    current_user: Usuario = Depends(get_current_user),
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
) -> MotivoRetiroResponseDTO:
    """**[TODOS]** Obtener un motivo de retiro por ID"""
    return service.get_motivo(motivo_id)


@router.put("/{motivo_id:int}", response_model=MotivoRetiroResponseDTO)
@require_permissions("admin", "regente", "recepcion")
async def update_motivo(
    motivo_id: int,
    motivo_dto: MotivoRetiroUpdateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
) -> MotivoRetiroResponseDTO:
    """**[DIRECTOR/REGENTE/RECEPCIÓN]** Actualizar un motivo de retiro"""
    return service.update_motivo(motivo_id, motivo_dto)


@router.delete("/{motivo_id:int}", status_code=status.HTTP_204_NO_CONTENT)
@require_permissions("admin")
async def delete_motivo(
    motivo_id: int,
    current_user: Usuario = Depends(get_current_user),
    service: MotivoRetiroService = Depends(get_motivo_retiro_service)
):
    """**[DIRECTOR]** Eliminar un motivo de retiro"""
    if not service.delete_motivo(motivo_id):
        raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")
