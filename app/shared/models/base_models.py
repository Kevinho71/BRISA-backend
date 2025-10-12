"""
Modelos base compartidos por todos los módulos del sistema BRISA
"""
from datetime import datetime
from app.core.extensions import db

class BaseModel(db.Model):
    """
    Modelo base con campos comunes a todas las entidades
    """
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
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
    Mixin para auditoría de cambios
    """
    
    @classmethod
    def create_audit_log(cls, action, entity_id, old_values=None, new_values=None, user_id=None):
        """Crear registro de auditoría"""
        # TODO: Implementar sistema de auditoría
        pass

class PersonaBase(BaseModel):
    """
    Modelo base para personas (estudiantes, profesores, administrativos)
    """
    __abstract__ = True
    
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    telefono = db.Column(db.String(15), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo"""
        return f"{self.nombres} {self.apellidos}"
    
    def __str__(self):
        return self.nombre_completo