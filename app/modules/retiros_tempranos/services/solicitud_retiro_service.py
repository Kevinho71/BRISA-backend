from typing import List, Optional
from fastapi import HTTPException
from app.modules.retiros_tempranos.models.SolicitudRetiro import SolicitudRetiro
from app.modules.retiros_tempranos.repositories import ISolicitudRetiroRepository
from app.modules.retiros_tempranos.dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO,
)
from app.shared.services.base_services import BaseService


class SolicitudRetiroService(BaseService):
    def __init__(self, repository: ISolicitudRetiroRepository):
        self.repository = repository

    def create_solicitud(self, solicitud_dto: SolicitudRetiroCreateDTO) -> SolicitudRetiroResponseDTO:
        """Crear una nueva solicitud de retiro"""
        solicitud = SolicitudRetiro(
            id_estudiante=solicitud_dto.id_estudiante,
            id_apoderado=solicitud_dto.id_apoderado,
            id_motivo=solicitud_dto.id_motivo,
            id_autorizacion=solicitud_dto.id_autorizacion,
            fecha_hora_salida=solicitud_dto.fecha_hora_salida,
            fecha_hora_retorno=solicitud_dto.fecha_hora_retorno,
            observacion=solicitud_dto.observacion,
            foto_retirante_url=solicitud_dto.foto_retirante_url,
            id_registro_salida=solicitud_dto.id_registro_salida,
        )
        creada = self.repository.create(solicitud)
        return SolicitudRetiroResponseDTO.model_validate(creada)

    def get_solicitud(self, solicitud_id: int) -> SolicitudRetiroResponseDTO:
        """Obtener una solicitud de retiro por ID"""
        solicitud = self.repository.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        return SolicitudRetiroResponseDTO.model_validate(solicitud)

    def get_all_solicitudes(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroResponseDTO]:
        """Obtener todas las solicitudes de retiro"""
        solicitudes = self.repository.get_all(skip=skip, limit=limit)
        return [SolicitudRetiroResponseDTO.model_validate(s) for s in solicitudes]

    def get_solicitudes_by_estudiante(self, estudiante_id: int) -> List[SolicitudRetiroResponseDTO]:
        """Obtener todas las solicitudes de retiro de un estudiante"""
        solicitudes = self.repository.get_by_estudiante(estudiante_id)
        return [SolicitudRetiroResponseDTO.model_validate(s) for s in solicitudes]

    def get_solicitudes_by_apoderado(self, apoderado_id: int) -> List[SolicitudRetiroResponseDTO]:
        """Obtener todas las solicitudes de retiro de un apoderado"""
        # Nota: La interfaz de repositorio no define get_by_apoderado; si existe en la implementación, úsalo.
        # Si no, esto debería implementarse en el repositorio.
        try:
            solicitudes = self.repository.get_by_apoderado(apoderado_id)  # type: ignore[attr-defined]
        except AttributeError:
            raise HTTPException(status_code=501, detail="Filtro por apoderado no implementado en el repositorio")
        return [SolicitudRetiroResponseDTO.model_validate(s) for s in solicitudes]

    def update_solicitud(self, solicitud_id: int, solicitud_dto: SolicitudRetiroUpdateDTO) -> SolicitudRetiroResponseDTO:
        """Actualizar una solicitud de retiro"""
        existing = self.repository.get_by_id(solicitud_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")

        updated = self.repository.update(solicitud_id, solicitud_dto.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la solicitud de retiro")
        return SolicitudRetiroResponseDTO.model_validate(updated)

    def delete_solicitud(self, solicitud_id: int) -> bool:
        """Eliminar una solicitud de retiro"""
        existing = self.repository.get_by_id(solicitud_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        return self.repository.delete(solicitud_id)