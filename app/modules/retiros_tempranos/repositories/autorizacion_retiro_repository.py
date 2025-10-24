from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.AutorizacionesRetiro import AutorizacionRetiro
from app.modules.retiros_tempranos.repositories.autorizacion_retiro_repository_interface import IAutorizacionRetiroRepository


class AutorizacionRetiroRepository(IAutorizacionRetiroRepository):
    """Implementación del repositorio de AutorizacionRetiro"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, autorizacion: AutorizacionRetiro) -> AutorizacionRetiro:
        """Crear una nueva autorización"""
        self.db.add(autorizacion)
        self.db.commit()
        self.db.refresh(autorizacion)
        return autorizacion
    
    def get_by_id(self, id_autorizacion: int) -> Optional[AutorizacionRetiro]:
        """Obtener una autorización por su ID"""
        return self.db.query(AutorizacionRetiro).filter(
            AutorizacionRetiro.id_autorizacion == id_autorizacion
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AutorizacionRetiro]:
        """Obtener todas las autorizaciones con paginación"""
        return self.db.query(AutorizacionRetiro).offset(skip).limit(limit).all()
    
    def get_by_decision(self, decision: str) -> List[AutorizacionRetiro]:
        """Obtener autorizaciones por tipo de decisión"""
        return self.db.query(AutorizacionRetiro).filter(
            AutorizacionRetiro.decision == decision
        ).all()
    
    def update(self, id_autorizacion: int, autorizacion_data: dict) -> Optional[AutorizacionRetiro]:
        """Actualizar una autorización"""
        autorizacion = self.get_by_id(id_autorizacion)
        if not autorizacion:
            return None
        
        for key, value in autorizacion_data.items():
            if value is not None and hasattr(autorizacion, key):
                setattr(autorizacion, key, value)
        
        self.db.commit()
        self.db.refresh(autorizacion)
        return autorizacion
    
    def delete(self, id_autorizacion: int) -> bool:
        """Eliminar una autorización"""
        autorizacion = self.get_by_id(id_autorizacion)
        if not autorizacion:
            return False
        
        self.db.delete(autorizacion)
        self.db.commit()
        return True
