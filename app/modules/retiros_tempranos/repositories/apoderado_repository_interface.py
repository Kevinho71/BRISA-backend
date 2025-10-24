from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.Apoderado import Apoderado


class IApoderadoRepository(ABC):
    """Interfaz para el repositorio de Apoderado"""
    
    @abstractmethod
    def create(self, apoderado: Apoderado) -> Apoderado:
        """Crear un nuevo apoderado"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_apoderado: int) -> Optional[Apoderado]:
        """Obtener un apoderado por su ID"""
        pass
    
    @abstractmethod
    def get_by_estudiante(self, id_estudiante: int) -> List[Apoderado]:
        """Obtener todos los apoderados de un estudiante"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Apoderado]:
        """Obtener todos los apoderados con paginación"""
        pass
    
    @abstractmethod
    def update(self, id_apoderado: int, apoderado_data: dict) -> Optional[Apoderado]:
        """Actualizar un apoderado"""
        pass
    
    @abstractmethod
    def delete(self, id_apoderado: int) -> bool:
        """Eliminar un apoderado"""
        pass
