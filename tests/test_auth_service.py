"""
tests/test_auth_service.py - CORREGIDO CON NOMBRES ÚNICOS
Pruebas unitarias para AuthService
"""
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
import random
import time

from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.dto.auth_dto import RegistroDTO, LoginDTO
from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.exceptions import Unauthorized


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
        assert AuthService.verify_password(password, hashed) is True
    
    def test_verify_password_incorrecto(self):
        password = "Password123!"
        wrong_password = "WrongPass456!"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(wrong_password, hashed) is False
    
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
        data = {"sub": 1, "usuario": "testuser"}
        token = AuthService.create_access_token(data)
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    def test_decode_token_valido(self):
        """CORREGIDO: Tu auth_service convierte sub a string"""
        data = {"sub": 1, "usuario": "testuser"}
        token = AuthService.create_access_token(data)
        decoded = AuthService.decode_token(token)
        
        # Tu AuthService convierte sub a string
        assert decoded["sub"] == "1"
        assert decoded["usuario"] == "testuser"
        assert "usuario_id" in decoded
        assert decoded["usuario_id"] == 1
    
    def test_decode_token_invalido(self):
        invalid_token = "token.invalido.aqui"
        with pytest.raises(Unauthorized):
            AuthService.decode_token(invalid_token)
    
    def test_token_con_expiracion_personalizada(self):
        """CORREGIDO: Verificar expiración del token"""
        data = {"sub": 1}
        expires_delta = timedelta(minutes=5)
        
        # Crear token
        token = AuthService.create_access_token(data, expires_delta)
        decoded = AuthService.decode_token(token)
        
        # Verificar que tiene campo exp
        assert "exp" in decoded
        
        # Verificar que usuario_id está correcto
        assert decoded["usuario_id"] == 1
        assert decoded["sub"] == "1"


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
        assert usuario.is_active is True
    
    def test_registrar_usuario_duplicado_usuario(self, db_session, crear_usuario_base):
        rand = random.randint(10000, 99999)
        usuario_name = f"testuser_dup_{rand}"
        crear_usuario_base(usuario_name, "pass123")
        
        registro_dto = RegistroDTO(
            ci=f"9999999{rand}",
            nombres="Another",
            apellido_paterno="User",
            apellido_materno="Last",
            usuario=usuario_name,
            correo=f"another{rand}@test.com",
            password="Password123!",
            tipo_persona="administrativo"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.registrar_usuario(db_session, registro_dto)
        
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
        # SOLUCIÓN: Usar timestamp para nombres únicos
        timestamp = int(time.time() * 1000)  # milisegundos
        usuario_name = f"testuser_login_{timestamp}"
        
        crear_usuario_base(usuario_name, "password123")
        login_dto = LoginDTO(usuario=usuario_name, password="password123")
        token_dto = AuthService.login(db_session, login_dto)
        
        assert token_dto.access_token is not None
        assert token_dto.token_type == "bearer"
        assert token_dto.usuario_id > 0
        assert token_dto.usuario == usuario_name
    
    def test_login_usuario_no_existe(self, db_session):
        timestamp = int(time.time() * 1000)
        login_dto = LoginDTO(usuario=f"noexiste_{timestamp}", password="password123")
        with pytest.raises(Unauthorized):
            AuthService.login(db_session, login_dto)
    
    def test_login_password_incorrecta(self, db_session, crear_usuario_base):
        # SOLUCIÓN: Usar timestamp para nombres únicos
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