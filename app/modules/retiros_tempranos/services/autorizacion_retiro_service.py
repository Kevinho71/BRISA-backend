from typing import List, Optional
from fastapi import HTTPException
from app.modules.retiros_tempranos.models.AutorizacionesRetiro import AutorizacionRetiro
from app.modules.retiros_tempranos.repositories import IAutorizacionRetiroRepository
from app.modules.retiros_tempranos.dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO,
)
from app.shared.services.base_services import BaseService


class AutorizacionRetiroService(BaseService):
    def __init__(self, repository: IAutorizacionRetiroRepository):
        self.repository = repository

    def create_autorizacion(self, autorizacion_dto: AutorizacionRetiroCreateDTO) -> AutorizacionRetiroResponseDTO:
        """Crear una nueva autorización de retiro"""
        autorizacion = AutorizacionRetiro(
            decidido_por=autorizacion_dto.decidido_por,
            decision=autorizacion_dto.decision,
            motivo_decision=autorizacion_dto.motivo_decision,
            decidido_en=autorizacion_dto.decidido_en,
        )
        creada = self.repository.create(autorizacion)
        return AutorizacionRetiroResponseDTO.model_validate(creada)

    def get_autorizacion(self, autorizacion_id: int) -> AutorizacionRetiroResponseDTO:
        """Obtener una autorización de retiro por ID"""
        autorizacion = self.repository.get_by_id(autorizacion_id)
        if not autorizacion:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
        return AutorizacionRetiroResponseDTO.model_validate(autorizacion)

    def get_all_autorizaciones(self, skip: int = 0, limit: int = 100) -> List[AutorizacionRetiroResponseDTO]:
        """Obtener todas las autorizaciones de retiro"""
        autorizaciones = self.repository.get_all(skip=skip, limit=limit)
        return [AutorizacionRetiroResponseDTO.model_validate(a) for a in autorizaciones]

    def update_autorizacion(self, autorizacion_id: int, autorizacion_dto: AutorizacionRetiroUpdateDTO) -> AutorizacionRetiroResponseDTO:
        """Actualizar una autorización de retiro"""
        existing = self.repository.get_by_id(autorizacion_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")

        updated = self.repository.update(autorizacion_id, autorizacion_dto.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la autorización de retiro")
        return AutorizacionRetiroResponseDTO.model_validate(updated)

    def delete_autorizacion(self, autorizacion_id: int) -> bool:
        """Eliminar una autorización de retiro"""
        existing = self.repository.get_by_id(autorizacion_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
        return self.repository.delete(autorizacion_id)