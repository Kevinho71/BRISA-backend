import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base para FastAPI"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Base de datos MySQL
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/brisa_db'
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Ver queries SQL en desarrollo
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/brisa_db'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/brisa_db'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_ECHO = False
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or 'mysql+pymysql://root:password@localhost/brisa_test'

# Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}