from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.modules.retiros_tempranos.models.EstudianteApoderado import EstudianteApoderado
from app.modules.retiros_tempranos.repositories.estudiante_apoderado_repository_interface import IEstudianteApoderadoRepository


class EstudianteApoderadoRepository(IEstudianteApoderadoRepository):
    """Implementación del repositorio de EstudianteApoderado"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, relacion: EstudianteApoderado) -> EstudianteApoderado:
        """Crear una nueva relación estudiante-apoderado"""
        self.db.add(relacion)
        self.db.commit()
        self.db.refresh(relacion)
        return relacion
    
    def get_by_ids(self, id_estudiante: int, id_apoderado: int) -> Optional[EstudianteApoderado]:
        """Obtener una relación específica por IDs"""
        return self.db.query(EstudianteApoderado).filter(
            EstudianteApoderado.id_estudiante == id_estudiante,
            EstudianteApoderado.id_apoderado == id_apoderado
        ).first()
    
    def get_by_estudiante(self, id_estudiante: int) -> List[EstudianteApoderado]:
        """Obtener todas las relaciones de un estudiante"""
        return self.db.query(EstudianteApoderado).filter(
            EstudianteApoderado.id_estudiante == id_estudiante
        ).all()
    
    def get_by_apoderado(self, id_apoderado: int) -> List[EstudianteApoderado]:
        """Obtener todas las relaciones de un apoderado con datos del estudiante"""
        return self.db.query(EstudianteApoderado).options(
            joinedload(EstudianteApoderado.estudiante)
        ).filter(
            EstudianteApoderado.id_apoderado == id_apoderado
        ).all()
    
    def get_contacto_principal(self, id_estudiante: int) -> Optional[EstudianteApoderado]:
        """Obtener el contacto principal de un estudiante"""
        return self.db.query(EstudianteApoderado).filter(
            EstudianteApoderado.id_estudiante == id_estudiante,
            EstudianteApoderado.es_contacto_principal == True
        ).first()
    
    def update(self, id_estudiante: int, id_apoderado: int, relacion_data: dict) -> Optional[EstudianteApoderado]:
        """Actualizar una relación estudiante-apoderado"""
        relacion = self.get_by_ids(id_estudiante, id_apoderado)
        if not relacion:
            return None
        
        for key, value in relacion_data.items():
            if value is not None and hasattr(relacion, key):
                setattr(relacion, key, value)
        
        self.db.commit()
        self.db.refresh(relacion)
        return relacion
    
    def delete(self, id_estudiante: int, id_apoderado: int) -> bool:
        """Eliminar una relación estudiante-apoderado"""
        relacion = self.get_by_ids(id_estudiante, id_apoderado)
        if not relacion:
            return False
        
        self.db.delete(relacion)
        self.db.commit()
        return True
    
    def set_contacto_principal(self, id_estudiante: int, id_apoderado: int) -> bool:
        """Establecer un apoderado como contacto principal (desmarcando otros)"""
        # Desmarcar todos los contactos principales del estudiante
        self.db.query(EstudianteApoderado).filter(
            EstudianteApoderado.id_estudiante == id_estudiante
        ).update({"es_contacto_principal": False})
        
        # Marcar el nuevo contacto principal
        relacion = self.get_by_ids(id_estudiante, id_apoderado)
        if not relacion:
            return False
        
        relacion.es_contacto_principal = True
        self.db.commit()
        return True
