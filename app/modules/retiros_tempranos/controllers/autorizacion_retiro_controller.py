from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.autorizacion_retiro_service import AutorizacionRetiroService
from app.modules.retiros_tempranos.services.solicitud_retiro_masivo_service import SolicitudRetiroMasivoService
from app.modules.retiros_tempranos.dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO,
    AprobarRechazarSolicitudMasivaDTO,
    SolicitudRetiroMasivoResponseDTO
)
from app.core.database import get_db
from app.modules.retiros_tempranos.repositories import AutorizacionRetiroRepository, SolicitudRetiroRepository
from app.shared.decorators.auth_decorators import require_permissions, get_current_user
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/autorizaciones-retiro", tags=["autorizaciones-retiro"])


def get_autorizacion_retiro_service(db: Session = Depends(get_db)) -> AutorizacionRetiroService:
    repo = AutorizacionRetiroRepository(db)
    solicitud_repo = SolicitudRetiroRepository(db)
    return AutorizacionRetiroService(repo, solicitud_repo)


def get_solicitud_masiva_service(db: Session = Depends(get_db)) -> SolicitudRetiroMasivoService:
    return SolicitudRetiroMasivoService(db)


@router.put("/{id_solicitud}/decision", response_model=AutorizacionRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("regente")
async def create_autorizacion(
    id_solicitud: int,
    autorizacion_dto: AutorizacionRetiroCreateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> AutorizacionRetiroResponseDTO:
    """**[REGENTE]** Aprobar o rechazar una solicitud de retiro"""
    return service.create_autorizacion(id_solicitud, autorizacion_dto, current_user.id_usuario)


@router.get("/{autorizacion_id}", response_model=AutorizacionRetiroResponseDTO)
@require_permissions("regente")
async def get_autorizacion(
    autorizacion_id: int,
    current_user: Usuario = Depends(get_current_user),
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> AutorizacionRetiroResponseDTO:
    """**[REGENTE]** Obtener una autorización de retiro por ID"""
    return service.get_autorizacion(autorizacion_id)


@router.get("/", response_model=List[AutorizacionRetiroResponseDTO])
@require_permissions("regente")
async def get_all_autorizaciones(
    current_user: Usuario = Depends(get_current_user),
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> List[AutorizacionRetiroResponseDTO]:
    """**[REGENTE]** Obtener todas las autorizaciones de retiro"""
    return service.get_all_autorizaciones()


@router.put("/{autorizacion_id}", response_model=AutorizacionRetiroResponseDTO)
@require_permissions("regente")
async def update_autorizacion(
    autorizacion_id: int,
    autorizacion_dto: AutorizacionRetiroUpdateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: AutorizacionRetiroService = Depends(get_autorizacion_retiro_service)
) -> AutorizacionRetiroResponseDTO:
    """**[REGENTE]** Actualizar una autorización de retiro"""
    return service.update_autorizacion(autorizacion_id, autorizacion_dto)


# ============================================================================
# ENDPOINTS PARA SOLICITUDES MASIVAS
# ============================================================================

@router.put("/masiva/{id_solicitud_masiva}/decision", response_model=SolicitudRetiroMasivoResponseDTO)
@require_permissions("regente")
async def aprobar_rechazar_solicitud_masiva(
    id_solicitud_masiva: int,
    decision_dto: AprobarRechazarSolicitudMasivaDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_solicitud_masiva_service)
) -> SolicitudRetiroMasivoResponseDTO:
    """**[REGENTE]** Aprobar o rechazar una solicitud de retiro masiva (derivada → aprobada/rechazada)"""
    return service.aprobar_rechazar_solicitud(id_solicitud_masiva, decision_dto, current_user.id_usuario)

