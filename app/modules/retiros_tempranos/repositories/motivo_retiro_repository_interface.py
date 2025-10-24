from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.MotivoRetiro import MotivoRetiro


class IMotivoRetiroRepository(ABC):
    """Interfaz para el repositorio de MotivoRetiro"""
    
    @abstractmethod
    def create(self, motivo: MotivoRetiro) -> MotivoRetiro:
        """Crear un nuevo motivo de retiro"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_motivo: int) -> Optional[MotivoRetiro]:
        """Obtener un motivo por su ID"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[MotivoRetiro]:
        """Obtener todos los motivos con paginación"""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[MotivoRetiro]:
        """Obtener solo los motivos activos"""
        pass
    
    @abstractmethod
    def get_by_severidad(self, severidad: str) -> List[MotivoRetiro]:
        """Obtener motivos por nivel de severidad"""
        pass
    
    @abstractmethod
    def update(self, id_motivo: int, motivo_data: dict) -> Optional[MotivoRetiro]:
        """Actualizar un motivo"""
        pass
    
    @abstractmethod
    def delete(self, id_motivo: int) -> bool:
        """Eliminar un motivo"""
        pass
