"""
tests/test_integration.py - CORREGIDO
Pruebas de integración de flujos completos
"""
import pytest
from fastapi import status
import random
from sqlalchemy import text


class TestFlujoRegistroLoginCompleto:
    """Pruebas de flujo completo: registro -> login"""
    
    def test_flujo_registro_y_login_exitoso(self, client, usuario_admin_autenticado, db_session):
        """Flujo: Crear usuario -> Login -> Verificar acceso"""
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(10000, 99999)
        
        # 1. Registrar nuevo usuario
        password_test = "Password123!"
        datos_registro = {
            "ci": f"TEST_{rand}",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": f"jperez_{rand}",
            "correo": f"jperez_{rand}@test.com",
            "password": password_test,
            "telefono": "12345678",
            "direccion": "Calle Test",
            "tipo_persona": "profesor"
        }
        
        response = client.post("/api/auth/registro", json=datos_registro, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        
        # 2. Login con el nuevo usuario - USAR PASSWORD ORIGINAL, NO HASHEADO
        response_login = client.post("/api/auth/login", json={
            "usuario": datos_registro["usuario"],
            "password": password_test  # Usar el password original
        })
        
        # Debug: ver qué responde el login
        if response_login.status_code != status.HTTP_200_OK:
            print(f"Login failed: {response_login.json()}")
        
        assert response_login.status_code == status.HTTP_200_OK
        login_data = response_login.json()
        assert "access_token" in login_data["data"]
        
        # 3. Verificar acceso con el token
        new_headers = {"Authorization": f"Bearer {login_data['data']['access_token']}"}
        response_me = client.get("/api/auth/me", headers=new_headers)
        assert response_me.status_code == status.HTTP_200_OK


class TestFlujoGestionRolesPermisos:
    """Pruebas de flujo: crear rol -> asignar permisos -> asignar a usuario"""
    
    def test_flujo_completo_roles_y_permisos(self, client, usuario_admin_autenticado, crear_usuario_base, crear_permiso_base, db_session):
        """Flujo: Crear rol -> Asignar permisos -> Asignar a usuario"""
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(10000, 99999)
        
        # 1. Crear rol
        datos_rol = {
            "nombre": f"Editor_{rand}",
            "descripcion": "Rol de editor de contenido"
        }
        response_rol = client.post("/api/auth/roles", json=datos_rol, headers=headers)
        assert response_rol.status_code == status.HTTP_201_CREATED
        
        rol_data = response_rol.json()
        id_rol = rol_data["data"]["id"]
        
        # 2. Crear permisos
        perm1 = crear_permiso_base(f"crear_contenido_{rand}", "contenido", "Crear contenido")
        perm2 = crear_permiso_base(f"editar_contenido_{rand}", "contenido", "Editar contenido")
        
        # 3. Asignar permisos al rol
        response_permisos = client.post(
            f"/api/auth/roles/{id_rol}/permisos",
            json=[perm1.id_permiso, perm2.id_permiso],
            headers=headers
        )
        assert response_permisos.status_code == status.HTTP_200_OK
        
        # 4. Crear usuario
        usuario = crear_usuario_base(f"editor_{rand}", "pass123")
        
        # 5. Asignar rol al usuario
        response_asignar = client.post(
            f"/api/auth/usuarios/{usuario.id_usuario}/roles/{id_rol}",
            headers=headers
        )
        assert response_asignar.status_code == status.HTTP_200_OK
        
        # 6. Verificar que el usuario tiene el rol
        response_usuario = client.get(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=headers
        )
        assert response_usuario.status_code == status.HTTP_200_OK


class TestFlujoActualizacionUsuario:
    """Pruebas de flujo: crear -> actualizar -> verificar"""
    
    def test_flujo_actualizacion_datos_usuario(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Flujo: Crear usuario -> Actualizar datos -> Verificar cambios"""
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(10000, 99999)
        
        # 1. Crear usuario
        usuario = crear_usuario_base(f"testuser_{rand}", "pass123")
        
        # 2. Actualizar usuario
        datos_actualizacion = {
            "nombres": "Nombre Actualizado",
            "correo": f"actualizado_{rand}@test.com"
        }
        response_update = client.put(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            json=datos_actualizacion,
            headers=headers
        )
        assert response_update.status_code == status.HTTP_200_OK
        
        # 3. Verificar actualización
        response_get = client.get(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=headers
        )
        assert response_get.status_code == status.HTTP_200_OK
        usuario_data = response_get.json()
        assert usuario_data["data"]["correo"] == datos_actualizacion["correo"]


class TestFlujoEliminacionUsuario:
    """Pruebas de flujo: crear -> eliminar -> verificar"""
    
    def test_flujo_eliminacion_usuario(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Flujo: Crear usuario -> Eliminar -> Verificar no está activo"""
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(10000, 99999)
        
        # 1. Crear usuario
        usuario = crear_usuario_base(f"testuser_{rand}", "pass123")
        
        # 2. Eliminar usuario
        response_delete = client.delete(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=headers
        )
        assert response_delete.status_code == status.HTTP_200_OK
        
        # 3. Verificar que no se puede obtener (borrado lógico)
        response_get = client.get(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=headers
        )
        # Usuario eliminado (is_active=False) debería retornar 404
        assert response_get.status_code == status.HTTP_404_NOT_FOUND


class TestFlujoSeguridadTokens:
    """Pruebas de seguridad con tokens"""
    
    def test_token_invalido_no_permite_acceso(self, client):
        """Token inválido debe rechazar acceso"""
        headers = {"Authorization": "Bearer token_invalido_12345"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_sin_token_no_permite_acceso(self, client):
        """Sin token debe rechazar acceso"""
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestSmokeTests:
    """Pruebas básicas de funcionamiento"""
    
    def test_health_check_auth_endpoints(self, client):
        """Verificar que los endpoints de auth están disponibles"""
        # Root endpoint
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        
        # Health check
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
    
    def test_database_connection(self, db_session):
        """Verificar conexión a base de datos"""
        assert db_session is not None
        # CORREGIDO: Usar text() para SQL raw
        from sqlalchemy import text
        result = db_session.execute(text("SELECT 1"))
        assert result is not None
    
    def test_jwt_service_available(self):
        """Verificar que el servicio JWT está disponible"""
        # CORREGIDO: Usar AuthService en lugar de shared.security
        from app.modules.auth.services.auth_service import AuthService
        
        # Crear token
        token = AuthService.create_access_token({"sub": 1, "usuario": "test"})
        assert token is not None
        assert isinstance(token, str)
        
        # Verificar token
        payload = AuthService.decode_token(token)
        assert payload["usuario_id"] == 1
        assert payload["usuario"] == "test"