from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.EstudianteApoderado import EstudianteApoderado


class IEstudianteApoderadoRepository(ABC):
    """Interfaz para el repositorio de EstudianteApoderado"""
    
    @abstractmethod
    def create(self, relacion: EstudianteApoderado) -> EstudianteApoderado:
        """Crear una nueva relación estudiante-apoderado"""
        pass
    
    @abstractmethod
    def get_by_ids(self, id_estudiante: int, id_apoderado: int) -> Optional[EstudianteApoderado]:
        """Obtener una relación específica por IDs"""
        pass
    
    @abstractmethod
    def get_by_estudiante(self, id_estudiante: int) -> List[EstudianteApoderado]:
        """Obtener todas las relaciones de un estudiante"""
        pass
    
    @abstractmethod
    def get_by_apoderado(self, id_apoderado: int) -> List[EstudianteApoderado]:
        """Obtener todas las relaciones de un apoderado"""
        pass
    
    @abstractmethod
    def get_contacto_principal(self, id_estudiante: int) -> Optional[EstudianteApoderado]:
        """Obtener el contacto principal de un estudiante"""
        pass
    
    @abstractmethod
    def update(self, id_estudiante: int, id_apoderado: int, relacion_data: dict) -> Optional[EstudianteApoderado]:
        """Actualizar una relación estudiante-apoderado"""
        pass
    
    @abstractmethod
    def delete(self, id_estudiante: int, id_apoderado: int) -> bool:
        """Eliminar una relación estudiante-apoderado"""
        pass
    
    @abstractmethod
    def set_contacto_principal(self, id_estudiante: int, id_apoderado: int) -> bool:
        """Establecer un apoderado como contacto principal (desmarcando otros)"""
        pass
