from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.AutorizacionesRetiro import AutorizacionRetiro


class IAutorizacionRetiroRepository(ABC):
    """Interfaz para el repositorio de AutorizacionRetiro"""
    
    @abstractmethod
    def create(self, autorizacion: AutorizacionRetiro) -> AutorizacionRetiro:
        """Crear una nueva autorización"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_autorizacion: int) -> Optional[AutorizacionRetiro]:
        """Obtener una autorización por su ID"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AutorizacionRetiro]:
        """Obtener todas las autorizaciones con paginación"""
        pass
    
    @abstractmethod
    def get_by_decision(self, decision: str) -> List[AutorizacionRetiro]:
        """Obtener autorizaciones por tipo de decisión"""
        pass
    
    @abstractmethod
    def update(self, id_autorizacion: int, autorizacion_data: dict) -> Optional[AutorizacionRetiro]:
        """Actualizar una autorización"""
        pass
    
    @abstractmethod
    def delete(self, id_autorizacion: int) -> bool:
        """Eliminar una autorización"""
        pass
