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


class SolicitudRetiroService(BaseService):
    def __init__(self, repository: ISolicitudRetiroRepository):
        self.repository = repository
    
    def _tiene_rol(self, usuario, nombre_rol: str) -> bool:
        """Verificar si un usuario tiene un rol específico"""
        if not usuario or not hasattr(usuario, 'roles'):
            return False
        return any(rol.nombre.lower() == nombre_rol.lower() for rol in usuario.roles)

    def create_solicitud(self, solicitud_dto: SolicitudRetiroCreateDTO, usuario_actual=None) -> SolicitudRetiroResponseDTO:
        """Crear solicitud - Requiere usuario con rol 'Recepcion'"""
        # Validar rol si se proporciona usuario
        if usuario_actual and not self._tiene_rol(usuario_actual, 'Recepcion'):
            raise HTTPException(status_code=403, detail='Solo usuarios con rol Recepcion pueden recibir solicitudes')
        
        now = datetime.now()
        solicitud = SolicitudRetiro(
            id_estudiante=solicitud_dto.id_estudiante,
            id_apoderado=solicitud_dto.id_apoderado,
            id_motivo=solicitud_dto.id_motivo,
            fecha_hora_salida=solicitud_dto.fecha_hora_salida,
            fecha_hora_retorno_previsto=solicitud_dto.fecha_hora_retorno_previsto,
            observacion=solicitud_dto.observacion,
            fecha_creacion=now,
            estado=EstadoSolicitudEnum.recibida,
            id_recepcionista=usuario_actual.id_usuario if usuario_actual else None,
            fecha_recepcion=now if usuario_actual else None
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

    def derivar_solicitud(self, solicitud_id: int, id_regente: int, usuario_actual=None) -> SolicitudRetiroResponseDTO:
        """Derivar solicitud a un regente - Requiere usuario con rol 'Recepcion'"""
        # Validar rol si se proporciona usuario
        if usuario_actual and not self._tiene_rol(usuario_actual, 'Recepcion'):
            raise HTTPException(status_code=403, detail='Solo usuarios con rol Recepcion pueden derivar solicitudes')
        
        solicitud = self.repository.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail='Solicitud no encontrada')
        if solicitud.estado != EstadoSolicitudEnum.recibida:
            raise HTTPException(status_code=400, detail=f'Solo se pueden derivar solicitudes en estado recibida. Estado actual: {solicitud.estado}')
        
        # TODO: Validar que id_regente existe y tiene rol 'Regente'
        # Requiere inyección de usuario_repository
        
        updated = self.repository.update(solicitud_id, {
            'estado': EstadoSolicitudEnum.derivada.value,
            'id_regente': id_regente,
            'fecha_derivacion': datetime.now()
        })
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
