from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.SoliticitudRetiroDetalle import SolicitudRetiroDetalle
from app.modules.retiros_tempranos.repositories.solicitud_retiro_detalle_repository_interface import ISolicitudRetiroDetalleRepository


class SolicitudRetiroDetalleRepository(ISolicitudRetiroDetalleRepository):
    """Implementación del repositorio de SolicitudRetiroDetalle"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, detalle: SolicitudRetiroDetalle) -> SolicitudRetiroDetalle:
        """Crear un nuevo detalle de solicitud"""
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle
    
    def get_by_id(self, id_detalle: int) -> Optional[SolicitudRetiroDetalle]:
        """Obtener un detalle por su ID"""
        return self.db.query(SolicitudRetiroDetalle).filter(
            SolicitudRetiroDetalle.id_detalle == id_detalle
        ).first()
    
    def get_by_solicitud(self, id_solicitud: int) -> List[SolicitudRetiroDetalle]:
        """Obtener todos los detalles de una solicitud"""
        return self.db.query(SolicitudRetiroDetalle).filter(
            SolicitudRetiroDetalle.id_solicitud == id_solicitud
        ).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroDetalle]:
        """Obtener todos los detalles con paginación"""
        return self.db.query(SolicitudRetiroDetalle).offset(skip).limit(limit).all()
    
    def update(self, id_detalle: int, detalle_data: dict) -> Optional[SolicitudRetiroDetalle]:
        """Actualizar un detalle"""
        detalle = self.get_by_id(id_detalle)
        if not detalle:
            return None
        
        for key, value in detalle_data.items():
            if value is not None and hasattr(detalle, key):
                setattr(detalle, key, value)
        
        self.db.commit()
        self.db.refresh(detalle)
        return detalle
    
    def delete(self, id_detalle: int) -> bool:
        """Eliminar un detalle"""
        detalle = self.get_by_id(id_detalle)
        if not detalle:
            return False
        
        self.db.delete(detalle)
        self.db.commit()
        return True
    
    def delete_by_solicitud(self, id_solicitud: int) -> bool:
        """Eliminar todos los detalles de una solicitud"""
        detalles = self.get_by_solicitud(id_solicitud)
        if not detalles:
            return False
        
        for detalle in detalles:
            self.db.delete(detalle)
        
        self.db.commit()
        return True
