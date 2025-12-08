"""
Script para probar endpoints principales del backend.
Ejecutar: python -m pytest scripts/test_endpoints.py -v
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal

# Aseguramos que 'app' esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.shared.security import verify_token  # la dependencia que usamos en los endpoints

# ==============================
# Función que reemplaza verify_token solo para tests
# ==============================
def fake_verify_token():
    return {
        "usuario_id": 1,
        "usuario": "cperez",
        "permisos": ["listar_usuarios", "crear_usuario", "eliminar_usuario"]
    }

# ==============================
# Fixture para usar DB de prueba
# ==============================
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sobreescribir dependencias de FastAPI
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_token] = fake_verify_token

client = TestClient(app)

# ==============================
# Test de salud del servidor
# ==============================
def test_health():
    response = client.get("/")
    print(f"[TEST] GET / -> {response.status_code}")
    assert response.status_code == 200

# ==============================
# Test de endpoints de usuarios
# ==============================
def test_usuario_endpoints():
    # Ya no necesitamos token real, fake_verify_token lo inyecta
    response = client.get("/api/usuarios")
    print(f"[TEST] GET /api/usuarios -> {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    # Verificar tipo de respuesta
    assert isinstance(data, dict)
    assert "data" in data  # response model incluye 'data'

# ==============================
# Ejecutar manualmente (opcional)
# ==============================
if __name__ == "__main__":
    print("="*60)
    print("PROBADOR DE ENDPOINTS")
    print("="*60)
    try:
        test_health()
        test_usuario_endpoints()
        print("\n✓ Todas las pruebas completadas correctamente")
    except Exception as e:
        print(f"\n✗ Error durante las pruebas: {e}")
