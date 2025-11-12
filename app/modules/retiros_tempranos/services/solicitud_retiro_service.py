from typing import List
from datetime import datetime
from fastapi import HTTPException
from app.modules.retiros_tempranos.models.SolicitudRetiro import SolicitudRetiro, EstadoSolicitudEnum
from app.modules.retiros_tempranos.repositories import ISolicitudRetiroRepository
from app.modules.retiros_tempranos.dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO,
)
from app.shared.services.base_services import BaseService

# IDs fijos de los actores del sistema
RECEPCIONISTA_ID = 1
REGENTE_ID = 2


class SolicitudRetiroService(BaseService):
    def __init__(self, repository: ISolicitudRetiroRepository):
        self.repository = repository

    def create_solicitud(self, solicitud_dto: SolicitudRetiroCreateDTO) -> SolicitudRetiroResponseDTO:
        """Crear solicitud - fecha_creacion, estado, recibido_por y fecha_recepcion automáticos"""
        now = datetime.now()
        solicitud = SolicitudRetiro(
            id_estudiante=solicitud_dto.id_estudiante,
            id_apoderado=solicitud_dto.id_apoderado,
            id_motivo=solicitud_dto.id_motivo,
            fecha_hora_salida=solicitud_dto.fecha_hora_salida,
            fecha_hora_retorno_previsto=solicitud_dto.fecha_hora_retorno_previsto,
            observacion=solicitud_dto.observacion,
            fecha_creacion=now,  # Automático
            estado=EstadoSolicitudEnum.recibida,  # Automático
            recibido_por=RECEPCIONISTA_ID,  # Automático (ID=1)
            fecha_recepcion=now  # Automático
        )
        creada = self.repository.create(solicitud)
        return SolicitudRetiroResponseDTO.model_validate(creada)

    def get_solicitud(self, solicitud_id: int) -> SolicitudRetiroResponseDTO:
        solicitud = self.repository.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail='Solicitud de retiro no encontrada')
        return SolicitudRetiroResponseDTO.model_validate(solicitud)

    def get_all_solicitudes(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroResponseDTO]:
        solicitudes = self.repository.get_all(skip=skip, limit=limit)
        return [SolicitudRetiroResponseDTO.model_validate(s) for s in solicitudes]

    def get_solicitudes_by_estudiante(self, estudiante_id: int) -> List[SolicitudRetiroResponseDTO]:
        solicitudes = self.repository.get_by_estudiante(estudiante_id)
        return [SolicitudRetiroResponseDTO.model_validate(s) for s in solicitudes]

    def get_solicitudes_by_estado(self, estado: EstadoSolicitudEnum) -> List[SolicitudRetiroResponseDTO]:
        solicitudes = self.repository.get_by_estado(estado.value)
        return [SolicitudRetiroResponseDTO.model_validate(s) for s in solicitudes]

    def derivar_solicitud(self, solicitud_id: int) -> SolicitudRetiroResponseDTO:
        solicitud = self.repository.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail='Solicitud no encontrada')
        if solicitud.estado != EstadoSolicitudEnum.recibida:
            raise HTTPException(status_code=400, detail=f'Solo se pueden derivar solicitudes en estado recibida. Estado actual: {solicitud.estado}')
        updated = self.repository.update(solicitud_id, {'estado': EstadoSolicitudEnum.derivada.value, 'derivado_a': REGENTE_ID, 'fecha_derivacion': datetime.now()})
        return SolicitudRetiroResponseDTO.model_validate(updated)

    def update_solicitud(self, solicitud_id: int, solicitud_dto: SolicitudRetiroUpdateDTO) -> SolicitudRetiroResponseDTO:
        existing = self.repository.get_by_id(solicitud_id)
        if not existing:
            raise HTTPException(status_code=404, detail='Solicitud de retiro no encontrada')
        updated = self.repository.update(solicitud_id, solicitud_dto.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=400, detail='No se pudo actualizar la solicitud de retiro')
        return SolicitudRetiroResponseDTO.model_validate(updated)

    def delete_solicitud(self, solicitud_id: int) -> bool:
        existing = self.repository.get_by_id(solicitud_id)
        if not existing:
            raise HTTPException(status_code=404, detail='Solicitud de retiro no encontrada')
        return self.repository.delete(solicitud_id)
