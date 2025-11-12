from typing import List, Optional
from fastapi import HTTPException
from app.modules.retiros_tempranos.models.RegistroSalida import RegistroSalida
from app.modules.retiros_tempranos.repositories import IRegistroSalidaRepository, ISolicitudRetiroRepository
from app.modules.retiros_tempranos.dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO,
)
from app.shared.services.base_services import BaseService


class RegistroSalidaService(BaseService):
    def __init__(self, repository: IRegistroSalidaRepository, solicitud_repository: ISolicitudRetiroRepository = None):
        self.repository = repository
        self.solicitud_repository = solicitud_repository

    def create_registro(self, registro_dto: RegistroSalidaCreateDTO) -> RegistroSalidaResponseDTO:
        """Crear un nuevo registro de salida (solo para solicitudes aprobadas)"""
        
        # Obtener la solicitud y validar
        if not self.solicitud_repository:
            raise HTTPException(status_code=500, detail="Repositorio de solicitudes no configurado")
        
        solicitud = self.solicitud_repository.get_by_id(registro_dto.id_solicitud)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        
        # Validar que la solicitud esté aprobada
        if solicitud.estado != 'aprobada':
            raise HTTPException(
                status_code=400,
                detail=f"Solo se pueden registrar salidas para solicitudes aprobadas. Estado actual: '{solicitud.estado}'"
            )
        
        # Crear el registro con el id_estudiante de la solicitud
        registro = RegistroSalida(
            id_estudiante=solicitud.id_estudiante,  # Obtenido automáticamente de la solicitud
            id_solicitud=registro_dto.id_solicitud,
            fecha_hora_salida_real=registro_dto.fecha_hora_salida_real,
            fecha_hora_retorno_real=registro_dto.fecha_hora_retorno_real,
        )
        creado = self.repository.create(registro)
        return RegistroSalidaResponseDTO.model_validate(creado)

    def get_registro(self, registro_id: int) -> RegistroSalidaResponseDTO:
        """Obtener un registro de salida por ID"""
        registro = self.repository.get_by_id(registro_id)
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de salida no encontrado")
        return RegistroSalidaResponseDTO.model_validate(registro)

    def get_all_registros(self, skip: int = 0, limit: int = 100) -> List[RegistroSalidaResponseDTO]:
        """Obtener todos los registros de salida"""
        registros = self.repository.get_all(skip=skip, limit=limit)
        return [RegistroSalidaResponseDTO.model_validate(r) for r in registros]

    def get_registros_by_estudiante(self, estudiante_id: int) -> List[RegistroSalidaResponseDTO]:
        """Obtener todos los registros de salida de un estudiante"""
        registros = self.repository.get_by_estudiante(estudiante_id)
        return [RegistroSalidaResponseDTO.model_validate(r) for r in registros]

    def update_registro(self, registro_id: int, registro_dto: RegistroSalidaUpdateDTO) -> RegistroSalidaResponseDTO:
        """Actualizar un registro de salida"""
        existing = self.repository.get_by_id(registro_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Registro de salida no encontrado")

        updated = self.repository.update(registro_id, registro_dto.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el registro de salida")
        return RegistroSalidaResponseDTO.model_validate(updated)

    def delete_registro(self, registro_id: int) -> bool:
        """Eliminar un registro de salida"""
        existing = self.repository.get_by_id(registro_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Registro de salida no encontrado")
        return self.repository.delete(registro_id)