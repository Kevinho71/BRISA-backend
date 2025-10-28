from typing import List, Optional
from app.modules.retiros_tempranos.repositories import IAutorizacionRetiroRepository
from app.modules.retiros_tempranos.dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO
)
from app.shared.services.base_services import BaseService
from fastapi import HTTPException


class AutorizacionRetiroService(BaseService):
    def __init__(self, repository: IAutorizacionRetiroRepository):
        self.repository = repository

    async def create_autorizacion(self, autorizacion_dto: AutorizacionRetiroCreateDTO) -> AutorizacionRetiroResponseDTO:
        """Crear una nueva autorización de retiro"""
        autorizacion = await self.repository.create(autorizacion_dto.model_dump())
        return AutorizacionRetiroResponseDTO.model_validate(autorizacion)

    async def get_autorizacion(self, autorizacion_id: int) -> AutorizacionRetiroResponseDTO:
        """Obtener una autorización de retiro por ID"""
        autorizacion = await self.repository.get_by_id(autorizacion_id)
        if not autorizacion:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
        return AutorizacionRetiroResponseDTO.model_validate(autorizacion)

    async def get_all_autorizaciones(self) -> List[AutorizacionRetiroResponseDTO]:
        """Obtener todas las autorizaciones de retiro"""
        autorizaciones = await self.repository.get_all()
        return [AutorizacionRetiroResponseDTO.model_validate(autorizacion) for autorizacion in autorizaciones]

    async def update_autorizacion(self, autorizacion_id: int, autorizacion_dto: AutorizacionRetiroUpdateDTO) -> AutorizacionRetiroResponseDTO:
        """Actualizar una autorización de retiro"""
        existing_autorizacion = await self.repository.get_by_id(autorizacion_id)
        if not existing_autorizacion:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
        
        updated_autorizacion = await self.repository.update(autorizacion_id, autorizacion_dto.model_dump(exclude_unset=True))
        return AutorizacionRetiroResponseDTO.model_validate(updated_autorizacion)

    async def delete_autorizacion(self, autorizacion_id: int) -> bool:
        """Eliminar una autorización de retiro"""
        existing_autorizacion = await self.repository.get_by_id(autorizacion_id)
        if not existing_autorizacion:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
        
        return await self.repository.delete(autorizacion_id)