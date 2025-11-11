"""
Script para cargar datos de prueba en Aiven Cloud MySQL
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.core.extensions import engine
from sqlalchemy import text

print("=" * 70)
print("CARGAR DATOS DE PRUEBA EN AIVEN CLOUD")
print("=" * 70)
print()

# Leer el archivo SQL
sql_file = os.path.join(os.path.dirname(__file__), '..', 'docs', 'seed_data.sql')

if not os.path.exists(sql_file):
    print(f"❌ No se encontró el archivo: {sql_file}")
    sys.exit(1)

print(f"📄 Leyendo datos desde: docs/seed_data.sql")

with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Dividir en statements individuales
statements = [s.strip() for s in sql_content.split(';') if s.strip()]

print(f"📊 Se encontraron {len(statements)} statements SQL")
print()

confirm = input("⚠️  ¿Cargar datos de prueba en Aiven Cloud? (S/N): ")
if confirm.lower() != 's':
    print("❌ Operación cancelada")
    sys.exit(0)

print()
print("🔧 Inicializando aplicación...")
app = create_app('development')

print("🔗 Conectando a Aiven Cloud...")

try:
    with engine.connect() as connection:
        executed = 0
        errors = 0
        
        print("⚙️  Cargando datos...")
        print()
        
        for i, statement in enumerate(statements, 1):
            if not statement or statement.startswith('--') or statement.startswith('/*'):
                continue
            
            try:
                # Ignorar comandos específicos
                upper_stmt = statement.upper()
                if upper_stmt.startswith(('USE ', 'SET FOREIGN_KEY_CHECKS', 'TRUNCATE', 'SELECT')):
                    if upper_stmt.startswith('TRUNCATE'):
                        print(f"[{i}] ⏭️  Saltando TRUNCATE (datos en producción)...")
                    continue
                
                connection.execute(text(statement))
                connection.commit()
                executed += 1
                
                # Mostrar qué se insertó
                if 'INSERT INTO' in upper_stmt:
                    table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                    print(f"[{executed}] ✓ Insertado en: {table_name}")
                    
            except Exception as e:
                error_msg = str(e)
                if "duplicate" in error_msg.lower() or "already exists" in error_msg.lower():
                    print(f"[{i}] ⚠️  Registro duplicado (ya existe)")
                else:
                    print(f"[{i}] ❌ Error: {error_msg[:100]}")
                    errors += 1
        
        print()
        print("=" * 70)
        print("✅ DATOS CARGADOS")
        print("=" * 70)
        print(f"✓ Statements ejecutados: {executed}")
        print(f"⚠️  Errores/Duplicados: {errors}")
        
        # Verificar datos insertados
        print("\n📊 Resumen de datos:")
        tables_to_check = [
            'personas', 'estudiantes', 'cursos', 'materias', 
            'apoderados', 'estudiantes_apoderados', 'motivos_retiro'
        ]
        
        for table in tables_to_check:
            try:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"   {table}: {count} registros")
            except:
                pass
        
except Exception as e:
    print()
    print("❌ ERROR CARGANDO DATOS")
    print(f"{str(e)}")
    sys.exit(1)
