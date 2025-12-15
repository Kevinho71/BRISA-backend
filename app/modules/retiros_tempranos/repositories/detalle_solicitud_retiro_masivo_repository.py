from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.retiros_tempranos.repositories.detalle_solicitud_retiro_masivo_repository_interface import DetalleSolicitudRetiroMasivoRepositoryInterface
from app.modules.retiros_tempranos.models.DetalleSolicitudRetiroMasivo import DetalleSolicitudRetiroMasivo


class DetalleSolicitudRetiroMasivoRepository(DetalleSolicitudRetiroMasivoRepositoryInterface):
    """Repositorio para la gestión de detalles de solicitud masiva"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, detalle: DetalleSolicitudRetiroMasivo) -> DetalleSolicitudRetiroMasivo:
        """Crea un nuevo detalle de solicitud"""
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def create_multiple(self, detalles: List[DetalleSolicitudRetiroMasivo]) -> List[DetalleSolicitudRetiroMasivo]:
        """Crea múltiples detalles de solicitud"""
        self.db.add_all(detalles)
        self.db.commit()
        for detalle in detalles:
            self.db.refresh(detalle)
        return detalles

    def get_by_id(self, id_detalle: int) -> Optional[DetalleSolicitudRetiroMasivo]:
        """Obtiene un detalle por ID"""
        return self.db.query(DetalleSolicitudRetiroMasivo).filter(
            DetalleSolicitudRetiroMasivo.id_detalle == id_detalle
        ).first()

    def get_by_solicitud(self, id_solicitud_masiva: int) -> List[DetalleSolicitudRetiroMasivo]:
        """Obtiene todos los detalles de una solicitud masiva"""
        return self.db.query(DetalleSolicitudRetiroMasivo).filter(
            DetalleSolicitudRetiroMasivo.id_solicitud_masiva == id_solicitud_masiva
        ).all()

    def get_by_estudiante(self, id_estudiante: int) -> List[DetalleSolicitudRetiroMasivo]:
        """Obtiene todos los detalles de un estudiante"""
        return self.db.query(DetalleSolicitudRetiroMasivo).filter(
            DetalleSolicitudRetiroMasivo.id_estudiante == id_estudiante
        ).all()

    def update(self, detalle: DetalleSolicitudRetiroMasivo) -> DetalleSolicitudRetiroMasivo:
        """Actualiza un detalle de solicitud"""
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def delete(self, id_detalle: int) -> bool:
        """Elimina un detalle de solicitud"""
        detalle = self.get_by_id(id_detalle)
        if detalle:
            self.db.delete(detalle)
            self.db.commit()
            return True
        return False

    def delete_by_solicitud(self, id_solicitud_masiva: int) -> int:
        """Elimina todos los detalles de una solicitud masiva. Retorna cantidad eliminada."""
        count = self.db.query(DetalleSolicitudRetiroMasivo).filter(
            DetalleSolicitudRetiroMasivo.id_solicitud_masiva == id_solicitud_masiva
        ).delete()
        self.db.commit()
        return count
