from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.config import config
import os

# Seleccionar configuración según ENV
env = os.environ.get("ENV", "development")
Settings = config.get(env, config['default'])

# Engine y Session
engine = create_engine(
    Settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"charset": "utf8mb4"} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependencia para inyectar sesión de DB en FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Funciones de inicialización/reseteo opcionales
def init_database():
    """Crear todas las tablas en la DB"""
    Base.metadata.create_all(bind=engine)
    print(" Base de datos inicializada correctamente")

def reset_database():
    """Resetear la base de datos (drop + create)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("🔄 Base de datos reseteada correctamente")
