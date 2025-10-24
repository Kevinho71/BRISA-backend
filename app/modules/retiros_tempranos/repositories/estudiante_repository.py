from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.Estudiante import Estudiante
from app.modules.retiros_tempranos.repositories.estudiante_repository_interface import IEstudianteRepository


class EstudianteRepository(IEstudianteRepository):
    """Implementación del repositorio de Estudiante"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, estudiante: Estudiante) -> Estudiante:
        """Crear un nuevo estudiante"""
        self.db.add(estudiante)
        self.db.commit()
        self.db.refresh(estudiante)
        return estudiante
    
    def get_by_id(self, id_estudiante: int) -> Optional[Estudiante]:
        """Obtener un estudiante por su ID"""
        return self.db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    
    def get_by_ci(self, ci: str) -> Optional[Estudiante]:
        """Obtener un estudiante por su cédula de identidad"""
        return self.db.query(Estudiante).filter(Estudiante.ci == ci).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        """Obtener todos los estudiantes con paginación"""
        return self.db.query(Estudiante).offset(skip).limit(limit).all()
    
    def update(self, id_estudiante: int, estudiante_data: dict) -> Optional[Estudiante]:
        """Actualizar un estudiante"""
        estudiante = self.get_by_id(id_estudiante)
        if not estudiante:
            return None
        
        for key, value in estudiante_data.items():
            if value is not None and hasattr(estudiante, key):
                setattr(estudiante, key, value)
        
        self.db.commit()
        self.db.refresh(estudiante)
        return estudiante
    
    def delete(self, id_estudiante: int) -> bool:
        """Eliminar un estudiante"""
        estudiante = self.get_by_id(id_estudiante)
        if not estudiante:
            return False
        
        self.db.delete(estudiante)
        self.db.commit()
        return True
    
    def exists_by_ci(self, ci: str) -> bool:
        """Verificar si existe un estudiante con la cédula dada"""
        return self.db.query(Estudiante).filter(Estudiante.ci == ci).count() > 0
