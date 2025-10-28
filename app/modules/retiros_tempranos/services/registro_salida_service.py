from typing import List, Optional
from app.modules.retiros_tempranos.repositories import IRegistroSalidaRepository
from app.modules.retiros_tempranos.dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)
from app.shared.services.base_services import BaseService
from fastapi import HTTPException


class RegistroSalidaService(BaseService):
    def __init__(self, repository: IRegistroSalidaRepository):
        self.repository = repository

    async def create_registro(self, registro_dto: RegistroSalidaCreateDTO) -> RegistroSalidaResponseDTO:
        """Crear un nuevo registro de salida"""
        registro = await self.repository.create(registro_dto.model_dump())
        return RegistroSalidaResponseDTO.model_validate(registro)

    async def get_registro(self, registro_id: int) -> RegistroSalidaResponseDTO:
        """Obtener un registro de salida por ID"""
        registro = await self.repository.get_by_id(registro_id)
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de salida no encontrado")
        return RegistroSalidaResponseDTO.model_validate(registro)

    async def get_all_registros(self) -> List[RegistroSalidaResponseDTO]:
        """Obtener todos los registros de salida"""
        registros = await self.repository.get_all()
        return [RegistroSalidaResponseDTO.model_validate(registro) for registro in registros]

    async def get_registros_by_estudiante(self, estudiante_id: int) -> List[RegistroSalidaResponseDTO]:
        """Obtener todos los registros de salida de un estudiante"""
        registros = await self.repository.get_by_estudiante(estudiante_id)
        return [RegistroSalidaResponseDTO.model_validate(registro) for registro in registros]

    async def update_registro(self, registro_id: int, registro_dto: RegistroSalidaUpdateDTO) -> RegistroSalidaResponseDTO:
        """Actualizar un registro de salida"""
        existing_registro = await self.repository.get_by_id(registro_id)
        if not existing_registro:
            raise HTTPException(status_code=404, detail="Registro de salida no encontrado")
        
        updated_registro = await self.repository.update(registro_id, registro_dto.model_dump(exclude_unset=True))
        return RegistroSalidaResponseDTO.model_validate(updated_registro)

    async def delete_registro(self, registro_id: int) -> bool:
        """Eliminar un registro de salida"""
        existing_registro = await self.repository.get_by_id(registro_id)
        if not existing_registro:
            raise HTTPException(status_code=404, detail="Registro de salida no encontrado")
        
        return await self.repository.delete(registro_id)