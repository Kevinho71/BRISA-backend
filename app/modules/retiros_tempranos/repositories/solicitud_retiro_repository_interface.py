from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from app.modules.retiros_tempranos.models.SolicitudRetiro import SolicitudRetiro


class ISolicitudRetiroRepository(ABC):
    """Interfaz para el repositorio de SolicitudRetiro"""
    
    @abstractmethod
    def create(self, solicitud: SolicitudRetiro) -> SolicitudRetiro:
        """Crear una nueva solicitud de retiro"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_solicitud: int) -> Optional[SolicitudRetiro]:
        """Obtener una solicitud por su ID"""
        pass
    
    @abstractmethod
    def get_by_estudiante(self, id_estudiante: int) -> List[SolicitudRetiro]:
        """Obtener todas las solicitudes de un estudiante"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiro]:
        """Obtener todas las solicitudes con paginación"""
        pass
    
    @abstractmethod
    def get_pendientes(self) -> List[SolicitudRetiro]:
        """Obtener solicitudes pendientes de autorización"""
        pass
    
    @abstractmethod
    def get_by_motivo(self, id_motivo: int) -> List[SolicitudRetiro]:
        """Obtener solicitudes por motivo"""
        pass
    
    @abstractmethod
    def get_by_fecha_rango(self, fecha_inicio: date, fecha_fin: date) -> List[SolicitudRetiro]:
        """Obtener solicitudes en un rango de fechas"""
        pass
    
    @abstractmethod
    def update(self, id_solicitud: int, solicitud_data: dict) -> Optional[SolicitudRetiro]:
        """Actualizar una solicitud"""
        pass
    
    @abstractmethod
    def delete(self, id_solicitud: int) -> bool:
        """Eliminar una solicitud"""
        pass
