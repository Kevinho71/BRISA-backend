"""
Modelos del Módulo de Bitacora
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Bitacora(Base):
    """Modelo de Bitácora - Bitacora de todas las acciones del sistema"""
    __tablename__ = "bitacora"
    __table_args__ = {"extend_existing": True}
    id_bitacora = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario_admin = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False, index=True)
    accion = Column(String(50), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    fecha_hora = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_objetivo = Column(Integer, nullable=True)
    tipo_objetivo = Column(String(50), nullable=True, index=True)
    
    # Relación con Usuario (quien realizó la acción)
    usuario_admin = relationship("Usuario", foreign_keys=[id_usuario_admin])
    
    def __repr__(self):
        return f"<Bitacora accion={self.accion} fecha={self.fecha_hora}>"
