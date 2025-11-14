"""
tests/test_auth_endpoints.py -
Pruebas de integración para endpoints de autenticación
✅ Adaptado para usar ResponseModel con "success": True
✅ Todos los fixtures necesarios
"""
import pytest
from fastapi import status
import random
import time


class TestLoginEndpoint:
    """Pruebas del endpoint de login"""
    
    def test_login_exitoso(self, client, crear_usuario_base, db_session):
        """Login exitoso debe retornar token"""
        timestamp = int(time.time() * 1000)
        usuario_name = f"testuser_{timestamp}"
        password = "Password123!"
        
        # Crear usuario con nombre exacto
        usuario = crear_usuario_base(usuario_name, password, mantener_nombre=True)
        db_session.flush()
        
        # Login con datos exactos
        response = client.post("/api/auth/login", json={
            "usuario": usuario_name,
            "password": password
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] == True
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
    
    def test_login_usuario_invalido(self, client):
        """Login con usuario inexistente debe fallar"""
        timestamp = int(time.time() * 1000)
        response = client.post("/api/auth/login", json={
            "usuario": f"noexiste_{timestamp}",
            "password": "cualquier_password"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_password_invalida(self, client, crear_usuario_base, db_session):
        """Login con password incorrecta debe fallar"""
        timestamp = int(time.time() * 1000)
        usuario_name = f"testuser_pass_{timestamp}"
        
        usuario = crear_usuario_base(usuario_name, "Password123!", mantener_nombre=True)
        db_session.flush()
        
        response = client.post("/api/auth/login", json={
            "usuario": usuario_name,
            "password": "PasswordIncorrecta123!"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_campos_faltantes(self, client):
        """Login sin campos requeridos debe fallar"""
        response = client.post("/api/auth/login", json={"usuario": "test"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestObtenerUsuarioActualEndpoint:
    """Pruebas del endpoint /me"""
    
    def test_obtener_usuario_actual_autenticado(self, client, usuario_admin_autenticado):
        """Usuario autenticado debe poder obtener sus datos"""
        headers = usuario_admin_autenticado["headers"]
        
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "usuario" in data["data"]
    
    def test_obtener_usuario_actual_sin_token(self, client):
        """Sin token debe retornar 401"""
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_obtener_usuario_actual_token_invalido(self, client):
        """Token inválido debe retornar 401"""
        headers = {"Authorization": "Bearer token_invalido_xyz"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCrearUsuarioEndpoint:
    """Pruebas del endpoint de creación de usuarios"""
    
    def test_crear_usuario_exitoso(self, client, usuario_admin_autenticado, db_session):
        """Crear usuario con datos válidos debe retornar 201"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        datos_usuario = {
            "ci": f"987654{timestamp}",
            "nombres": "Nuevo",
            "apellido_paterno": "Usuario",
            "apellido_materno": "Test",
            "usuario": f"nuevousuario_{timestamp}",
            "correo": f"nuevo_{timestamp}@test.com",
            "password": "Password123!",
            "tipo_persona": "administrativo"
        }
        
        response = client.post("/api/auth/registro", json=datos_usuario, headers=headers)
        
        # Si falla, mostrar detalles
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Error: {response.json()}")
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] == True
        assert "data" in data
    
    def test_crear_usuario_sin_autenticacion(self, client):
        """Crear usuario sin autenticación debe retornar 401"""
        timestamp = int(time.time() * 1000)
        datos_usuario = {
            "ci": f"123456{timestamp}",
            "nombres": "Test",
            "apellido_paterno": "User",
            "apellido_materno": "Last",
            "usuario": f"testuser_{timestamp}",
            "correo": f"test_{timestamp}@test.com",
            "password": "Password123!",
            "tipo_persona": "administrativo"
        }
        
        response = client.post("/api/auth/registro", json=datos_usuario)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_crear_usuario_datos_invalidos(self, client, usuario_admin_autenticado):
        """Crear usuario con datos inválidos debe retornar 422"""
        headers = usuario_admin_autenticado["headers"]
        
        # Password sin mayúsculas
        datos_invalidos = {
            "ci": "123",
            "nombres": "Test",
            "apellido_paterno": "User",
            "apellido_materno": "Last",
            "usuario": "test",
            "correo": "test@test.com",
            "password": "password123!", 
            "tipo_persona": "administrativo"
        }
        
        response = client.post("/api/auth/registro", json=datos_invalidos, headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListarUsuariosEndpoint:
    """Pruebas del endpoint de listado de usuarios"""
    
    def test_listar_usuarios_exitoso(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Listar usuarios debe retornar lista"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        crear_usuario_base(f"user1_{timestamp}", "pass123")
        crear_usuario_base(f"user2_{timestamp}", "pass123")
        db_session.flush()
        
        response = client.get("/api/auth/usuarios", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] == True
        assert isinstance(data["data"], list)
    
    def test_listar_usuarios_paginacion(self, client, usuario_admin_autenticado):
        """Paginación debe funcionar correctamente"""
        headers = usuario_admin_autenticado["headers"]
        
        response = client.get("/api/auth/usuarios?skip=0&limit=5", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) <= 5
    
    def test_listar_usuarios_sin_autenticacion(self, client):
        """Listar usuarios sin autenticación debe retornar 401"""
        response = client.get("/api/auth/usuarios")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestObtenerUsuarioEndpoint:
    """Pruebas del endpoint de obtener usuario específico"""
    
    def test_obtener_usuario_existente(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Obtener usuario existente debe retornar sus datos"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        usuario = crear_usuario_base(f"testuser_{timestamp}", "pass123")
        db_session.flush()
        
        response = client.get(f"/api/auth/usuarios/{usuario.id_usuario}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] == True
        assert data["data"]["id_usuario"] == usuario.id_usuario
    
    def test_obtener_usuario_no_existe(self, client, usuario_admin_autenticado):
        """Obtener usuario inexistente debe retornar 404"""
        headers = usuario_admin_autenticado["headers"]
        
        response = client.get("/api/auth/usuarios/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_obtener_usuario_sin_autenticacion(self, client):
        """Obtener usuario sin autenticación debe retornar 401"""
        response = client.get("/api/auth/usuarios/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestActualizarUsuarioEndpoint:
    """Pruebas del endpoint de actualización de usuarios"""
    
    def test_actualizar_usuario_exitoso(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Actualizar usuario debe funcionar correctamente"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        # Crear usuario a actualizar
        usuario = crear_usuario_base(f"testuser_{timestamp}", "pass123")
        db_session.flush()
        
        # Datos de actualización con correo ÚNICO
        datos_actualizacion = {
            "correo": f"actualizado_{timestamp}@test.com",  # Correo único
            "usuario": f"actualizado_{timestamp}"
        }
        
        response = client.put(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            json=datos_actualizacion,
            headers=headers
        )
        
        # Debug si falla
        if response.status_code != status.HTTP_200_OK:
            print(f"Error: {response.json()}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] == True
    
    def test_actualizar_usuario_no_existe(self, client, usuario_admin_autenticado):
        """Actualizar usuario inexistente debe retornar 404"""
        headers = usuario_admin_autenticado["headers"]
        
        datos_actualizacion = {"correo": "nuevo@test.com"}
        
        response = client.put(
            "/api/auth/usuarios/99999",
            json=datos_actualizacion,
            headers=headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestEliminarUsuarioEndpoint:
    """Pruebas del endpoint de eliminación de usuarios"""
    
    def test_eliminar_usuario_exitoso(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Eliminar usuario debe funcionar correctamente"""
        headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        usuario = crear_usuario_base(f"testuser_{timestamp}", "pass123")
        db_session.flush()
        
        response = client.delete(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] == True
    
    def test_eliminar_usuario_no_existe(self, client, usuario_admin_autenticado):
        """Eliminar usuario inexistente debe retornar 404"""
        headers = usuario_admin_autenticado["headers"]
        
        response = client.delete("/api/auth/usuarios/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND