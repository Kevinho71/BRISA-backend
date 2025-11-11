"""
Script para ejecutar el esquema SQL en Aiven Cloud MySQL
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.core.extensions import engine
from sqlalchemy import text

print("=" * 70)
print("EJECUTAR ESQUEMA SQL EN AIVEN CLOUD")
print("=" * 70)
print()

# Leer el archivo SQL
sql_file = os.path.join(os.path.dirname(__file__), '..', 'docs', 'brisa_tablas.sql')

if not os.path.exists(sql_file):
    print(f"❌ No se encontró el archivo: {sql_file}")
    sys.exit(1)

print(f"📄 Leyendo esquema desde: docs/brisa_tablas.sql")

with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Dividir en statements individuales
statements = [s.strip() for s in sql_content.split(';') if s.strip()]

print(f"📊 Se encontraron {len(statements)} statements SQL")
print()

confirm = input("⚠️  ¿Ejecutar esquema en Aiven Cloud? (S/N): ")
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
        
        print("⚙️  Ejecutando statements...")
        print()
        
        for i, statement in enumerate(statements, 1):
            if not statement or statement.startswith('--'):
                continue
            
            try:
                # Ignorar comandos específicos de MySQL CLI
                if statement.upper().startswith(('USE ', 'SET FOREIGN_KEY_CHECKS')):
                    print(f"[{i}/{len(statements)}] ⏭️  Saltando: {statement[:50]}...")
                    continue
                
                connection.execute(text(statement))
                connection.commit()
                executed += 1
                
                # Mostrar progreso cada 10 statements
                if executed % 10 == 0:
                    print(f"   ✓ Ejecutados {executed} statements...")
                    
            except Exception as e:
                error_msg = str(e)
                # Ignorar errores de "tabla ya existe"
                if "already exists" in error_msg.lower():
                    print(f"[{i}/{len(statements)}] ⚠️  Ya existe: {statement[:50]}...")
                else:
                    print(f"[{i}/{len(statements)}] ❌ Error: {error_msg[:100]}")
                    errors += 1
        
        print()
        print("=" * 70)
        print("✅ PROCESO COMPLETADO")
        print("=" * 70)
        print(f"✓ Statements ejecutados: {executed}")
        print(f"⚠️  Errores: {errors}")
        
        # Verificar tablas creadas
        result = connection.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"\n📊 Tablas en la base de datos: {len(tables)}")
        for table in tables:
            print(f"   ✓ {table[0]}")
        
except Exception as e:
    print()
    print("❌ ERROR EJECUTANDO ESQUEMA")
    print(f"{str(e)}")
    sys.exit(1)
