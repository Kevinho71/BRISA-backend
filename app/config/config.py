# app/config/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Config:
    """Configuración base para FastAPI"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # 🔧 Conexión a tu base real
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@127.0.0.1:3306/bienestar_estudiantil'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@127.0.0.1:3306/bienestar_estudiantil'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@127.0.0.1:3306/bienestar_estudiantil'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or 'mysql+pymysql://root:@127.0.0.1:3306/bienestar_estudiantil'

# 🔁 Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
