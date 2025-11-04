"""
Script para probar conexión a MySQL sin contraseña
Ejecutar: python scripts/test_database_connection.py
"""

import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from pathlib import Path
from sqlalchemy import inspect
from core.database import engine
# ----------------------------
# Configuración de conexión
# ----------------------------

# Agregar la raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

print("🛠 Ruta del proyecto agregada a sys.path:", PROJECT_ROOT)

DB_USER = "root"
DB_PASSWORD = ""  
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "bienestar_estudiantil"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# Todas las tablas que realmente existen en MySQL
print("Tablas reales en la base de datos:")
for t in inspector.get_table_names():
    print("-", t)

# Tablas que SQLAlchemy conoce por modelos
print("\nTablas registradas en SQLAlchemy:")
for t in Base.metadata.tables.keys():
    print("-", t)
