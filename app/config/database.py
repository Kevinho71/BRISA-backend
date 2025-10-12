# Configuración de la base de datos
from app.core.extensions import db

def init_database(app):
    """
    Inicializar base de datos con datos de prueba
    """
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        print("✅ Base de datos inicializada correctamente")

def reset_database(app):
    """
    Resetear la base de datos
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print("🔄 Base de datos reseteada correctamente")