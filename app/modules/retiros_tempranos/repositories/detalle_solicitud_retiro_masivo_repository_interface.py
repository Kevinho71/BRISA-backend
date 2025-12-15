from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.DetalleSolicitudRetiroMasivo import DetalleSolicitudRetiroMasivo


class DetalleSolicitudRetiroMasivoRepositoryInterface(ABC):
    """Interfaz del repositorio de detalles de solicitud masiva"""

    @abstractmethod
    def create(self, detalle: DetalleSolicitudRetiroMasivo) -> DetalleSolicitudRetiroMasivo:
        """Crea un nuevo detalle de solicitud"""
        pass

    @abstractmethod
    def create_multiple(self, detalles: List[DetalleSolicitudRetiroMasivo]) -> List[DetalleSolicitudRetiroMasivo]:
        """Crea múltiples detalles de solicitud"""
        pass

    @abstractmethod
    def get_by_id(self, id_detalle: int) -> Optional[DetalleSolicitudRetiroMasivo]:
        """Obtiene un detalle por ID"""
        pass

    @abstractmethod
    def get_by_solicitud(self, id_solicitud_masiva: int) -> List[DetalleSolicitudRetiroMasivo]:
        """Obtiene todos los detalles de una solicitud masiva"""
        pass

    @abstractmethod
    def get_by_estudiante(self, id_estudiante: int) -> List[DetalleSolicitudRetiroMasivo]:
        """Obtiene todos los detalles de un estudiante"""
        pass

    @abstractmethod
    def update(self, detalle: DetalleSolicitudRetiroMasivo) -> DetalleSolicitudRetiroMasivo:
        """Actualiza un detalle de solicitud"""
        pass

    @abstractmethod
    def delete(self, id_detalle: int) -> bool:
        """Elimina un detalle de solicitud"""
        pass

    @abstractmethod
    def delete_by_solicitud(self, id_solicitud_masiva: int) -> int:
        """Elimina todos los detalles de una solicitud masiva. Retorna cantidad eliminada."""
        pass
