import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Configuración base para FastAPI"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Base de datos - SOLO desde .env
    DATABASE_URL = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    # Usar TEST_DATABASE_URL si existe, sino usar DATABASE_URL
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or os.environ.get('DATABASE_URL')

# 🔁 Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}