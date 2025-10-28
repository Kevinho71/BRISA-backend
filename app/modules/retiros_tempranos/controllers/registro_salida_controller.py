from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.retiros_tempranos.services.registro_salida_service import RegistroSalidaService
from app.modules.retiros_tempranos.dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)

router = APIRouter(prefix="/api/registros-salida", tags=["registros-salida"])


@router.post("/", response_model=RegistroSalidaResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_registro(
    registro_dto: RegistroSalidaCreateDTO,
    service: RegistroSalidaService = Depends()
) -> RegistroSalidaResponseDTO:
    """Crear un nuevo registro de salida"""
    return await service.create_registro(registro_dto)


@router.get("/{registro_id}", response_model=RegistroSalidaResponseDTO)
async def get_registro(
    registro_id: int,
    service: RegistroSalidaService = Depends()
) -> RegistroSalidaResponseDTO:
    """Obtener un registro de salida por ID"""
    return await service.get_registro(registro_id)


@router.get("/", response_model=List[RegistroSalidaResponseDTO])
async def get_all_registros(
    service: RegistroSalidaService = Depends()
) -> List[RegistroSalidaResponseDTO]:
    """Obtener todos los registros de salida"""
    return await service.get_all_registros()


@router.get("/estudiante/{estudiante_id}", response_model=List[RegistroSalidaResponseDTO])
async def get_registros_by_estudiante(
    estudiante_id: int,
    service: RegistroSalidaService = Depends()
) -> List[RegistroSalidaResponseDTO]:
    """Obtener todos los registros de salida de un estudiante"""
    return await service.get_registros_by_estudiante(estudiante_id)


@router.put("/{registro_id}", response_model=RegistroSalidaResponseDTO)
async def update_registro(
    registro_id: int,
    registro_dto: RegistroSalidaUpdateDTO,
    service: RegistroSalidaService = Depends()
) -> RegistroSalidaResponseDTO:
    """Actualizar un registro de salida"""
    return await service.update_registro(registro_id, registro_dto)


@router.delete("/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registro(
    registro_id: int,
    service: RegistroSalidaService = Depends()
):
    """Eliminar un registro de salida"""
    if not await service.delete_registro(registro_id):
        raise HTTPException(status_code=404, detail="Registro de salida no encontrado")