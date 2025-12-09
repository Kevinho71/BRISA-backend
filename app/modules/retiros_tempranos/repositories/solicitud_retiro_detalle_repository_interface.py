from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.SoliticitudRetiroDetalle import SolicitudRetiroDetalle


class ISolicitudRetiroDetalleRepository(ABC):
    """Interfaz para el repositorio de SolicitudRetiroDetalle"""
    
    @abstractmethod
    def create(self, detalle: SolicitudRetiroDetalle) -> SolicitudRetiroDetalle:
        """Crear un nuevo detalle de solicitud"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_detalle: int) -> Optional[SolicitudRetiroDetalle]:
        """Obtener un detalle por su ID"""
        pass
    
    @abstractmethod
    def get_by_solicitud(self, id_solicitud: int) -> List[SolicitudRetiroDetalle]:
        """Obtener todos los detalles de una solicitud"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroDetalle]:
        """Obtener todos los detalles con paginación"""
        pass
    
    @abstractmethod
    def update(self, id_detalle: int, detalle_data: dict) -> Optional[SolicitudRetiroDetalle]:
        """Actualizar un detalle"""
        pass
    
    @abstractmethod
    def delete(self, id_detalle: int) -> bool:
        """Eliminar un detalle"""
        pass
    
    @abstractmethod
    def delete_by_solicitud(self, id_solicitud: int) -> bool:
        """Eliminar todos los detalles de una solicitud"""
        pass
