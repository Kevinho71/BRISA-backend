"""
tests/test_integration.py  
Pruebas de integración end-to-end

"""
import pytest
from fastapi import status
import random
import time


class TestFlujoRegistroLoginCompleto:
    """Prueba del flujo completo: Registro → Login → Acceso a recursos"""
    
    def test_flujo_registro_y_login_exitoso(self, client, usuario_admin_autenticado, db_session):
        """
        Flujo completo:
        1. Admin registra nuevo usuario
        2. Usuario hace login
        3. Usuario accede a sus datos con el token
        """
        admin_headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        # Paso 1: Registrar usuario
        datos_registro = {
            "ci": f"111222{timestamp}",
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "García",
            "usuario": f"juanperez_{timestamp}",
            "correo": f"juan.perez_{timestamp}@test.com",
            "password": "Password123!",
            "tipo_persona": "administrativo"
        }
        
        response_registro = client.post(
            "/api/auth/registro",
            json=datos_registro,
            headers=admin_headers
        )
        assert response_registro.status_code == status.HTTP_201_CREATED
        assert response_registro.json()["success"] == True
        
        # Paso 2: Login con el nuevo usuario
        response_login = client.post("/api/auth/login", json={
            "usuario": datos_registro["usuario"],
            "password": datos_registro["password"]
        })
        assert response_login.status_code == status.HTTP_200_OK
        login_data = response_login.json()
        assert login_data["success"] == True
        assert "access_token" in login_data["data"]
        
        # Paso 3: Acceder a /me con el token
        user_token = login_data["data"]["access_token"]
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        response_me = client.get("/api/auth/me", headers=user_headers)
        assert response_me.status_code == status.HTTP_200_OK
        me_data = response_me.json()
        assert me_data["success"] == True
        assert me_data["data"]["usuario"] == datos_registro["usuario"]


class TestFlujoGestionRolesPermisos:
    """Prueba del flujo completo de gestión de roles y permisos"""
    
    def test_flujo_completo_roles_y_permisos(self, client, usuario_admin_autenticado, crear_permiso_base, db_session):
        """
        Flujo completo:
        1. Admin crea un nuevo rol
        2. Admin asigna permisos al rol
        3. Admin crea un usuario (el endpoint crea la persona automáticamente)
        4. Admin asigna el rol al usuario
        5. Verifica que el usuario tiene los permisos
        """
        admin_headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        # Paso 1: Crear rol
        datos_rol = {
            "nombre": f"Profesor_{timestamp}",
            "descripcion": "Rol para profesores"
        }
        response_rol = client.post("/api/auth/roles", json=datos_rol, headers=admin_headers)
        assert response_rol.status_code == status.HTTP_201_CREATED
        rol_data = response_rol.json()
        assert rol_data["success"] == True
        id_rol = rol_data["data"]["id_rol"]
        
        # Paso 2: Crear permisos
        perm1 = crear_permiso_base(f"ver_calificaciones_{timestamp}", "calificaciones", "Ver calificaciones")
        perm2 = crear_permiso_base(f"editar_calificaciones_{timestamp}", "calificaciones", "Editar calificaciones")
        db_session.flush()
        
        # Asignar permisos al rol
        response_permisos = client.post(
            f"/api/auth/roles/{id_rol}/permisos",
            json=[perm1.id_permiso, perm2.id_permiso],
            headers=admin_headers
        )
        assert response_permisos.status_code == status.HTTP_200_OK
        
        # Paso 3: Crear usuario (el endpoint registrar_usuario crea la persona automáticamente)
        ci_unico = f"333444{timestamp}"
        datos_usuario = {
            "ci": ci_unico,
            "nombres": "María",
            "apellido_paterno": "López",
            "apellido_materno": "Gómez",
            "usuario": f"marialopez_{timestamp}",
            "correo": f"maria.lopez_{timestamp}@test.com",
            "password": "Password123!",
            "tipo_persona": "profesor"
        }
        response_usuario = client.post(
            "/api/auth/registro",
            json=datos_usuario,
            headers=admin_headers
        )
        
        # Debug si falla
        if response_usuario.status_code != status.HTTP_201_CREATED:
            print(f"Error al crear usuario: {response_usuario.json()}")
        
        assert response_usuario.status_code == status.HTTP_201_CREATED
        usuario_data = response_usuario.json()
        id_usuario = usuario_data["data"]["id_usuario"]
        
        # Paso 4: Asignar rol al usuario
        response_asignar = client.post(
            f"/api/auth/usuarios/{id_usuario}/roles/{id_rol}",
            headers=admin_headers
        )
        assert response_asignar.status_code == status.HTTP_200_OK
        
        # Paso 5: Verificar que el usuario tiene el rol
        response_usuario_detail = client.get(
            f"/api/auth/usuarios/{id_usuario}",
            headers=admin_headers
        )
        assert response_usuario_detail.status_code == status.HTTP_200_OK




class TestFlujoActualizacionUsuario:
    """Prueba del flujo de actualización de datos de usuario"""
    
    def test_flujo_actualizacion_datos_usuario(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """
        Flujo completo:
        1. Admin crea usuario
        2. Admin actualiza datos del usuario
        3. Verifica que los cambios se aplicaron
        """
        admin_headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        # Paso 1: Crear usuario
        usuario = crear_usuario_base(f"testuser_{timestamp}", "Password123!")
        db_session.flush()
        
        # Paso 2: Actualizar datos
        datos_actualizacion = {
            "correo": f"nuevo.correo_{timestamp}@test.com",
            "usuario": f"usuario_actualizado_{timestamp}"
        }
        
        response_actualizar = client.put(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            json=datos_actualizacion,
            headers=admin_headers
        )
        assert response_actualizar.status_code == status.HTTP_200_OK
        
        # Paso 3: Verificar cambios
        response_verificar = client.get(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=admin_headers
        )
        assert response_verificar.status_code == status.HTTP_200_OK
        usuario_data = response_verificar.json()["data"]
        assert usuario_data["correo"] == datos_actualizacion["correo"]


class TestFlujoEliminacionUsuario:
    """Prueba del flujo de eliminación de usuario"""
    
    def test_flujo_eliminacion_usuario(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """
        Flujo completo:
        1. Admin crea usuario
        2. Admin elimina usuario
        3. Verifica que el usuario fue eliminado (borrado lógico)
        """
        admin_headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        # Paso 1: Crear usuario
        usuario = crear_usuario_base(f"testuser_{timestamp}", "Password123!")
        db_session.flush()
        id_usuario = usuario.id_usuario
        
        # Paso 2: Eliminar usuario
        response_eliminar = client.delete(
            f"/api/auth/usuarios/{id_usuario}",
            headers=admin_headers
        )
        assert response_eliminar.status_code == status.HTTP_200_OK
        
        # Paso 3: Verificar que ya no se puede acceder
        response_verificar = client.get(
            f"/api/auth/usuarios/{id_usuario}",
            headers=admin_headers
        )
        assert response_verificar.status_code == status.HTTP_404_NOT_FOUND


class TestFlujoSeguridadTokens:
    """Pruebas de seguridad con tokens"""
    
    def test_token_invalido_no_permite_acceso(self, client):
        """Token inválido debe ser rechazado"""
        headers = {"Authorization": "Bearer token_completamente_invalido_xyz"}
        
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_sin_token_no_permite_acceso(self, client):
        """
        ✅ Sin token debe retornar 401 (Unauthorized), no 403
        403 es para cuando estás autenticado pero no tienes permisos
        401 es para cuando NO estás autenticado
        """
        response = client.get("/api/auth/usuarios")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_expirado_no_permite_acceso(self, client):
        """Token expirado debe ser rechazado"""
        # Token expirado de prueba (este es un ejemplo, en realidad necesitarías generar uno expirado)
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}
        
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestSmokeTests:
    """Tests básicos de sanidad del sistema"""
    
    def test_health_check_auth_endpoints(self, client):
        """Verificar que los endpoints de autenticación están disponibles"""
        # Login endpoint debe estar disponible (sin autenticación)
        response = client.post("/api/auth/login", json={
            "usuario": "cualquiera",
            "password": "cualquiera"
        })
        # Debe retornar 401 (credenciales incorrectas), no 404 (endpoint no existe)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_422_UNPROCESSABLE_ENTITY]
    
    def test_database_connection(self, db_session):
        """Verificar que la conexión a la base de datos funciona"""
        from app.modules.usuarios.models.usuario_models import Usuario
        
        # Consulta simple para verificar conexión
        result = db_session.query(Usuario).first()
        assert db_session is not None
    
    def test_jwt_service_available(self):
        """Verificar que el servicio JWT está disponible"""
        from app.modules.auth.services.auth_service import AuthService
        
        # Crear un token de prueba
        token = AuthService.create_access_token(data={"sub": 1})
        assert token is not None
        assert len(token) > 0
        
        # Decodificar el token
        decoded = AuthService.decode_token(token)
        
        # JWT puede convertir int a string
        # Verificar que sea 1 como int o "1" como string
        assert decoded["sub"] == 1 or decoded["sub"] == "1"

class TestFlujoPermisosDenegados:
    """Pruebas de flujos donde permisos deben ser denegados"""
    
    def test_usuario_sin_permisos_no_puede_crear_roles(self, client, usuario_simple_autenticado):
        """Usuario sin permisos no puede crear roles"""
        headers = usuario_simple_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        datos_rol = {
            "nombre": f"RolNuevo_{timestamp}",
            "descripcion": "Intento de crear rol sin permisos"
        }
        
        response = client.post("/api/auth/roles", json=datos_rol, headers=headers)
        # Debe ser rechazado por falta de permisos
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
    
    def test_usuario_sin_permisos_no_puede_eliminar_usuarios(self, client, usuario_simple_autenticado, crear_usuario_base, db_session):
        """Usuario sin permisos no puede eliminar otros usuarios"""
        headers = usuario_simple_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        # Crear usuario a eliminar
        usuario = crear_usuario_base(f"testuser_{timestamp}", "Password123!")
        db_session.flush()
        
        response = client.delete(
            f"/api/auth/usuarios/{usuario.id_usuario}",
            headers=headers
        )
        # Debe ser rechazado por falta de permisos
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]


class TestFlujoValidacionDatos:
    """Pruebas de validación de datos de entrada"""
    
    def test_registro_con_password_debil_falla(self, client, usuario_admin_autenticado):
        """Registro con password débil debe ser rechazado"""
        admin_headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        datos_registro = {
            "ci": f"555666{timestamp}",
            "nombres": "Test",
            "apellido_paterno": "User",
            "apellido_materno": "Last",
            "usuario": f"testuser_{timestamp}",
            "correo": f"test_{timestamp}@test.com",
            "password": "123",  # Password muy débil
            "tipo_persona": "administrativo"
        }
        
        response = client.post(
            "/api/auth/registro",
            json=datos_registro,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_registro_con_email_invalido_falla(self, client, usuario_admin_autenticado):
        """Registro con email inválido debe ser rechazado"""
        admin_headers = usuario_admin_autenticado["headers"]
        timestamp = int(time.time() * 1000)
        
        datos_registro = {
            "ci": f"777888{timestamp}",
            "nombres": "Test",
            "apellido_paterno": "User",
            "apellido_materno": "Last",
            "usuario": f"testuser_{timestamp}",
            "correo": "email_invalido",  # Email sin formato correcto
            "password": "Password123!",
            "tipo_persona": "administrativo"
        }
        
        response = client.post(
            "/api/auth/registro",
            json=datos_registro,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY