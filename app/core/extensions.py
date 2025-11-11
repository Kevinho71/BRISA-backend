from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from typing import Generator
import os

# Base para modelos SQLAlchemy
Base = declarative_base()

# Variables para sesión de BD
engine = None
SessionLocal = None

def init_extensions(app):
    """Inicializar todas las extensiones para FastAPI"""
    global engine, SessionLocal
    
    # Obtener configuración del entorno
    from app.config.config import config
    config_name = os.environ.get('ENV', 'development')
    app_config = config[config_name]
    
    # Guardar config en app para acceso posterior
    app.state.config = app_config
    
    database_url = app_config.DATABASE_URL
    echo_sql = app_config.SQLALCHEMY_ECHO
    
    print(f"🔗 Conectando a base de datos...")
    print(f"📍 URL: {database_url.split('@')[1].split('?')[0] if '@' in database_url else 'N/A'}")
    print(f"🔍 Echo SQL: {echo_sql}")
    
    # Configurar argumentos de conexión para MySQL
    connect_args = {}
    
    # Si es Aiven o requiere SSL, configurar SSL
    if 'aivencloud.com' in database_url or 'ssl' in database_url.lower():
        print("🔒 Conexión SSL detectada")
        connect_args = {
            'ssl': {
                'ssl_disabled': False
            }
        }
    
    # Crear engine de SQLAlchemy
    engine = create_engine(
        database_url,
        echo=echo_sql,
        pool_pre_ping=True,  # Verificar conexión antes de usar
        pool_size=10,         # Tamaño del pool de conexiones
        max_overflow=20,      # Conexiones adicionales si se necesita
        pool_recycle=3600,    # Reciclar conexiones cada hora
        poolclass=QueuePool,  # Usar QueuePool para conexiones persistentes
        connect_args=connect_args
    )
    
    # Crear SessionLocal
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Importar todos los modelos para que SQLAlchemy los reconozca
    import_all_models()
    
    print("✅ Extensiones inicializadas correctamente")
    
    return app

def import_all_models():
    """Importar todos los modelos para que SQLAlchemy los reconozca"""
    # Módulo Retiros Tempranos
    from app.modules.retiros_tempranos.models import (
        Estudiante,
        Apoderado,
        EstudianteApoderado,
        MotivoRetiro,
        AutorizacionRetiro,
        SolicitudRetiro,
        RegistroSalida,
        SolicitudRetiroDetalle,
    )
    
    # Módulo Estudiantes (modelos compartidos)
    from app.modules.estudiantes.models import (
        Curso,
        Materia,
        EstudianteCurso,
    )
    
    # Modelos compartidos
    from app.shared.models import (
        Persona,
        ProfesorCursoMateria,
    )
    
    print("📦 Modelos importados correctamente")

def get_db() -> Generator:
    """Dependency para obtener sesión de BD en FastAPI"""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_extensions first.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Crear todas las tablas en la base de datos"""
    if engine is None:
        raise RuntimeError("Database engine not initialized.")
    
    import_all_models()
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")

def drop_tables():
    """Eliminar todas las tablas de la base de datos"""
    if engine is None:
        raise RuntimeError("Database engine not initialized.")
    
    import_all_models()
    Base.metadata.drop_all(bind=engine)
    print("🗑️  Tablas eliminadas correctamente")