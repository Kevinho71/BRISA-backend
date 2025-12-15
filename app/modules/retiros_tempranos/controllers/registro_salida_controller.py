from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.registro_salida_service import RegistroSalidaService
from app.modules.retiros_tempranos.dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaMasivoCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)
from app.core.database import get_db
from app.shared.decorators.auth_decorators import require_permissions

router = APIRouter(prefix="/api/retiros-tempranos/registros-salida", tags=["Registros de Salida"])


def get_service(db: Session = Depends(get_db)) -> RegistroSalidaService:
    """Inyección de dependencia del servicio"""
    return RegistroSalidaService(db)


# ============================================================================
# ENDPOINTS PARA CREAR REGISTROS DE SALIDA
# ============================================================================

@router.post("/individual", response_model=RegistroSalidaResponseDTO, status_code=status.HTTP_201_CREATED)
@require_permissions("recepcion")
async def crear_registro_individual(
    registro_dto: RegistroSalidaCreateDTO,
    service: RegistroSalidaService = Depends(get_service)
) -> RegistroSalidaResponseDTO:
    """
    **[RECEPCIONISTA]** Crear un registro de salida individual
    
    - Requiere solicitud aprobada
    - Registra la hora de salida del estudiante
    - Un registro por solicitud individual
    """
    return service.crear_registro_individual(registro_dto)


@router.post("/masivo", response_model=List[RegistroSalidaResponseDTO], status_code=status.HTTP_201_CREATED)
@require_permissions("recepcion")
async def crear_registros_masivos(
    registro_dto: RegistroSalidaMasivoCreateDTO,
    service: RegistroSalidaService = Depends(get_service)
) -> List[RegistroSalidaResponseDTO]:
    """
    **[RECEPCIONISTA]** Crear registros de salida masivos
    
    - Requiere solicitud masiva aprobada
    - Crea un registro para cada estudiante de la solicitud
    - Todos con la misma hora de salida
    """
    return service.crear_registros_masivos(registro_dto)


# ============================================================================
# ENDPOINTS PARA REGISTRAR RETORNOS
# ============================================================================

@router.put("/{id_registro}/retorno", response_model=RegistroSalidaResponseDTO)
@require_permissions("recepcion")
async def registrar_retorno(
    id_registro: int,
    retorno_dto: RegistroSalidaUpdateDTO,
    service: RegistroSalidaService = Depends(get_service)
) -> RegistroSalidaResponseDTO:
    """
    **[RECEPCIONISTA]** Registrar el retorno de un estudiante
    
    - Marca la hora de retorno del estudiante
    - Solo se puede registrar una vez
    """
    return service.registrar_retorno(id_registro, retorno_dto)


# ============================================================================
# ENDPOINTS DE CONSULTA
# ============================================================================

@router.get("/", response_model=List[RegistroSalidaResponseDTO])
@require_permissions("recepcion", "regente")
async def listar_registros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: RegistroSalidaService = Depends(get_service)
) -> List[RegistroSalidaResponseDTO]:
    """**[RECEPCIÓN/REGENTE]** Listar todos los registros de salida"""
    return service.listar_registros(skip, limit)


@router.get("/{id_registro}", response_model=RegistroSalidaResponseDTO)
@require_permissions("recepcion", "regente")
async def obtener_registro(
    id_registro: int,
    service: RegistroSalidaService = Depends(get_service)
) -> RegistroSalidaResponseDTO:
    """**[RECEPCIÓN/REGENTE]** Obtener un registro de salida por ID"""
    return service.obtener_registro(id_registro)


@router.get("/estudiante/{id_estudiante}", response_model=List[RegistroSalidaResponseDTO])
@require_permissions("recepcion", "regente")
async def listar_registros_por_estudiante(
    id_estudiante: int,
    service: RegistroSalidaService = Depends(get_service)
) -> List[RegistroSalidaResponseDTO]:
    """**[RECEPCIÓN/REGENTE]** Listar registros de salida de un estudiante específico"""
    return service.listar_por_estudiante(id_estudiante)


@router.get("/solicitud/{id_solicitud}", response_model=List[RegistroSalidaResponseDTO])
@require_permissions("recepcion", "regente")
async def listar_registros_por_solicitud(
    id_solicitud: int,
    service: RegistroSalidaService = Depends(get_service)
) -> List[RegistroSalidaResponseDTO]:
    """**[RECEPCIÓN/REGENTE]** Listar registros de una solicitud individual específica"""
    return service.listar_por_solicitud(id_solicitud)


@router.get("/solicitud-masiva/{id_solicitud_masiva}", response_model=List[RegistroSalidaResponseDTO])
@require_permissions("recepcion", "regente")
async def listar_registros_por_solicitud_masiva(
    id_solicitud_masiva: int,
    service: RegistroSalidaService = Depends(get_service)
) -> List[RegistroSalidaResponseDTO]:
    """**[RECEPCIÓN/REGENTE]** Listar registros de una solicitud masiva específica"""
    return service.listar_por_solicitud_masiva(id_solicitud_masiva)


# ============================================================================
# ENDPOINTS DE ADMINISTRACIÓN
# ============================================================================

@router.delete("/{id_registro}")
@require_permissions("recepcion")
async def eliminar_registro(
    id_registro: int,
    service: RegistroSalidaService = Depends(get_service)
) -> dict:
    """**[RECEPCIÓN]** Eliminar un registro de salida"""
    eliminado = service.eliminar_registro(id_registro)
    
    if eliminado:
        return {"message": "Registro eliminado exitosamente"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")

