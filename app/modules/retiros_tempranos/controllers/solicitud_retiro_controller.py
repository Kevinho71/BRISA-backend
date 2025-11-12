from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.solicitud_retiro_service import SolicitudRetiroService
from app.modules.retiros_tempranos.dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO,
    EstadoSolicitudEnum
)
from app.core.extensions import get_db
from app.modules.retiros_tempranos.repositories import SolicitudRetiroRepository

router = APIRouter(prefix="/api/solicitudes-retiro", tags=["solicitudes-retiro"])


def get_solicitud_retiro_service(db: Session = Depends(get_db)) -> SolicitudRetiroService:
    repo = SolicitudRetiroRepository(db)
    return SolicitudRetiroService(repo)


@router.post("/", response_model=SolicitudRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_solicitud(
    solicitud_dto: SolicitudRetiroCreateDTO,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> SolicitudRetiroResponseDTO:
    """Crear una nueva solicitud de retiro (estado inicial: recibida, automáticamente)"""
    return service.create_solicitud(solicitud_dto)


@router.get("/", response_model=List[SolicitudRetiroResponseDTO])
async def get_all_solicitudes(
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> List[SolicitudRetiroResponseDTO]:
    """Obtener todas las solicitudes de retiro"""
    return service.get_all_solicitudes()


@router.get("/estado/{estado}", response_model=List[SolicitudRetiroResponseDTO])
async def get_solicitudes_by_estado(
    estado: EstadoSolicitudEnum,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> List[SolicitudRetiroResponseDTO]:
    """Obtener solicitudes por estado (recibida, derivada, aprobada, rechazada, cancelada)"""
    return service.get_solicitudes_by_estado(estado)


@router.get("/{solicitud_id}", response_model=SolicitudRetiroResponseDTO)
async def get_solicitud(
    solicitud_id: int,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> SolicitudRetiroResponseDTO:
    """Obtener una solicitud de retiro por ID"""
    return service.get_solicitud(solicitud_id)


@router.get("/estudiante/{estudiante_id}", response_model=List[SolicitudRetiroResponseDTO])
async def get_solicitudes_by_estudiante(
    estudiante_id: int,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> List[SolicitudRetiroResponseDTO]:
    """Obtener todas las solicitudes de retiro de un estudiante"""
    return service.get_solicitudes_by_estudiante(estudiante_id)


@router.post("/{solicitud_id}/derivar", response_model=SolicitudRetiroResponseDTO)
async def derivar_solicitud(
    solicitud_id: int,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> SolicitudRetiroResponseDTO:
    """RECEPCIONISTA: Derivar solicitud al regente (recibida → derivada, automático sin body)"""
    return service.derivar_solicitud(solicitud_id)


@router.put("/{solicitud_id}", response_model=SolicitudRetiroResponseDTO)
async def update_solicitud(
    solicitud_id: int,
    solicitud_dto: SolicitudRetiroUpdateDTO,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
) -> SolicitudRetiroResponseDTO:
    """Actualizar una solicitud de retiro"""
    return service.update_solicitud(solicitud_id, solicitud_dto)


@router.delete("/{solicitud_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solicitud(
    solicitud_id: int,
    service: SolicitudRetiroService = Depends(get_solicitud_retiro_service)
):
    """Eliminar una solicitud de retiro"""
    if not service.delete_solicitud(solicitud_id):
        raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
