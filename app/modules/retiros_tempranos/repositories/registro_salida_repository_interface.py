from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from app.modules.retiros_tempranos.models.RegistroSalida import RegistroSalida


class IRegistroSalidaRepository(ABC):
    """Interfaz para el repositorio de RegistroSalida"""
    
    @abstractmethod
    def create(self, registro: RegistroSalida) -> RegistroSalida:
        """Crear un nuevo registro de salida"""
        pass
    
    @abstractmethod
    def get_by_id(self, id_registro: int) -> Optional[RegistroSalida]:
        """Obtener un registro por su ID"""
        pass
    
    @abstractmethod
    def get_by_estudiante(self, id_estudiante: int) -> List[RegistroSalida]:
        """Obtener todos los registros de un estudiante"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[RegistroSalida]:
        """Obtener todos los registros con paginación"""
        pass
    
    @abstractmethod
    def get_sin_retorno(self) -> List[RegistroSalida]:
        """Obtener registros de salidas sin retorno"""
        pass
    
    @abstractmethod
    def get_by_fecha_rango(self, fecha_inicio: date, fecha_fin: date) -> List[RegistroSalida]:
        """Obtener registros en un rango de fechas"""
        pass
    
    @abstractmethod
    def update(self, id_registro: int, registro_data: dict) -> Optional[RegistroSalida]:
        """Actualizar un registro"""
        pass
    
    @abstractmethod
    def delete(self, id_registro: int) -> bool:
        """Eliminar un registro"""
        pass
