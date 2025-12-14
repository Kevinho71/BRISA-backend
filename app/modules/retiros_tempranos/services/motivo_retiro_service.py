from typing import List, Optional
from fastapi import HTTPException
from app.modules.retiros_tempranos.models.MotivoRetiro import MotivoRetiro
from app.modules.retiros_tempranos.repositories import IMotivoRetiroRepository
from app.modules.retiros_tempranos.dto import (
    MotivoRetiroCreateDTO,
    MotivoRetiroUpdateDTO,
    MotivoRetiroResponseDTO,
)
from app.shared.services.base_services import BaseService


class MotivoRetiroService(BaseService):
    def __init__(self, repository: IMotivoRetiroRepository):
        self.repository = repository

    def create_motivo(self, motivo_dto: MotivoRetiroCreateDTO) -> MotivoRetiroResponseDTO:
        """Crear un nuevo motivo de retiro"""
        motivo = MotivoRetiro(
            nombre=motivo_dto.nombre,
            severidad=motivo_dto.severidad,
            activo=motivo_dto.activo,
            descripcion=motivo_dto.descripcion,
        )
        creado = self.repository.create(motivo)
        return MotivoRetiroResponseDTO.model_validate(creado)

    def get_motivo(self, motivo_id: int) -> MotivoRetiroResponseDTO:
        """Obtener un motivo de retiro por ID"""
        motivo = self.repository.get_by_id(motivo_id)
        if not motivo:
            raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")
        return MotivoRetiroResponseDTO.model_validate(motivo)

    def get_all_motivos(self, skip: int = 0, limit: int = 100) -> List[MotivoRetiroResponseDTO]:
        """Obtener todos los motivos de retiro con paginación"""
        motivos = self.repository.get_all(skip=skip, limit=limit)
        return [MotivoRetiroResponseDTO.model_validate(m) for m in motivos]

    def get_motivos_activos(self) -> List[MotivoRetiroResponseDTO]:
        """Obtener solo los motivos activos"""
        motivos = self.repository.get_activos()
        return [MotivoRetiroResponseDTO.model_validate(m) for m in motivos]

    def get_motivos_by_severidad(self, severidad: str) -> List[MotivoRetiroResponseDTO]:
        """Obtener motivos por nivel de severidad"""
        if not severidad:
            raise HTTPException(status_code=400, detail="La severidad es requerida")
        motivos = self.repository.get_by_severidad(severidad)
        return [MotivoRetiroResponseDTO.model_validate(m) for m in motivos]

    def update_motivo(self, motivo_id: int, motivo_dto: MotivoRetiroUpdateDTO) -> MotivoRetiroResponseDTO:
        """Actualizar un motivo de retiro"""
        existing = self.repository.get_by_id(motivo_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")

        updated = self.repository.update(motivo_id, motivo_dto.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el motivo de retiro")
        return MotivoRetiroResponseDTO.model_validate(updated)

    def delete_motivo(self, motivo_id: int) -> bool:
        """Eliminar un motivo de retiro"""
        existing = self.repository.get_by_id(motivo_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Motivo de retiro no encontrado")
        return self.repository.delete(motivo_id)