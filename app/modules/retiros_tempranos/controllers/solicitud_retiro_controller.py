from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.solicitud_retiro_service import SolicitudRetiroService
from app.modules.retiros_tempranos.dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroResponseDTO,
    RecibirSolicitudDTO,
    DerivarSolicitudDTO,
    AprobarRechazarSolicitudDTO,
    CancelarSolicitudDTO
)
from app.core.database import get_db
from app.shared.decorators.auth_decorators import get_current_user, require_permissions
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/retiros-tempranos/solicitudes", tags=["Solicitudes de Retiro Individual"])


def get_service(db: Session = Depends(get_db)) -> SolicitudRetiroService:
    """Inyección de dependencia del servicio"""
    return SolicitudRetiroService(db)


# ============================================================================
# ENDPOINTS PARA APODERADOS
# ============================================================================

@router.post("/", response_model=SolicitudRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("apoderado")
async def crear_solicitud_individual(
    solicitud_dto: SolicitudRetiroCreateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> SolicitudRetiroResponseDTO:
    """
    **[APODERADO]** Crear una nueva solicitud de retiro individual
    
    - Requiere foto_evidencia obligatoria
    - Valida relación apoderado-estudiante
    - Estado inicial: 'pendiente'
    """
    # Obtener id_apoderado del usuario actual
    apoderado = db.query(db.query(db.execute(
        "SELECT id_apoderado FROM apoderados WHERE id_persona = :id_persona",
        {"id_persona": current_user.id_persona}
    ).fetchone()).scalar())
    
    if not apoderado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no tiene perfil de apoderado"
        )
    
    return service.crear_solicitud(solicitud_dto, apoderado)


@router.get("/mis-solicitudes", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("apoderado")
async def listar_mis_solicitudes(
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> List[SolicitudRetiroResponseDTO]:
    """**[APODERADO]** Listar las solicitudes del apoderado autenticado"""
    apoderado = db.execute(
        "SELECT id_apoderado FROM apoderados WHERE id_persona = :id_persona",
        {"id_persona": current_user.id_persona}
    ).fetchone()
    
    if not apoderado:
        return []
    
    return service.listar_por_apoderado(apoderado[0])


@router.put("/{id_solicitud}/cancelar", response_model=SolicitudRetiroResponseDTO)
@require_permissions("apoderado")
async def cancelar_solicitud(
    id_solicitud: int,
    cancelar_dto: CancelarSolicitudDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> SolicitudRetiroResponseDTO:
    """**[APODERADO]** Cancelar una solicitud propia (solo si no está aprobada/rechazada)"""
    apoderado = db.execute(
        "SELECT id_apoderado FROM apoderados WHERE id_persona = :id_persona",
        {"id_persona": current_user.id_persona}
    ).fetchone()
    
    if not apoderado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no es apoderado")
    
    return service.cancelar_solicitud(id_solicitud, cancelar_dto, apoderado[0])


@router.delete("/{id_solicitud}")
@require_permissions("apoderado")
async def eliminar_solicitud(
    id_solicitud: int,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> dict:
    """**[APODERADO]** Eliminar una solicitud propia (solo si está en estado 'pendiente')"""
    apoderado = db.execute(
        "SELECT id_apoderado FROM apoderados WHERE id_persona = :id_persona",
        {"id_persona": current_user.id_persona}
    ).fetchone()
    
    if not apoderado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no es apoderado")
    
    eliminado = service.eliminar_solicitud(id_solicitud, apoderado[0])
    
    if eliminado:
        return {"message": "Solicitud eliminada exitosamente"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo eliminar la solicitud")


# ============================================================================
# ENDPOINTS PARA RECEPCIONISTAS
# ============================================================================

@router.get("/pendientes", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion")
async def listar_solicitudes_pendientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[RECEPCIONISTA]** Listar solicitudes pendientes de recepción"""
    return service.listar_pendientes(skip, limit)


@router.get("/recibidas", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion")
async def listar_solicitudes_recibidas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[RECEPCIONISTA]** Listar solicitudes recibidas (pendientes de derivar)"""
    return service.listar_recibidas(skip, limit)


@router.put("/{id_solicitud}/recibir", response_model=SolicitudRetiroResponseDTO)
@require_permissions("recepcion")
async def recibir_solicitud(
    id_solicitud: int,
    recibir_dto: RecibirSolicitudDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service)
) -> SolicitudRetiroResponseDTO:
    """**[RECEPCIONISTA]** Marcar solicitud como recibida (pendiente → recibida)"""
    return service.recibir_solicitud(id_solicitud, recibir_dto, current_user.id_usuario)


@router.put("/{id_solicitud}/derivar", response_model=SolicitudRetiroResponseDTO)
@require_permissions("recepcion")
async def derivar_solicitud(
    id_solicitud: int,
    derivar_dto: DerivarSolicitudDTO,
    service: SolicitudRetiroService = Depends(get_service)
) -> SolicitudRetiroResponseDTO:
    """**[RECEPCIONISTA]** Derivar solicitud a un regente (recibida → derivada)"""
    return service.derivar_solicitud(id_solicitud, derivar_dto)


# ============================================================================
# ENDPOINTS PARA REGENTES
# ============================================================================

@router.get("/derivadas-a-mi", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("regente")
async def listar_solicitudes_derivadas_a_mi(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[REGENTE]** Listar solicitudes derivadas al regente autenticado"""
    return service.listar_derivadas_a_regente(current_user.id_usuario, skip, limit)


@router.put("/{id_solicitud}/decision", response_model=SolicitudRetiroResponseDTO)
@require_permissions("regente")
async def aprobar_rechazar_solicitud(
    id_solicitud: int,
    decision_dto: AprobarRechazarSolicitudDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service)
) -> SolicitudRetiroResponseDTO:
    """**[REGENTE]** Aprobar o rechazar una solicitud (derivada → aprobada/rechazada)"""
    return service.aprobar_rechazar_solicitud(id_solicitud, decision_dto, current_user.id_usuario)


# ============================================================================
# ENDPOINTS GENERALES (CONSULTA)
# ============================================================================

@router.get("/", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion", "regente", "admin")
async def listar_solicitudes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[ADMIN/RECEPCIÓN/REGENTE]** Listar todas las solicitudes individuales"""
    return service.listar_solicitudes(skip, limit)


@router.get("/{id_solicitud}", response_model=SolicitudRetiroResponseDTO)
async def obtener_solicitud(
    id_solicitud: int,
    service: SolicitudRetiroService = Depends(get_service)
) -> SolicitudRetiroResponseDTO:
    """Obtener una solicitud específica por ID"""
    return service.obtener_solicitud(id_solicitud)


@router.get("/estudiante/{id_estudiante}", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion", "regente", "admin", "apoderado")
async def listar_solicitudes_por_estudiante(
    id_estudiante: int,
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """Listar solicitudes de un estudiante específico"""
    return service.listar_por_estudiante(id_estudiante)
