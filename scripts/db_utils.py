"""
Script de utilidades para gestión de base de datos
Ejecutar desde la raíz del proyecto con: python scripts/db_utils.py [comando]
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config.database import init_database, reset_database, check_connection
from app.core.extensions import engine
from sqlalchemy import text

def create_tables():
    """Crear todas las tablas"""
    print("=" * 60)
    print("CREAR TABLAS EN LA BASE DE DATOS")
    print("=" * 60)
    
    app = create_app('development')
    init_database()
    print("\n✅ Proceso completado")

def drop_and_create():
    """Eliminar y recrear todas las tablas"""
    print("=" * 60)
    print("⚠️  RESETEAR BASE DE DATOS (ELIMINAR TODOS LOS DATOS)")
    print("=" * 60)
    
    confirm = input("\n¿Estás seguro? Esta acción eliminará todos los datos (s/n): ")
    if confirm.lower() != 's':
        print("❌ Operación cancelada")
        return
    
    app = create_app('development')
    reset_database()
    print("\n✅ Proceso completado")

def test_connection():
    """Probar conexión a la base de datos"""
    print("=" * 60)
    print("PROBAR CONEXIÓN A BASE DE DATOS")
    print("=" * 60)
    
    app = create_app('development')
    
    if check_connection():
        # Mostrar información de la BD
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT DATABASE() as db_name"))
                db_name = result.fetchone()[0]
                print(f"📍 Base de datos actual: {db_name}")
                
                result = conn.execute(text("SELECT VERSION() as version"))
                version = result.fetchone()[0]
                print(f"🔢 Versión de MySQL: {version}")
                
                result = conn.execute(text("SHOW TABLES"))
                tables = result.fetchall()
                print(f"\n📊 Tablas en la base de datos ({len(tables)}):")
                for table in tables:
                    print(f"   - {table[0]}")
        except Exception as e:
            print(f"⚠️  Error al obtener información: {e}")
    else:
        print("\n❌ No se pudo establecer conexión")
        print("\n💡 Verifica:")
        print("   1. MySQL está corriendo")
        print("   2. Las credenciales en .env son correctas")
        print("   3. La base de datos 'brisa_db' existe")

def show_help():
    """Mostrar ayuda"""
    print("=" * 60)
    print("UTILIDADES DE BASE DE DATOS - BRISA Backend")
    print("=" * 60)
    print("\nComandos disponibles:\n")
    print("  test       - Probar conexión a la base de datos")
    print("  create     - Crear todas las tablas (si no existen)")
    print("  reset      - ELIMINAR y recrear todas las tablas")
    print("  help       - Mostrar esta ayuda")
    print("\nEjemplo de uso:")
    print("  python scripts/db_utils.py test")
    print("  python scripts/db_utils.py create")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "test":
        test_connection()
    elif command == "create":
        create_tables()
    elif command == "reset":
        drop_and_create()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Comando desconocido: {command}")
        print("\nUsa 'python scripts/db_utils.py help' para ver los comandos disponibles")
        sys.exit(1)
