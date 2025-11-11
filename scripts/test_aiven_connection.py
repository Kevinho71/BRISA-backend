"""
Script rápido para probar la conexión a Aiven Cloud MySQL
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("=" * 70)
print("PRUEBA DE CONEXIÓN - AIVEN CLOUD MYSQL")
print("=" * 70)
print()

try:
    print("📦 Cargando configuración...")
    from app import create_app
    from app.core.extensions import engine
    from sqlalchemy import text
    
    print("🔧 Inicializando aplicación...")
    app = create_app('development')
    
    print("🔗 Intentando conectar a Aiven Cloud...")
    print()
    
    with engine.connect() as connection:
        # Verificar versión de MySQL
        result = connection.execute(text("SELECT VERSION() as version"))
        version = result.fetchone()[0]
        print(f"✅ CONEXIÓN EXITOSA!")
        print(f"🔢 Versión MySQL: {version}")
        
        # Verificar base de datos actual
        result = connection.execute(text("SELECT DATABASE() as db_name"))
        db_name = result.fetchone()[0]
        print(f"📍 Base de datos: {db_name}")
        
        # Listar tablas existentes
        result = connection.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"\n📊 Tablas encontradas: {len(tables)}")
        
        if len(tables) > 0:
            print("\nTablas existentes:")
            for table in tables:
                print(f"   ✓ {table[0]}")
        else:
            print("\n⚠️  No hay tablas creadas aún")
            print("   Ejecuta: mysql -h bienestarestudiantil-hola.e.aivencloud.com -P 19241 -u avnadmin -p defaultdb < docs/brisa_tablas.sql")
        
        print()
        print("=" * 70)
        print("✅ PRUEBA COMPLETADA - LA CONEXIÓN FUNCIONA CORRECTAMENTE")
        print("=" * 70)
        
except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERROR EN LA CONEXIÓN")
    print("=" * 70)
    print(f"\n{str(e)}\n")
    print("💡 Posibles soluciones:")
    print("   1. Verifica que las credenciales en .env sean correctas")
    print("   2. Verifica tu conexión a internet")
    print("   3. Verifica que el servicio Aiven esté activo")
    print("   4. Instala el paquete cryptography: pip install cryptography")
    print()
    sys.exit(1)
