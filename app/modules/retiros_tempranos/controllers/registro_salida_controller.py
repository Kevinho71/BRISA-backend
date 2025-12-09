from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.services.registro_salida_service import RegistroSalidaService
from app.modules.retiros_tempranos.dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)
from app.core.database import get_db
from app.modules.retiros_tempranos.repositories import RegistroSalidaRepository, SolicitudRetiroRepository

router = APIRouter(prefix="/api/registros-salida", tags=["registros-salida"])


def get_registro_salida_service(db: Session = Depends(get_db)) -> RegistroSalidaService:
    repo = RegistroSalidaRepository(db)
    solicitud_repo = SolicitudRetiroRepository(db)
    return RegistroSalidaService(repo, solicitud_repo)


@router.post("/", response_model=RegistroSalidaResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_registro(
    registro_dto: RegistroSalidaCreateDTO,
    service: RegistroSalidaService = Depends(get_registro_salida_service)
) -> RegistroSalidaResponseDTO:
    """Crear un nuevo registro de salida"""
    return service.create_registro(registro_dto)


@router.get("/{registro_id}", response_model=RegistroSalidaResponseDTO)
async def get_registro(
    registro_id: int,
    service: RegistroSalidaService = Depends(get_registro_salida_service)
) -> RegistroSalidaResponseDTO:
    """Obtener un registro de salida por ID"""
    return service.get_registro(registro_id)


@router.get("/", response_model=List[RegistroSalidaResponseDTO])
async def get_all_registros(
    service: RegistroSalidaService = Depends(get_registro_salida_service)
) -> List[RegistroSalidaResponseDTO]:
    """Obtener todos los registros de salida"""
    return service.get_all_registros()


@router.get("/estudiante/{estudiante_id}", response_model=List[RegistroSalidaResponseDTO])
async def get_registros_by_estudiante(
    estudiante_id: int,
    service: RegistroSalidaService = Depends(get_registro_salida_service)
) -> List[RegistroSalidaResponseDTO]:
    """Obtener todos los registros de salida de un estudiante"""
    return service.get_registros_by_estudiante(estudiante_id)


@router.put("/{registro_id}", response_model=RegistroSalidaResponseDTO)
async def update_registro(
    registro_id: int,
    registro_dto: RegistroSalidaUpdateDTO,
    service: RegistroSalidaService = Depends(get_registro_salida_service)
) -> RegistroSalidaResponseDTO:
    """Actualizar un registro de salida"""
    return service.update_registro(registro_id, registro_dto)


@router.delete("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registro(
    registro_id: int,
    service: RegistroSalidaService = Depends(get_registro_salida_service)
):
    """Eliminar un registro de salida"""
    if not service.delete_registro(registro_id):
        raise HTTPException(status_code=404, detail="Registro de salida no encontrado")
