import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def token():
    """Crear token de autenticación"""
    # Registrar
    client.post(
        "/api/auth/register",
        json={
            "ci": "1234567890",
            "nombres": "Admin",
            "apellido_paterno": "Usuario",
            "apellido_materno": "Test",
            "usuario": "admin",
            "correo": "admin@example.com",
            "password": "Password123!",
            "tipo_persona": "administrativo"
        }
    )
    
    # Autenticar
    response = client.post(
        "/api/auth/login",
        json={
            "usuario": "admin",
            "password": "Password123!"
        }
    )
    
    return response.json()["data"]["access_token"]

def test_listar_usuarios(token):
    """Test: Listar usuarios"""
    response = client.get(
        "/api/usuarios",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)

def test_obtener_usuario(token):
    """Test: Obtener usuario específico"""
    # Primero obtener lista para conseguir un ID
    list_response = client.get(
        "/api/usuarios",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    users = list_response.json()["data"]
    if users:
        user_id = users[0]["id_usuario"]
        
        response = client.get(
            f"/api/usuarios/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id_usuario"] == user_id

def test_crear_usuario(token):
    """Test RF-01: Crear usuario"""
    response = client.post(
        "/api/usuarios",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "ci": "9876543210",
            "nombres": "Carlos",
            "apellido_paterno": "López",
            "apellido_materno": "Martínez",
            "usuario": "clopez",
            "correo": "clopez@example.com",
            "password": "Password456!",
            "tipo_persona": "profesor"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["usuario"] == "clopez"

def test_listar_roles(token):
    """Test: Listar roles"""
    response = client.get(
        "/api/usuarios/roles",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_listar_permisos(token):
    """Test: Listar permisos"""
    response = client.get(
        "/api/usuarios/permisos",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
