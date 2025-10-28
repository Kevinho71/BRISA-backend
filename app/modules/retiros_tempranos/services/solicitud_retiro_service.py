from typing import List, Optional
from app.modules.retiros_tempranos.repositories import ISolicitudRetiroRepository
from app.modules.retiros_tempranos.dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO
)
from app.shared.services.base_services import BaseService
from fastapi import HTTPException


class SolicitudRetiroService(BaseService):
    def __init__(self, repository: ISolicitudRetiroRepository):
        self.repository = repository

    async def create_solicitud(self, solicitud_dto: SolicitudRetiroCreateDTO) -> SolicitudRetiroResponseDTO:
        """Crear una nueva solicitud de retiro"""
        solicitud = await self.repository.create(solicitud_dto.model_dump())
        return SolicitudRetiroResponseDTO.model_validate(solicitud)

    async def get_solicitud(self, solicitud_id: int) -> SolicitudRetiroResponseDTO:
        """Obtener una solicitud de retiro por ID"""
        solicitud = await self.repository.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        return SolicitudRetiroResponseDTO.model_validate(solicitud)

    async def get_all_solicitudes(self) -> List[SolicitudRetiroResponseDTO]:
        """Obtener todas las solicitudes de retiro"""
        solicitudes = await self.repository.get_all()
        return [SolicitudRetiroResponseDTO.model_validate(solicitud) for solicitud in solicitudes]

    async def get_solicitudes_by_estudiante(self, estudiante_id: int) -> List[SolicitudRetiroResponseDTO]:
        """Obtener todas las solicitudes de retiro de un estudiante"""
        solicitudes = await self.repository.get_by_estudiante(estudiante_id)
        return [SolicitudRetiroResponseDTO.model_validate(solicitud) for solicitud in solicitudes]

    async def get_solicitudes_by_apoderado(self, apoderado_id: int) -> List[SolicitudRetiroResponseDTO]:
        """Obtener todas las solicitudes de retiro de un apoderado"""
        solicitudes = await self.repository.get_by_apoderado(apoderado_id)
        return [SolicitudRetiroResponseDTO.model_validate(solicitud) for solicitud in solicitudes]

    async def update_solicitud(self, solicitud_id: int, solicitud_dto: SolicitudRetiroUpdateDTO) -> SolicitudRetiroResponseDTO:
        """Actualizar una solicitud de retiro"""
        existing_solicitud = await self.repository.get_by_id(solicitud_id)
        if not existing_solicitud:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        
        updated_solicitud = await self.repository.update(solicitud_id, solicitud_dto.model_dump(exclude_unset=True))
        return SolicitudRetiroResponseDTO.model_validate(updated_solicitud)

    async def delete_solicitud(self, solicitud_id: int) -> bool:
        """Eliminar una solicitud de retiro"""
        existing_solicitud = await self.repository.get_by_id(solicitud_id)
        if not existing_solicitud:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        
        return await self.repository.delete(solicitud_id)