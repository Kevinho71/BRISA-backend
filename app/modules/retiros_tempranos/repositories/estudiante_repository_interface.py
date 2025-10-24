from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.Estudiante import Estudiante


class IEstudianteRepository(ABC):
    """Interfaz para el repositorio de Estudiante"""
    
    @abstractmethod
    def create(self, estudiante: Estudiante) -> Estudiante:
        """Crear un nuevo estudiante"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_estudiante: int) -> Optional[Estudiante]:
        """Obtener un estudiante por su ID"""
        pass
    
    @abstractmethod
    def get_by_ci(self, ci: str) -> Optional[Estudiante]:
        """Obtener un estudiante por su cédula de identidad"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        """Obtener todos los estudiantes con paginación"""
        pass
    
    @abstractmethod
    def update(self, id_estudiante: int, estudiante_data: dict) -> Optional[Estudiante]:
        """Actualizar un estudiante"""
        pass
    
    @abstractmethod
    def delete(self, id_estudiante: int) -> bool:
        """Eliminar un estudiante"""
        pass
    
    @abstractmethod
    def exists_by_ci(self, ci: str) -> bool:
        """Verificar si existe un estudiante con la cédula dada"""
        pass
