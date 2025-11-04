import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base, get_db
from app.main import app

# ----------------------------
# Configuración de base de datos para testing
# ----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------
# Dependency override
# ----------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture(scope="function")
def db():
    """Crea las tablas al inicio del test y las elimina al final para tests aislados."""
    Base.metadata.create_all(bind=engine)  # Crear tablas
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Limpiar tablas

@pytest.fixture(scope="function")
def client():
    """Devuelve un cliente de FastAPI para hacer requests de prueba."""
    from fastapi.testclient import TestClient
    return TestClient(app)
