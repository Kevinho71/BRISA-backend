# alembic/env.py
import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ----------------------------
# Configuración inicial
# ----------------------------

# Agregar ruta del proyecto para importar app.config y modelos
sys.path.insert(0, str(Path(__file__).parent.parent))

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de Alembic
config = context.config

# Configurar logging desde alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------
# Importar Base y modelos
# ----------------------------
from core.database import Base

# Módulo usuarios
from app.modules.usuarios.models.usuario_models import (
    Persona1, Usuario, Rol, Permiso, LoginLog, RolHistorial, Bitacora
)

# Módulo administracion (ejemplo: estudiantes)


# Módulo esquelas


# Metadata que Alembic usará para autogenerate
target_metadata = Base.metadata

# ----------------------------
# Configurar URL de la base de datos
# ----------------------------
sqlalchemy_url = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root@127.0.0.1:3306/bienestar_estudiantil?charset=utf8mb4"
)

config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# ----------------------------
# Funciones de migración
# ----------------------------

def run_migrations_offline():
    """Ejecuta migraciones en modo offline (solo SQL)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo online (conectando al DB)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detecta cambios en tipos de columnas
            render_as_batch=True  # Útil para SQLite o futuras migraciones
        )
        with context.begin_transaction():
            context.run_migrations()


# ----------------------------
# Ejecutar según el modo
# ----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
