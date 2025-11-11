"""
Utilidades para gestión de base de datos
"""
from app.core.extensions import Base, engine, create_tables, drop_tables

def init_database():
    """
    Crear todas las tablas en la base de datos
    Usar solo en desarrollo o para inicialización
    """
    if engine is None:
        raise RuntimeError("Database engine not initialized. Call init_extensions first.")
    
    print("🔨 Creando tablas en la base de datos...")
    create_tables()
    print("✅ Base de datos inicializada correctamente")

def reset_database():
    """
    Resetear la base de datos (eliminar y recrear todas las tablas)
    ⚠️  CUIDADO: Esto elimina todos los datos
    """
    if engine is None:
        raise RuntimeError("Database engine not initialized. Call init_extensions first.")
    
    print("⚠️  RESETEANDO BASE DE DATOS...")
    drop_tables()
    create_tables()
    print("🔄 Base de datos reseteada correctamente")

def check_connection():
    """
    Verificar la conexión a la base de datos
    """
    if engine is None:
        raise RuntimeError("Database engine not initialized.")
    
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Conexión a base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False