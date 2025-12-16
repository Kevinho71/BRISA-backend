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
from app.modules.retiros_tempranos.models import Apoderado, EstudianteApoderado

router = APIRouter(prefix="/api/retiros-tempranos/solicitudes", tags=["Solicitudes de Retiro Individual"])


def get_service(db: Session = Depends(get_db)) -> SolicitudRetiroService:
    """Inyección de dependencia del servicio"""
    return SolicitudRetiroService(db)


# ============================================================================
# ENDPOINTS PARA APODERADOS
# ============================================================================

@router.post("/", response_model=SolicitudRetiroResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("apoderado", "profesor")
async def crear_solicitud_individual(
    solicitud_dto: SolicitudRetiroCreateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> SolicitudRetiroResponseDTO:
    """
    **[APODERADO/PROFESOR]** Crear una nueva solicitud de retiro individual
    
    - El id_apoderado se obtiene automáticamente del usuario autenticado
    - Valida relación apoderado-estudiante (solo puede solicitar para sus estudiantes)
    - Requiere foto_evidencia obligatoria
    - Estado inicial: 'recibida'
    """
    from app.modules.retiros_tempranos.models import Apoderado, EstudianteApoderado
    
    # 1. Obtener apoderado del usuario autenticado
    apoderado = db.query(Apoderado).filter(
        Apoderado.id_persona == current_user.id_persona
    ).first()
    
    if not apoderado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene perfil de apoderado registrado"
        )
    
    # 2. Validar que el estudiante esté relacionado con el apoderado
    #    Query optimizado con EXISTS
    relacion_existe = db.query(
        db.query(EstudianteApoderado).filter(
            EstudianteApoderado.id_apoderado == apoderado.id_apoderado,
            EstudianteApoderado.id_estudiante == solicitud_dto.id_estudiante
        ).exists()
    ).scalar()
    
    if not relacion_existe:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tiene permisos para solicitar retiro del estudiante {solicitud_dto.id_estudiante}. Solo puede solicitar para estudiantes bajo su tutela."
        )
    
    # 3. Crear la solicitud (el servicio ya no necesita id_apoderado como parámetro)
    return service.crear_solicitud(solicitud_dto, apoderado.id_apoderado)


@router.get("/mis-solicitudes", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("apoderado")
async def listar_mis_solicitudes(
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> List[SolicitudRetiroResponseDTO]:
    """
    **[APODERADO]** Listar todas las solicitudes creadas por el apoderado autenticado
    
    Retorna solo las solicitudes del apoderado logueado.
    """
    from app.modules.retiros_tempranos.models import Apoderado
    
    # Query optimizado: obtener id_apoderado directamente
    apoderado = db.query(Apoderado.id_apoderado).filter(
        Apoderado.id_persona == current_user.id_persona
    ).scalar()
    
    if not apoderado:
        # Si no es apoderado, retornar lista vacía
        return []
    
    return service.listar_por_apoderado(apoderado)


@router.put("/{id_solicitud}/cancelar", response_model=SolicitudRetiroResponseDTO)
@require_permissions("apoderado", "recepcion", "regente")
async def cancelar_solicitud(
    id_solicitud: int,
    cancelar_dto: CancelarSolicitudDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> SolicitudRetiroResponseDTO:
    """**[APODERADO/RECEPCIÓN/REGENTE]** Cancelar una solicitud propia (solo si no está aprobada/rechazada)"""
    # Obtener apoderado usando ORM en lugar de SQL raw
    apoderado = db.query(Apoderado).filter(
        Apoderado.id_persona == current_user.id_persona
    ).first()
    
    if not apoderado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no es apoderado")
    
    return service.cancelar_solicitud(id_solicitud, cancelar_dto, apoderado.id_apoderado)


@router.delete("/{id_solicitud}")
@require_permissions("apoderado", "recepcion", "regente")
async def eliminar_solicitud(
    id_solicitud: int,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> dict:
    """**[APODERADO/RECEPCIÓN/REGENTE]** Eliminar una solicitud propia (solo si está en estado 'recibida')"""
    # Obtener apoderado usando ORM en lugar de SQL raw
    apoderado = db.query(Apoderado).filter(
        Apoderado.id_persona == current_user.id_persona
    ).first()
    
    if not apoderado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no es apoderado")
    
    eliminado = service.eliminar_solicitud(id_solicitud, apoderado.id_apoderado)
    
    if eliminado:
        return {"message": "Solicitud eliminada exitosamente"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo eliminar la solicitud")


# ============================================================================
# ENDPOINTS PARA RECEPCIONISTAS
# ============================================================================

@router.get("/pendientes", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion")
async def listar_solicitudes_pendientes(
    current_user: Usuario = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[RECEPCIONISTA]** Listar solicitudes recién creadas (estado recibida)"""
    return service.listar_pendientes(skip, limit)


@router.put("/{id_solicitud}/derivar", response_model=SolicitudRetiroResponseDTO)
@require_permissions("recepcion")
async def derivar_solicitud(
    id_solicitud: int,
    derivar_dto: DerivarSolicitudDTO,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service)
) -> SolicitudRetiroResponseDTO:
    """**[RECEPCIONISTA]** Derivar solicitud a un regente (recibida → derivada)"""
    return service.derivar_solicitud(id_solicitud, derivar_dto)

# ============================================================================
# ENDPOINTS PARA REGENTES
# ============================================================================

@router.get("/derivadas-a-mi", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("regente", "recepcion")
async def listar_solicitudes_derivadas_a_mi(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[REGENTE/RECEPCIÓN]** Listar solicitudes derivadas"""
    return service.listar_derivadas(skip, limit)


# ============================================================================
# ENDPOINTS GENERALES (CONSULTA)
# ============================================================================

@router.get("/", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion", "regente", "admin")
async def listar_solicitudes(
    current_user: Usuario = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: SolicitudRetiroService = Depends(get_service)
) -> List[SolicitudRetiroResponseDTO]:
    """**[ADMIN/RECEPCIÓN/REGENTE]** Listar todas las solicitudes individuales"""
    return service.listar_solicitudes(skip, limit)


@router.get("/{id_solicitud}", response_model=SolicitudRetiroResponseDTO)
@require_permissions("recepcion", "regente", "admin")
async def obtener_solicitud(
    id_solicitud: int,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service)
) -> SolicitudRetiroResponseDTO:
    """**[RECEPCIÓN/REGENTE/DIRECTOR]** Obtener una solicitud específica por ID"""
    return service.obtener_solicitud(id_solicitud)


@router.get("/estudiante/{id_estudiante}", response_model=List[SolicitudRetiroResponseDTO])
@require_permissions("recepcion", "regente", "apoderado")
async def listar_solicitudes_por_estudiante(
    id_estudiante: int,
    current_user: Usuario = Depends(get_current_user),
    service: SolicitudRetiroService = Depends(get_service),
    db: Session = Depends(get_db)
) -> List[SolicitudRetiroResponseDTO]:
    """
    **[RECEPCIÓN/REGENTE/APODERADO]** Listar solicitudes de un estudiante específico
    
    - APODERADO: Solo puede ver estudiantes con los que tiene relación vigente
    - RECEPCIÓN/REGENTE: Pueden ver cualquier estudiante
    """
    from app.shared.permission_mapper import tiene_permiso
    from app.modules.retiros_tempranos.models import Apoderado, EstudianteApoderado
    
    # Si es apoderado, verificar relación
    if tiene_permiso(current_user, "apoderado"):
        # Query optimizado con ORM y EXISTS
        relacion_existe = db.query(
            db.query(EstudianteApoderado).join(Apoderado).filter(
                Apoderado.id_persona == current_user.id_persona,
                EstudianteApoderado.id_estudiante == id_estudiante
            ).exists()
        ).scalar()
        
        if not relacion_existe:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permiso para ver solicitudes del estudiante {id_estudiante}. Solo puede ver estudiantes bajo su tutela."
            )
    
    return service.listar_por_estudiante(id_estudiante)
