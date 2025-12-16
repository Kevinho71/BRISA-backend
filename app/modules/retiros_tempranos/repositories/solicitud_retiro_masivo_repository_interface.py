from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.retiros_tempranos.models.SolicitudRetiroMasivo import SolicitudRetiroMasivo


class SolicitudRetiroMasivoRepositoryInterface(ABC):
    """Interfaz del repositorio de solicitudes de retiro masivo"""

    @abstractmethod
    def create(self, solicitud: SolicitudRetiroMasivo) -> SolicitudRetiroMasivo:
        """Crea una nueva solicitud de retiro masivo"""
        pass

    @abstractmethod
    def get_by_id(self, id_solicitud_masiva: int) -> Optional[SolicitudRetiroMasivo]:
        """Obtiene una solicitud por ID"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene todas las solicitudes de retiro masivo"""
        pass

    @abstractmethod
    def get_by_solicitante(self, id_solicitante: int, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes por solicitante (profesor/admin)"""
        pass

    @abstractmethod
    def get_by_estado(self, estado: str, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes por estado"""
        pass

    @abstractmethod
    def get_pendientes(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes pendientes de recepción"""
        pass

    @abstractmethod
    def get_recibidas(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes recibidas (pendientes de derivar)"""
        pass

    @abstractmethod
    def get_aprobadas(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes aprobadas"""
        pass

    @abstractmethod
    def update(self, solicitud: SolicitudRetiroMasivo) -> SolicitudRetiroMasivo:
        """Actualiza una solicitud de retiro masivo"""
        pass

    @abstractmethod
    def delete(self, id_solicitud_masiva: int) -> bool:
        """Elimina una solicitud de retiro masivo"""
        pass
