from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.modules.retiros_tempranos.models.AutorizacionesRetiro import AutorizacionRetiro
from app.modules.retiros_tempranos.repositories import IAutorizacionRetiroRepository, ISolicitudRetiroRepository
from app.modules.retiros_tempranos.dto import (
    AutorizacionRetiroCreateDTO,
    AutorizacionRetiroUpdateDTO,
    AutorizacionRetiroResponseDTO,
)
from app.shared.services.base_services import BaseService


class AutorizacionRetiroService(BaseService):
    def __init__(self, repository: IAutorizacionRetiroRepository, solicitud_repository: ISolicitudRetiroRepository = None):
        self.repository = repository
        self.solicitud_repository = solicitud_repository
    
    def _tiene_rol(self, usuario, nombre_rol: str) -> bool:
        """Verificar si un usuario tiene un rol específico"""
        if not usuario or not hasattr(usuario, 'roles'):
            return False
        return any(rol.nombre.lower() == nombre_rol.lower() for rol in usuario.roles)

    def create_autorizacion(
        self, 
        id_solicitud: int,
        autorizacion_dto: AutorizacionRetiroCreateDTO, 
        id_usuario_aprobador: int
    ) -> AutorizacionRetiroResponseDTO:
        """Crear una nueva autorización de retiro (aprobar/rechazar solicitud)"""
        
        # Validar que la solicitud existe y está en estado válido
        if not self.solicitud_repository:
            raise HTTPException(status_code=500, detail="Repositorio de solicitudes no disponible")
            
        solicitud = self.solicitud_repository.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
        
        # Validar que la solicitud esté derivada
        if solicitud.estado != 'derivada':
            raise HTTPException(
                status_code=400, 
                detail=f"La solicitud debe estar en estado 'derivada', actualmente está en '{solicitud.estado}'"
            )
        
        # Crear la autorización
        autorizacion = AutorizacionRetiro(
            id_usuario_aprobador=id_usuario_aprobador,
            decision=autorizacion_dto.decision,
            motivo_decision=autorizacion_dto.motivo_decision,
            fecha_decision=datetime.now(),
        )
        creada = self.repository.create(autorizacion)
        
        # Actualizar la solicitud con el id_autorizacion y cambiar el estado
        if creada:
            estado_nuevo = 'aprobada' if autorizacion_dto.decision == 'aprobada' else 'rechazada'
            self.solicitud_repository.update(
                id_solicitud,
                {
                    'id_autorizacion': creada.id_autorizacion,
                    'estado': estado_nuevo
                }
            )
        
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
        """Actualizar una autorización de retiro y actualizar estado de la solicitud si la decisión cambió"""
        existing = self.repository.get_by_id(autorizacion_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")

        # Obtener datos a actualizar
        update_data = autorizacion_dto.model_dump(exclude_unset=True)
        
        # Si se está cambiando la decisión, actualizar también el estado de la solicitud
        if 'decision' in update_data and update_data['decision'] != existing.decision:
            if self.solicitud_repository:
                # Obtener la solicitud vinculada por id_autorizacion
                solicitud = self.solicitud_repository.get_by_autorizacion(autorizacion_id)
                if solicitud:
                    # Determinar el nuevo estado según la decisión
                    nuevo_estado = 'aprobada' if update_data['decision'] == 'aprobada' else 'rechazada'
                    self.solicitud_repository.update(
                        solicitud.id_solicitud,
                        {'estado': nuevo_estado}
                    )
        
        updated = self.repository.update(autorizacion_id, update_data)
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la autorización de retiro")
        return AutorizacionRetiroResponseDTO.model_validate(updated)