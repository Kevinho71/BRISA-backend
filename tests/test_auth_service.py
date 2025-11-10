"""
tests/test_auth_service.py - COMPLETAMENTE CORREGIDO
Pruebas unitarias para AuthService
"""
import pytest
from datetime import timedelta
import random
import time

from fastapi import HTTPException

from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.dto.auth_dto import RegistroDTO, LoginDTO, TokenDTO
from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.exceptions import Unauthorized
from app.shared.security import hash_password, ACCESS_TOKEN_EXPIRE_MINUTES


class TestAuthServicePasswordHashing:
    """Pruebas de hasheo y verificación de contraseñas"""
    
    def test_hash_password_genera_hash_diferente(self):
        password = "Password123!"
        hashed = AuthService.hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password_correcto(self):
        password = "Password123!"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed)
    
    def test_verify_password_incorrecto(self):
        password = "Password123!"
        wrong_password = "WrongPass456!"
        hashed = AuthService.hash_password(password)
        assert not AuthService.verify_password(wrong_password, hashed)
    
    def test_hash_diferentes_para_misma_password(self):
        password = "Password123!"
        hash1 = AuthService.hash_password(password)
        hash2 = AuthService.hash_password(password)
        assert hash1 != hash2
        assert AuthService.verify_password(password, hash1)
        assert AuthService.verify_password(password, hash2)


class TestAuthServiceJWT:
    """Pruebas de creación y decodificación de tokens JWT"""
    
    def test_create_access_token_contiene_datos(self):
        data = {"usuario_id": 1, "usuario": "testuser"}
        token = AuthService.create_access_token(data)
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    def test_decode_token_valido(self):
        data = {"usuario_id": 1, "usuario": "testuser"}
        token = AuthService.create_access_token(data)
        decoded = AuthService.decode_token(token)
        assert decoded["usuario_id"] == 1
        assert decoded["usuario"] == "testuser"
    
    def test_decode_token_invalido(self):
        invalid_token = "token.invalido.aqui"
        with pytest.raises(Unauthorized):
            AuthService.decode_token(invalid_token)
    
    def test_token_con_expiracion_personalizada(self):
        data = {"usuario_id": 1}
        expires_delta = timedelta(minutes=5)
        token = AuthService.create_access_token(data, expires_delta)
        decoded = AuthService.decode_token(token)
        assert "exp" in decoded
        assert decoded["usuario_id"] == 1


class TestAuthServiceRegistro:
    """Pruebas de registro de usuarios"""
    
    def test_registrar_usuario_exitoso(self, db_session):
        rand = random.randint(10000, 99999)
        registro_dto = RegistroDTO(
            ci=f"123456{rand}",
            nombres="Test",
            apellido_paterno="User",
            apellido_materno="Last",
            usuario=f"testuser{rand}",
            correo=f"test{rand}@test.com",
            password="Password123!",
            tipo_persona="administrativo"
        )
        resultado = AuthService.registrar_usuario(db_session, registro_dto)
        assert resultado["usuario"] == f"testuser{rand}"
        assert resultado["correo"] == f"test{rand}@test.com"
        assert "id_usuario" in resultado
        assert "mensaje" in resultado
        
        usuario = db_session.query(Usuario).filter(Usuario.usuario == f"testuser{rand}").first()
        assert usuario is not None
        assert usuario.is_active
    
    def test_registrar_usuario_duplicado_usuario(self, db_session, crear_usuario_base):
        """
        Debe fallar al intentar registrar un usuario con un nombre de usuario
        que ya existe en la base de datos.
        """
        import time

        timestamp = int(time.time() * 1000)
        usuario_name = f"testuser_dup_{timestamp}"

        # Crear usuario exacto en la DB (sin sufijos aleatorios)
        usuario_existente = crear_usuario_base(usuario_name, "Password123!", mantener_nombre=True)

        # Intentar crear otro usuario con el MISMO nombre
        registro_dto = RegistroDTO(
            ci=f"9999999{timestamp}",
            nombres="Another",
            apellido_paterno="User",
            apellido_materno="Last",
            usuario=usuario_name,  # mismo nombre exacto
            correo=f"another{timestamp}@test.com",
            password="Password123!",
            tipo_persona="administrativo"
        )

        with pytest.raises(HTTPException) as exc_info:
            AuthService.registrar_usuario(db_session, registro_dto)

        # Verificar que lanza error 400
        assert exc_info.value.status_code == 400

        
    def test_registrar_usuario_ci_duplicado(self, db_session, crear_persona_base):
        rand = random.randint(10000, 99999)
        ci_unico = f"1234567{rand}"
        crear_persona_base(ci_unico, "Existing")
        registro_dto = RegistroDTO(
            ci=ci_unico,
            nombres="New",
            apellido_paterno="User",
            apellido_materno="Last",
            usuario=f"newuser{rand}",
            correo=f"new{rand}@test.com",
            password="Password123!",
            tipo_persona="administrativo"
        )
        with pytest.raises(HTTPException) as exc_info:
            AuthService.registrar_usuario(db_session, registro_dto)
        assert exc_info.value.status_code == 400


class TestAuthServiceLogin:
    """Pruebas de inicio de sesión"""
    
    def test_login_exitoso(self, db_session, crear_usuario_base):
        """
        Debe iniciar sesión correctamente y devolver un token válido.
        """
        import time

        timestamp = int(time.time() * 1000)
        usuario_name = f"testuser_login_{timestamp}"

        # Crear usuario exacto en la DB
        usuario_login = crear_usuario_base(usuario_name, "password123", mantener_nombre=True)

        # Login con los mismos datos
        login_dto = LoginDTO(usuario=usuario_name, password="password123")
        token_dto = AuthService.login(db_session, login_dto)

        # Validar que se devuelve el token
        assert token_dto.access_token is not None
        assert token_dto.token_type == "bearer"
        assert token_dto.usuario_id == usuario_login.id_usuario
        assert token_dto.usuario == usuario_name

    def test_login_usuario_no_existe(self, db_session):
        timestamp = int(time.time() * 1000)
        login_dto = LoginDTO(usuario=f"noexiste_{timestamp}", password="password123")
        with pytest.raises(Unauthorized):
            AuthService.login(db_session, login_dto)
    
    def test_login_password_incorrecta(self, db_session, crear_usuario_base):
        timestamp = int(time.time() * 1000)
        usuario_name = f"testuser_pass_{timestamp}"
        crear_usuario_base(usuario_name, "correctpassword")
        login_dto = LoginDTO(usuario=usuario_name, password="wrongpassword")
        with pytest.raises(Unauthorized):
            AuthService.login(db_session, login_dto)


class TestAuthServiceObtenerUsuarioActual:
    """Pruebas de obtención de usuario actual"""
    
    def test_obtener_usuario_actual_exitoso(self, db_session, usuario_admin_autenticado):
        usuario_data = usuario_admin_autenticado["usuario"]
        usuario_actual = AuthService.obtener_usuario_actual(db_session, usuario_data.id_usuario)
        assert usuario_actual.id_usuario == usuario_data.id_usuario
        assert usuario_actual.usuario == usuario_data.usuario
        assert isinstance(usuario_actual.roles, list)
        assert isinstance(usuario_actual.permisos, list)
    
    def test_obtener_usuario_actual_no_existe(self, db_session):
        with pytest.raises(HTTPException) as exc_info:
            AuthService.obtener_usuario_actual(db_session, 99999)
        assert exc_info.value.status_code == 404
