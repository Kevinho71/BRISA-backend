from typing import List, Optional
from app.modules.retiros_tempranos.repositories import IMotivoRetiroRepository
from app.modules.retiros_tempranos.dto import (
    MotivoRetiroCreateDTO,
    MotivoRetiroUpdateDTO,
    MotivoRetiroResponseDTO
)
from app.shared.services.base_services import BaseService
from fastapi import HTTPException


class MotivoRetiroService(BaseService):
    def __init__(self, repository: IMotivoRetiroRepository):
        self.repository = repository

    async def create_motivo(self, motivo_dto: MotivoRetiroCreateDTO) -> MotivoRetiroResponseDTO:
        """Crear un nuevo motivo de retiro"""
        motivo = await self.repository.create(motivo_dto.model_dump())
        return MotivoRetiroResponseDTO.model_validate(motivo)

    async def get_motivo(self, motivo_id: int) -> MotivoRetiroResponseDTO:
        """Obtener un motivo de retiro por ID"""
        motivo = await self.repository.get_by_id(motivo_id)
        if not motivo:
            raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")
        return MotivoRetiroResponseDTO.model_validate(motivo)

    async def get_all_motivos(self, skip: int = 0, limit: int = 100) -> List[MotivoRetiroResponseDTO]:
        """Obtener todos los motivos de retiro con paginación"""
        motivos = await self.repository.get_all(skip=skip, limit=limit)
        return [MotivoRetiroResponseDTO.model_validate(motivo) for motivo in motivos]
        
    async def get_motivos_activos(self) -> List[MotivoRetiroResponseDTO]:
        """Obtener solo los motivos activos"""
        motivos = await self.repository.get_activos()
        return [MotivoRetiroResponseDTO.model_validate(motivo) for motivo in motivos]
        
    async def get_motivos_by_severidad(self, severidad: str) -> List[MotivoRetiroResponseDTO]:
        """Obtener motivos por nivel de severidad"""
        if not severidad:
            raise HTTPException(status_code=400, detail="La severidad es requerida")
        motivos = await self.repository.get_by_severidad(severidad)
        return [MotivoRetiroResponseDTO.model_validate(motivo) for motivo in motivos]

    async def update_motivo(self, motivo_id: int, motivo_dto: MotivoRetiroUpdateDTO) -> MotivoRetiroResponseDTO:
        """Actualizar un motivo de retiro"""
        existing_motivo = await self.repository.get_by_id(motivo_id)
        if not existing_motivo:
            raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")
        
        updated_motivo = await self.repository.update(motivo_id, motivo_dto.model_dump(exclude_unset=True))
        return MotivoRetiroResponseDTO.model_validate(updated_motivo)

    async def delete_motivo(self, motivo_id: int) -> bool:
        """Eliminar un motivo de retiro"""
        existing_motivo = await self.repository.get_by_id(motivo_id)
        if not existing_motivo:
            raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")
        
        return await self.repository.delete(motivo_id)