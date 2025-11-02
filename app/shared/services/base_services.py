"""
Servicios compartidos del sistema BRISA
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.core.extensions import db
from app.shared.exceptions.custom_exceptions import NotFound, DatabaseException
from sqlalchemy.orm import Session


class BaseService:
    """Servicio base con operaciones CRUD comunes"""
    
    model_class = None
    
    @classmethod
    def get_all(cls, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 10):
        """Obtener todos los registros con paginación y filtros"""
        try:
            query = cls.model_class.query.filter_by(is_active=True)
            
            # Aplicar filtros
            if filters:
                for key, value in filters.items():
                    if hasattr(cls.model_class, key) and value is not None:
                        query = query.filter(getattr(cls.model_class, key) == value)
            
            # Paginar
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'items': [item.to_dict() for item in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        except Exception as e:
            raise DatabaseException(f"Error retrieving records: {str(e)}")
    
    @classmethod
    def get_by_id(cls, entity_id: int):
        """Obtener registro por ID"""
        try:
            entity = cls.model_class.query.filter_by(
                id=entity_id, 
                is_active=True
            ).first()
            
            if not entity:
                raise NotFound(cls.model_class.__name__, entity_id)
            
            return entity
        except NotFound:
            raise
        except Exception as e:
            raise DatabaseException(f"Error retrieving record: {str(e)}")
    
    @classmethod
    def create(cls, data: Dict[str, Any], user_id: Optional[int] = None):
        """Crear nuevo registro"""
        try:
            # Añadir metadatos
            if user_id:
                data['created_by'] = user_id
            
            entity = cls.model_class(**data)
            db.session.add(entity)
            db.session.commit()
            
            return entity
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f"Error creating record: {str(e)}")
    
    @classmethod
    def update(cls, entity_id: int, data: Dict[str, Any], user_id: Optional[int] = None):
        """Actualizar registro"""
        try:
            entity = cls.get_by_id(entity_id)
            
            # Actualizar campos
            entity.update_from_dict(data)
            
            if user_id:
                entity.updated_by = user_id
            
            entity.updated_at = datetime.utcnow()
            
            db.session.commit()
            return entity
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f"Error updating record: {str(e)}")
    
    @classmethod
    def delete(cls, entity_id: int, soft_delete: bool = True):
        """Eliminar registro (lógica o física)"""
        try:
            entity = cls.get_by_id(entity_id)
            
            if soft_delete:
                entity.soft_delete()
                db.session.commit()
            else:
                db.session.delete(entity)
                db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f"Error deleting record: {str(e)}")

class AuditService:
    """Servicio para auditoría y logs"""
    
    @staticmethod
    def log_user_action(user_id: int, action: str, entity_type: str, 
                       entity_id: Optional[int] = None, details: Optional[Dict] = None):
        """Registrar acción del usuario"""
        # TODO: Implementar logging en base de datos o archivo
        log_entry = {
            'user_id': user_id,
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'details': details,
            'timestamp': datetime.utcnow().isoformat(),
            'ip_address': None  # TODO: obtener de request
        }
        
        # Por ahora solo imprimir, luego guardar en BD
        print(f"AUDIT LOG: {log_entry}")

class NotificationService:
    """Servicio para notificaciones"""
    
    @staticmethod
    def send_email(to: str, subject: str, body: str, html_body: Optional[str] = None):
        """Enviar notificación por email"""
        # TODO: Implementar envío real de emails
        print(f"EMAIL TO: {to}, SUBJECT: {subject}")
        return True
    
    @staticmethod
    def send_sms(to: str, message: str):
        """Enviar notificación por SMS"""
        # TODO: Implementar envío real de SMS
        print(f"SMS TO: {to}, MESSAGE: {message}")
        return True

class ReportService:
    """Servicio para generación de reportes"""
    
    @staticmethod
    def generate_pdf_report(data: List[Dict], template: str, filename: str):
        """Generar reporte en PDF"""
        # TODO: Implementar generación real de PDFs
        print(f"GENERATING PDF: {filename} with template {template}")
        return f"/reports/{filename}"
    
    @staticmethod
    def generate_excel_report(data: List[Dict], filename: str):
        """Generar reporte en Excel"""
        # TODO: Implementar generación real de Excel
        print(f"GENERATING EXCEL: {filename}")
        return f"/reports/{filename}"

class CacheService:
    """Servicio para manejo de caché"""
    
    @staticmethod
    def get(key: str):
        """Obtener valor del caché"""
        # TODO: Implementar con Redis
        return None
    
    @staticmethod
    def set(key: str, value: Any, expiration: int = 3600):
        """Guardar valor en caché"""
        # TODO: Implementar con Redis
        pass
    
    @staticmethod
    def delete(key: str):
        """Eliminar valor del caché"""
        # TODO: Implementar con Redis
        pass