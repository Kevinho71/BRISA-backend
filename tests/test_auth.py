import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import SessionLocal

client = TestClient(app)

def test_registrar_usuario():
    """Test RF-01: Registrar usuario"""
    response = client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "jperez@example.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["usuario"] == "jperez"

def test_registrar_usuario_duplicado():
    """Test: Validar duplicados"""
    # Primer usuario
    client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "jperez@example.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
    )
    
    # Intentar usuario duplicado
    response = client.post(
        "/api/auth/register",
        json={
            "ci": "1234567891",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "otro@example.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
    )
    
    assert response.status_code == 400

def test_password_insegura():
    """Test: Validar complejidad de contraseña"""
    response = client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "jperez@example.com",
            "password": "123456",  # Muy simple
            "tipo_persona": "profesor"
        }
    )
    
    assert response.status_code in [400, 422]

def test_login_exitoso():
    """Test RF-05: Autenticación exitosa"""
    # Crear usuario
    client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "jperez@example.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
    )
    
    # Iniciar sesión
    response = client.post(
        "/api/auth/login",
        json={
            "usuario": "jperez",
            "password": "Password123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"

def test_login_incorrecto():
    """Test: Login con contraseña incorrecta"""
    # Crear usuario
    client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "jperez@example.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
    )
    
    # Intentar con contraseña incorrecta
    response = client.post(
        "/api/auth/login",
        json={
            "usuario": "jperez",
            "password": "IncorrectPassword!"
        }
    )
    
    assert response.status_code == 401

def test_obtener_usuario_actual():
    """Test: Obtener datos del usuario autenticado"""
    # Crear y autenticar usuario
    client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": "jperez",
            "correo": "jperez@example.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
    )
    
    login_response = client.post(
        "/api/auth/login",
        json={
            "usuario": "jperez",
            "password": "Password123!"
        }
    )
    
    token = login_response.json()["data"]["access_token"]
    
    # Obtener datos del usuario
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["usuario"] == "jperez"
