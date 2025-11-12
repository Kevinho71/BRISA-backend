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

# ID fijo del regente (quien siempre toma las decisiones)
REGENTE_ID = 2


class AutorizacionRetiroService(BaseService):
    def __init__(self, repository: IAutorizacionRetiroRepository, solicitud_repository: ISolicitudRetiroRepository = None):
        self.repository = repository
        self.solicitud_repository = solicitud_repository

    def create_autorizacion(self, autorizacion_dto: AutorizacionRetiroCreateDTO) -> AutorizacionRetiroResponseDTO:
        """Crear una nueva autorización de retiro y actualizar la solicitud (decidido_por y fecha_decision automáticos)"""
        
        # Validar que la solicitud existe y está en estado válido
        if self.solicitud_repository:
            solicitud = self.solicitud_repository.get_by_id(autorizacion_dto.id_solicitud)
            if not solicitud:
                raise HTTPException(status_code=404, detail="Solicitud de retiro no encontrada")
            
            # Validar que la solicitud esté derivada
            if solicitud.estado != 'derivada':
                raise HTTPException(
                    status_code=400, 
                    detail=f"La solicitud debe estar en estado 'derivada', actualmente está en '{solicitud.estado}'"
                )
        
        # Crear la autorización con valores automáticos
        autorizacion = AutorizacionRetiro(
            decidido_por=REGENTE_ID,  # Regente fijo (ID=2)
            decision=autorizacion_dto.decision,
            motivo_decision=autorizacion_dto.motivo_decision,
            fecha_decision=datetime.now(),  # Fecha automática
        )
        creada = self.repository.create(autorizacion)
        
        # Actualizar la solicitud con el id_autorizacion y cambiar el estado
        if self.solicitud_repository and creada:
            estado_nuevo = 'aprobada' if autorizacion_dto.decision == 'aprobado' else 'rechazada'
            self.solicitud_repository.update(
                autorizacion_dto.id_solicitud,
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
                    nuevo_estado = 'aprobada' if update_data['decision'] == 'aprobado' else 'rechazada'
                    self.solicitud_repository.update(
                        solicitud.id_solicitud,
                        {'estado': nuevo_estado}
                    )
        
        updated = self.repository.update(autorizacion_id, update_data)
        if not updated:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la autorización de retiro")
        return AutorizacionRetiroResponseDTO.model_validate(updated)

    def delete_autorizacion(self, autorizacion_id: int) -> bool:
        """Eliminar una autorización de retiro y regresar la solicitud a estado 'derivada'"""
        existing = self.repository.get_by_id(autorizacion_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Autorización de retiro no encontrada")
        
        # Antes de eliminar, actualizar la solicitud vinculada a estado 'derivada'
        if self.solicitud_repository:
            solicitud = self.solicitud_repository.get_by_autorizacion(autorizacion_id)
            if solicitud:
                self.solicitud_repository.update(
                    solicitud.id_solicitud,
                    {
                        'estado': 'derivada',
                        'id_autorizacion': None  # Limpiar la referencia a la autorización
                    }
                )
        
        return self.repository.delete(autorizacion_id)