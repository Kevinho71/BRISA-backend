from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.MotivoRetiro import MotivoRetiro
from app.modules.retiros_tempranos.repositories.motivo_retiro_repository_interface import IMotivoRetiroRepository


class MotivoRetiroRepository(IMotivoRetiroRepository):
    """Implementación del repositorio de MotivoRetiro"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, motivo: MotivoRetiro) -> MotivoRetiro:
        """Crear un nuevo motivo de retiro"""
        self.db.add(motivo)
        self.db.commit()
        self.db.refresh(motivo)
        return motivo
    
    def get_by_id(self, id_motivo: int) -> Optional[MotivoRetiro]:
        """Obtener un motivo por su ID"""
        return self.db.query(MotivoRetiro).filter(MotivoRetiro.id_motivo == id_motivo).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[MotivoRetiro]:
        """Obtener todos los motivos con paginación"""
        return self.db.query(MotivoRetiro).offset(skip).limit(limit).all()
    
    def get_activos(self) -> List[MotivoRetiro]:
        """Obtener solo los motivos activos"""
        return self.db.query(MotivoRetiro).filter(MotivoRetiro.activo == True).all()
    
    def get_by_severidad(self, severidad: str) -> List[MotivoRetiro]:
        """Obtener motivos por nivel de severidad"""
        return self.db.query(MotivoRetiro).filter(MotivoRetiro.severidad == severidad).all()
    
    def update(self, id_motivo: int, motivo_data: dict) -> Optional[MotivoRetiro]:
        """Actualizar un motivo"""
        motivo = self.get_by_id(id_motivo)
        if not motivo:
            return None
        
        for key, value in motivo_data.items():
            if value is not None and hasattr(motivo, key):
                setattr(motivo, key, value)
        
        self.db.commit()
        self.db.refresh(motivo)
        return motivo
    
    def delete(self, id_motivo: int) -> bool:
        """Eliminar un motivo"""
        motivo = self.get_by_id(id_motivo)
        if not motivo:
            return False
        
        self.db.delete(motivo)
        self.db.commit()
        return True
