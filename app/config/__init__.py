# app/config/__init__.py

from app.core.database import engine, Base, SessionLocal
from app.config.config import config

# Selecciona la configuración deseada
current_config = config['default']  # o 'development', 'production', etc.
