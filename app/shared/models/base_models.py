from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session
from app.core.database import get_db


Base = declarative_base()

class BaseModel(Base):
    """
    Modelo base con campos comunes a todas las entidades
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    updated_by = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    def to_dict(self, include_relationships=False):
        """Convertir modelo a diccionario"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result

    def update_from_dict(self, data, exclude_fields=None):
        """Actualizar modelo desde diccionario"""
        exclude_fields = exclude_fields or ['id', 'created_at', 'created_by']

        for key, value in data.items():
            if key not in exclude_fields and hasattr(self, key):
                setattr(self, key, value)

    def soft_delete(self):
        """Eliminación lógica"""
        self.is_active = False

    def restore(self):
        """Restaurar elemento eliminado lógicamente"""
        self.is_active = True

class AuditMixin:
    """
    Mixin para bitacora de cambios
    """

    @classmethod
    def create_audit_log(cls, db: Session, action, entity_id, old_values=None, new_values=None, user_id=None):
        """Crear registro de bitacora"""
        # TODO: Implementar sistema de bitacora en base de datos o en un sistema de logging
        audit_log = {
            'action': action,
            'entity_id': entity_id,
            'old_values': old_values,
            'new_values': new_values,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        
        print(f"AUDIT LOG: {audit_log}")
