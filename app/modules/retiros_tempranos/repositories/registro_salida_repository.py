from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.modules.retiros_tempranos.models.RegistroSalida import RegistroSalida
from app.modules.retiros_tempranos.repositories.registro_salida_repository_interface import IRegistroSalidaRepository


class RegistroSalidaRepository(IRegistroSalidaRepository):
    """Implementación del repositorio de RegistroSalida"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, registro: RegistroSalida) -> RegistroSalida:
        """Crear un nuevo registro de salida"""
        self.db.add(registro)
        self.db.commit()
        self.db.refresh(registro)
        return registro
    
    def get_by_id(self, id_registro: int) -> Optional[RegistroSalida]:
        """Obtener un registro por su ID"""
        return self.db.query(RegistroSalida).filter(
            RegistroSalida.id_registro == id_registro
        ).first()
    
    def get_by_solicitud(self, id_solicitud: int) -> Optional[RegistroSalida]:
        """Obtener un registro por su ID de solicitud"""
        return self.db.query(RegistroSalida).filter(
            RegistroSalida.id_solicitud == id_solicitud
        ).first()
    
    def get_by_estudiante(self, id_estudiante: int) -> List[RegistroSalida]:
        """Obtener todos los registros de un estudiante"""
        return self.db.query(RegistroSalida).filter(
            RegistroSalida.id_estudiante == id_estudiante
        ).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[RegistroSalida]:
        """Obtener todos los registros con paginación"""
        return self.db.query(RegistroSalida).offset(skip).limit(limit).all()
    
    def get_sin_retorno(self) -> List[RegistroSalida]:
        """Obtener registros de salidas sin retorno"""
        return self.db.query(RegistroSalida).filter(
            RegistroSalida.fecha_hora_retorno_real.is_(None)
        ).all()
    
    def get_by_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[RegistroSalida]:
        """Obtener registros en un rango de fechas"""
        return self.db.query(RegistroSalida).filter(
            RegistroSalida.fecha_hora_salida_real >= fecha_inicio,
            RegistroSalida.fecha_hora_salida_real <= fecha_fin
        ).all()
    
    def update(self, id_registro: int, registro_data: dict) -> Optional[RegistroSalida]:
        """Actualizar un registro"""
        registro = self.get_by_id(id_registro)
        if not registro:
            return None
        
        for key, value in registro_data.items():
            if value is not None and hasattr(registro, key):
                setattr(registro, key, value)
        
        self.db.commit()
        self.db.refresh(registro)
        return registro
    
    def delete(self, id_registro: int) -> bool:
        """Eliminar un registro"""
        registro = self.get_by_id(id_registro)
        if not registro:
            return False
        
        self.db.delete(registro)
        self.db.commit()
        return True

