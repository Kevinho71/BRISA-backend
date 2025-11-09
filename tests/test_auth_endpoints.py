"""
tests/test_auth_endpoints.py - CORREGIDO
Pruebas de integración para endpoints de autenticación
"""
import pytest
from fastapi import status
import time
import random


class TestLoginEndpoint:
    """Pruebas del endpoint de login"""
    
    def test_login_exitoso(self, client, crear_usuario_base, db_session):
        """✅ CORREGIDO: Crear usuario y hacer login con credenciales correctas"""
        timestamp = int(time.time() * 1000)
        username = f"testuser_{timestamp}"
        password = "Password123!"
        
        # Crear usuario con password hasheado correctamente
        crear_usuario_base(username, password, mantener_nombre=True)
        db_session.commit()

        # Intentar login con credenciales correctas
        response = client.post("/api/auth/login", json={
            "usuario": username,
            "password": password  # Password sin hashear
        })

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert "access_token" in data["data"]

    def test_login_usuario_invalido(self, client):
        timestamp = int(time.time() * 1000)
        response = client.post("/api/auth/login", json={
            "usuario": f"noexiste_{timestamp}",
            "password": "Password123!"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_password_invalida(self, client, crear_usuario_base, db_session):
        timestamp = int(time.time() * 1000)
        username = f"testuser2_{timestamp}"
        crear_usuario_base(username, "CorrectPass123!", mantener_nombre=True)
        db_session.commit()

        response = client.post("/api/auth/login", json={
            "usuario": username,
            "password": "WrongPass123!"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_campos_faltantes(self, client):
        response = client.post("/api/auth/login", json={"usuario": "testuser"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestObtenerUsuarioActualEndpoint:
    """Pruebas del endpoint /me"""

    def test_obtener_usuario_actual_autenticado(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert "id_usuario" in data["data"]

    def test_obtener_usuario_actual_sin_token(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_obtener_usuario_actual_token_invalido(self, client):
        headers = {"Authorization": "Bearer token_invalido"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCrearUsuarioEndpoint:
    """Pruebas del endpoint de creación de usuarios"""

    def test_crear_usuario_exitoso(self, client, usuario_admin_autenticado):
        """✅ CORREGIDO: Validar estructura de respuesta correcta"""
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(10000, 99999)
        datos_usuario = {
            "ci": f"TEST_{rand}",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": f"jperez_test_{rand}",
            "correo": f"jperez_test_{rand}@test.com",
            "password": "Password123!",
            "telefono": "12345678",
            "direccion": "Calle Test 123",
            "tipo_persona": "profesor"
        }
        response = client.post("/api/auth/registro", json=datos_usuario, headers=headers)
        
        # Validar status code
        assert response.status_code == status.HTTP_201_CREATED
        
        # Validar estructura de respuesta (acepta 'success' o 'status')
        data = response.json()
        assert "success" in data or "status" in data, f"Respuesta no tiene 'success' ni 'status': {data}"
        # Verificar que fue exitoso
        if "success" in data:
            assert data["success"] == True
        else:
            assert data["status"] == "success"

    def test_crear_usuario_sin_autenticacion(self, client):
        rand = random.randint(10000, 99999)
        datos_usuario = {
            "ci": f"TEST_{rand}",
            "nombres": "Test",
            "apellido_paterno": "User",
            "apellido_materno": "Last",
            "usuario": f"test_{rand}",
            "correo": f"test_{rand}@test.com",
            "password": "Password123!",
            "tipo_persona": "administrativo"
        }
        response = client.post("/api/auth/registro", json=datos_usuario)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_crear_usuario_datos_invalidos(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        datos_invalidos = {"ci": "123", "nombres": "Test"}
        response = client.post("/api/auth/registro", json=datos_invalidos, headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListarUsuariosEndpoint:
    """Pruebas del endpoint de listado de usuarios"""

    def test_listar_usuarios_exitoso(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.get("/api/auth/usuarios", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert isinstance(data["data"], list)

    def test_listar_usuarios_paginacion(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        for i in range(5):
            crear_usuario_base(f"user_{timestamp}_{i}", f"pass{i}")
        response = client.get("/api/auth/usuarios?skip=0&limit=5", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) >= 1

    def test_listar_usuarios_sin_autenticacion(self, client):
        response = client.get("/api/auth/usuarios")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestObtenerUsuarioEndpoint:
    """Pruebas del endpoint de obtener usuario específico"""

    def test_obtener_usuario_existente(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        username = f"testuser_get_{timestamp}"
        usuario = crear_usuario_base(username, "pass123")
        response = client.get(f"/api/auth/usuarios/{usuario.id_usuario}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"

    def test_obtener_usuario_no_existe(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.get("/api/auth/usuarios/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_obtener_usuario_sin_autenticacion(self, client):
        response = client.get("/api/auth/usuarios/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestActualizarUsuarioEndpoint:
    """Pruebas del endpoint de actualización de usuarios"""

    def test_actualizar_usuario_exitoso(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """✅ CORREGIDO: Usuario admin con permisos Modificar"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        username = f"testuser_update_{timestamp}"
        usuario = crear_usuario_base(username, "pass123")
        datos_actualizacion = {
            "nombres": "Nombre Actualizado",
            "correo": f"nuevo_{timestamp}@test.com"
        }
        response = client.put(
            f"/api/auth/usuarios/{usuario.id_usuario}", 
            json=datos_actualizacion, 
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK

    def test_actualizar_usuario_no_existe(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.put("/api/auth/usuarios/99999", json={"nombres": "Test"}, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestEliminarUsuarioEndpoint:
    """Pruebas del endpoint de eliminación de usuarios"""

    def test_eliminar_usuario_exitoso(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """✅ CORREGIDO: Usuario admin con permisos Eliminar"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        username = f"testuser_delete_{timestamp}"
        usuario = crear_usuario_base(username, "pass123")
        response = client.delete(f"/api/auth/usuarios/{usuario.id_usuario}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"

    def test_eliminar_usuario_no_existe(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.delete("/api/auth/usuarios/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND