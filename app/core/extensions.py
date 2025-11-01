from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from fastapi import HTTPException

# Base para modelos SQLAlchemy
Base = declarative_base()

# Variables para sesión de BD
engine = None
SessionLocal = None


def init_extensions(app):
    """Inicializar todas las extensiones para FastAPI"""
    global engine, SessionLocal

    # Obtener URL de la base de datos desde config
    database_url = (
        app.config.DATABASE_URL
        if hasattr(app, "config")
        else "mysql+pymysql://user:password@localhost/brisa"
    )

    # Crear engine con echo=False para reducir logs
    engine = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
    )

    # Crear SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # NO crear tablas aquí - hazlo manualmente o con migraciones
    # Base.metadata.create_all(bind=engine)

    return app


def get_db() -> Generator:
    """Dependency para obtener sesión de BD en FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

