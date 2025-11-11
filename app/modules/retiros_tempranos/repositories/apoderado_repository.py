from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.Apoderado import Apoderado
from app.modules.retiros_tempranos.models.EstudianteApoderado import EstudianteApoderado
from app.modules.retiros_tempranos.repositories.apoderado_repository_interface import IApoderadoRepository


class ApoderadoRepository(IApoderadoRepository):
    """Implementación del repositorio de Apoderado"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, apoderado: Apoderado) -> Apoderado:
        """Crear un nuevo apoderado"""
        self.db.add(apoderado)
        self.db.commit()
        self.db.refresh(apoderado)
        return apoderado
    
    def get_by_id(self, id_apoderado: int) -> Optional[Apoderado]:
        """Obtener un apoderado por su ID"""
        return self.db.query(Apoderado).filter(Apoderado.id_apoderado == id_apoderado).first()
    
    def get_by_ci(self, ci: str) -> Optional[Apoderado]:
        """Obtener un apoderado por su cédula de identidad"""
        return self.db.query(Apoderado).filter(Apoderado.ci == ci).first()
    
    def get_by_estudiante(self, id_estudiante: int) -> List[Apoderado]:
        """Obtener todos los apoderados de un estudiante a través de la tabla intermedia"""
        return self.db.query(Apoderado)\
            .join(EstudianteApoderado, EstudianteApoderado.id_apoderado == Apoderado.id_apoderado)\
            .filter(EstudianteApoderado.id_estudiante == id_estudiante)\
            .all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Apoderado]:
        """Obtener todos los apoderados con paginación"""
        return self.db.query(Apoderado).offset(skip).limit(limit).all()
    
    def update(self, id_apoderado: int, apoderado_data: dict) -> Optional[Apoderado]:
        """Actualizar un apoderado"""
        apoderado = self.get_by_id(id_apoderado)
        if not apoderado:
            return None
        
        for key, value in apoderado_data.items():
            if value is not None and hasattr(apoderado, key):
                setattr(apoderado, key, value)
        
        self.db.commit()
        self.db.refresh(apoderado)
        return apoderado
    
    def delete(self, id_apoderado: int) -> bool:
        """Eliminar un apoderado"""
        apoderado = self.get_by_id(id_apoderado)
        if not apoderado:
            return False
        
        self.db.delete(apoderado)
        self.db.commit()
        return True
    
    def exists_by_ci(self, ci: str) -> bool:
        """Verificar si existe un apoderado con la cédula dada"""
        return self.db.query(Apoderado).filter(Apoderado.ci == ci).count() > 0
