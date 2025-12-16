from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.solicitud_retiro_masivo_service import SolicitudRetiroMasivoService
from app.modules.retiros_tempranos.dto import (
    SolicitudRetiroMasivoCreateDTO,
    SolicitudRetiroMasivoResponseDTO,
    SolicitudRetiroMasivoDetalladaResponseDTO,
    DerivarSolicitudMasivaDTO,
    CancelarSolicitudMasivaDTO
)
from app.core.database import get_db
from app.shared.decorators.auth_decorators import get_current_user, require_permissions
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/retiros-tempranos/solicitudes-masivas", tags=["Solicitudes de Retiro Masivo"])


def get_service(db: Session = Depends(get_db)) -> SolicitudRetiroMasivoService:
    """Inyección de dependencia del servicio"""
    return SolicitudRetiroMasivoService(db)


# ============================================================================
# ENDPOINTS PARA PROFESORES/ADMINISTRATIVOS
# ============================================================================

@router.post("/", response_model=SolicitudRetiroMasivoDetalladaResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("profesor", "admin", "recepcion", "regente")
async def crear_solicitud_masiva(
    solicitud_dto: SolicitudRetiroMasivoCreateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> SolicitudRetiroMasivoDetalladaResponseDTO:
    """
    **[PROFESOR/ADMIN/RECEPCIÓN/REGENTE]** Crear una nueva solicitud de retiro masivo
    
    - Requiere foto_evidencia obligatoria
    - Lista de estudiantes (mínimo 1)
    - Estado inicial: 'recibida' (automático)
    - Uso: paseos, excursiones, eventos grupales
    """
    return service.crear_solicitud(solicitud_dto, current_user.id_usuario)


@router.put("/{id_solicitud}/cancelar", response_model=SolicitudRetiroMasivoResponseDTO)
@require_permissions("profesor", "admin", "recepcion", "regente")
async def cancelar_solicitud_masiva(
    id_solicitud: int,
    cancelar_dto: CancelarSolicitudMasivaDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> SolicitudRetiroMasivoResponseDTO:
    """**[SOLICITANTE]** Cancelar una solicitud masiva propia (solo si no está aprobada/rechazada)"""
    return service.cancelar_solicitud(id_solicitud, cancelar_dto, current_user.id_usuario)


# ============================================================================
# ENDPOINTS PARA RECEPCIONISTAS
# ============================================================================

@router.get("/recibidas", response_model=List[SolicitudRetiroMasivoResponseDTO])
@require_permissions("recepcion")
async def listar_solicitudes_masivas_recibidas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> List[SolicitudRetiroMasivoResponseDTO]:
    """**[RECEPCIONISTA]** Listar solicitudes masivas recibidas (pendientes de derivar al regente)"""
    return service.listar_recibidas(skip, limit)


@router.put("/{id_solicitud}/derivar", response_model=SolicitudRetiroMasivoResponseDTO)
@require_permissions("recepcion")
async def derivar_solicitud_masiva(
    id_solicitud: int,
    derivar_dto: DerivarSolicitudMasivaDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> SolicitudRetiroMasivoResponseDTO:
    """**[RECEPCIONISTA]** Derivar solicitud masiva al regente (recibida → derivada)"""
    return service.derivar_solicitud(id_solicitud, derivar_dto)


# ============================================================================
# ENDPOINTS PARA REGENTES
# ============================================================================

@router.get("/derivadas", response_model=List[SolicitudRetiroMasivoResponseDTO])
@require_permissions("regente")
async def listar_solicitudes_masivas_derivadas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> List[SolicitudRetiroMasivoResponseDTO]:
    """**[REGENTE]** Listar solicitudes masivas derivadas (pendientes de aprobación/rechazo)"""
    return service.listar_derivadas(skip, limit)


# ============================================================================
# ENDPOINTS GENERALES (CONSULTA)
# ============================================================================

@router.get("/", response_model=List[SolicitudRetiroMasivoResponseDTO])
@require_permissions("recepcion", "regente", "admin")
async def listar_solicitudes_masivas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> List[SolicitudRetiroMasivoResponseDTO]:
    """**[ADMIN/RECEPCIÓN/REGENTE]** Listar todas las solicitudes masivas"""
    return service.listar_solicitudes(skip, limit)


@router.get("/{id_solicitud}", response_model=SolicitudRetiroMasivoDetalladaResponseDTO)
@require_permissions("recepcion", "regente", "admin", "profesor")
async def obtener_solicitud_masiva(
    id_solicitud: int,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroMasivoService = Depends(get_service)
) -> SolicitudRetiroMasivoDetalladaResponseDTO:
    """Obtener una solicitud masiva específica con su lista completa de estudiantes"""
    return service.obtener_solicitud(id_solicitud)
