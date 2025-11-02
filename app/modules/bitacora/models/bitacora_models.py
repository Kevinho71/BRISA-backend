"""
Modelos del Módulo de Bitácora
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.models.base_models import Base, BaseModel

class Bitacora(BaseModel):
    """Modelo de Bitácora - Registro de todas las acciones del sistema"""
    __tablename__ = "bitacora"
    
    id_usuario_admin = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    accion = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    id_objetivo = Column(Integer, nullable=True)
    tipo_objetivo = Column(String(50), nullable=True, index=True)
    estado_anterior = Column(JSON, nullable=True)
    estado_nuevo = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Relación con Usuario (quien realizó la acción)
    usuario_admin = relationship("Usuario", foreign_keys=[id_usuario_admin])
    
    def __repr__(self):
        return f"<Bitacora accion={self.accion} fecha={self.created_at}>"
