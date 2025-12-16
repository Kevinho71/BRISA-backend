from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.SolicitudRetiro import SolicitudRetiro
from app.modules.retiros_tempranos.repositories.solicitud_retiro_repository_interface import ISolicitudRetiroRepository


class SolicitudRetiroRepository(ISolicitudRetiroRepository):
    """Implementación del repositorio de SolicitudRetiro"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, solicitud: SolicitudRetiro) -> SolicitudRetiro:
        """Crear una nueva solicitud de retiro"""
        self.db.add(solicitud)
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud
    
    def get_by_id(self, id_solicitud: int) -> Optional[SolicitudRetiro]:
        """Obtener una solicitud por su ID"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.id_solicitud == id_solicitud
        ).first()
    
    def get_by_estudiante(self, id_estudiante: int) -> List[SolicitudRetiro]:
        """Obtener todas las solicitudes de un estudiante"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.id_estudiante == id_estudiante
        ).all()
    
    def get_by_apoderado(self, id_apoderado: int) -> List[SolicitudRetiro]:
        """Obtener todas las solicitudes de un apoderado"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.id_apoderado == id_apoderado
        ).order_by(SolicitudRetiro.fecha_creacion.desc()).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiro]:
        """Obtener todas las solicitudes con paginación"""
        return self.db.query(SolicitudRetiro).offset(skip).limit(limit).all()
    
    def get_pendientes(self) -> List[SolicitudRetiro]:
        """Obtener solicitudes pendientes de autorización"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.id_autorizacion.is_(None)
        ).all()
    
    def get_by_motivo(self, id_motivo: int) -> List[SolicitudRetiro]:
        """Obtener solicitudes por motivo"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.id_motivo == id_motivo
        ).all()
    
    def get_by_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[SolicitudRetiro]:
        """Obtener solicitudes en un rango de fechas"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.fecha_creacion >= fecha_inicio,
            SolicitudRetiro.fecha_creacion <= fecha_fin
        ).all()
    
    def get_by_estado(self, estado: str, skip: int = 0, limit: int = 100) -> List[SolicitudRetiro]:
        """Obtener solicitudes por estado con paginación"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.estado == estado
        ).order_by(SolicitudRetiro.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    def update(self, id_solicitud: int, solicitud_data: dict) -> Optional[SolicitudRetiro]:
        """Actualizar una solicitud"""
        solicitud = self.get_by_id(id_solicitud)
        if not solicitud:
            return None
        
        for key, value in solicitud_data.items():
            if value is not None and hasattr(solicitud, key):
                setattr(solicitud, key, value)
        
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud
    
    def get_by_autorizacion(self, id_autorizacion: int) -> Optional[SolicitudRetiro]:
        """Obtener una solicitud por id_autorizacion"""
        return self.db.query(SolicitudRetiro).filter(
            SolicitudRetiro.id_autorizacion == id_autorizacion
        ).first()
    
    def delete(self, id_solicitud: int) -> bool:
        """Eliminar una solicitud"""
        solicitud = self.get_by_id(id_solicitud)
        if not solicitud:
            return False
        
        self.db.delete(solicitud)
        self.db.commit()
        return True
