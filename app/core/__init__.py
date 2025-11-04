# Core utilities and extensionsfrom .database import get_db
from .database import engine, get_db

# app/core/__init__.py

from app.config.config import DevelopmentConfig


# Variables de configuración que antes fallaban
SECRET_KEY = DevelopmentConfig.SECRET_KEY
DATABASE_URL = DevelopmentConfig.DATABASE_URL
ACCESS_TOKEN_EXPIRE_MINUTES = DevelopmentConfig.JWT_ACCESS_TOKEN_EXPIRES
ALGORITHM = "HS256"  # o lo que uses en tu JWT
