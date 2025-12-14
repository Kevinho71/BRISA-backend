from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.retiros_tempranos.repositories.solicitud_retiro_masivo_repository_interface import SolicitudRetiroMasivoRepositoryInterface
from app.modules.retiros_tempranos.models.SolicitudRetiroMasivo import SolicitudRetiroMasivo


class SolicitudRetiroMasivoRepository(SolicitudRetiroMasivoRepositoryInterface):
    """Repositorio para la gestión de solicitudes de retiro masivo"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, solicitud: SolicitudRetiroMasivo) -> SolicitudRetiroMasivo:
        """Crea una nueva solicitud de retiro masivo"""
        self.db.add(solicitud)
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud

    def get_by_id(self, id_solicitud_masiva: int) -> Optional[SolicitudRetiroMasivo]:
        """Obtiene una solicitud por ID"""
        return self.db.query(SolicitudRetiroMasivo).filter(
            SolicitudRetiroMasivo.id_solicitud_masiva == id_solicitud_masiva
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene todas las solicitudes de retiro masivo"""
        return self.db.query(SolicitudRetiroMasivo).offset(skip).limit(limit).all()

    def get_by_solicitante(self, id_solicitante: int, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes por solicitante (profesor/admin)"""
        return self.db.query(SolicitudRetiroMasivo).filter(
            SolicitudRetiroMasivo.id_solicitante == id_solicitante
        ).offset(skip).limit(limit).all()

    def get_by_estado(self, estado: str, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes por estado"""
        return self.db.query(SolicitudRetiroMasivo).filter(
            SolicitudRetiroMasivo.estado == estado
        ).offset(skip).limit(limit).all()

    def get_pendientes(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes pendientes de recepción"""
        return self.get_by_estado("pendiente", skip, limit)

    def get_recibidas(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes recibidas (pendientes de derivar)"""
        return self.get_by_estado("recibida", skip, limit)

    def get_derivadas(self, id_regente: int, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes derivadas a un regente"""
        return self.db.query(SolicitudRetiroMasivo).filter(
            SolicitudRetiroMasivo.id_regente == id_regente,
            SolicitudRetiroMasivo.estado == "derivada"
        ).offset(skip).limit(limit).all()

    def get_aprobadas(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroMasivo]:
        """Obtiene solicitudes aprobadas"""
        return self.get_by_estado("aprobada", skip, limit)

    def update(self, solicitud: SolicitudRetiroMasivo) -> SolicitudRetiroMasivo:
        """Actualiza una solicitud de retiro masivo"""
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud

    def delete(self, id_solicitud_masiva: int) -> bool:
        """Elimina una solicitud de retiro masivo"""
        solicitud = self.get_by_id(id_solicitud_masiva)
        if solicitud:
            self.db.delete(solicitud)
            self.db.commit()
            return True
        return False
