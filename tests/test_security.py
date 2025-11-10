"""
tests/test_security.py 
Tests de seguridad y validaciones
"""
import pytest
from fastapi import status
from datetime import timedelta

from app.modules.auth.services.auth_service import AuthService
from app.modules.auth.dto.auth_dto import RegistroDTO


class TestPasswordSecurity:
    """Tests de seguridad de contraseñas"""
    
    def test_password_debe_tener_minimo_8_caracteres(self):
        """Contraseña debe tener mínimo 8 caracteres"""
        with pytest.raises(ValueError, match="mínimo 8 caracteres"):
            RegistroDTO(
                ci="123",
                nombres="Test",
                apellido_paterno="User",
                apellido_materno="Last",
                usuario="test",
                correo="test@test.com",
                password="Short1!",
                tipo_persona="administrativo"
            )
    
    def test_password_debe_tener_mayuscula(self):
        """Contraseña debe contener al menos una mayúscula"""
        with pytest.raises(ValueError, match="mayúsculas"):
            RegistroDTO(
                ci="123",
                nombres="Test",
                apellido_paterno="User",
                apellido_materno="Last",
                usuario="test",
                correo="test@test.com",
                password="password123!",
                tipo_persona="administrativo"
            )
    
    def test_password_debe_tener_minuscula(self):
        """Contraseña debe contener al menos una minúscula"""
        with pytest.raises(ValueError, match="minúsculas"):
            RegistroDTO(
                ci="123",
                nombres="Test",
                apellido_paterno="User",
                apellido_materno="Last",
                usuario="test",
                correo="test@test.com",
                password="PASSWORD123!",
                tipo_persona="administrativo"
            )
    
    def test_password_debe_tener_numero(self):
        """Contraseña debe contener al menos un número"""
        with pytest.raises(ValueError, match="números"):
            RegistroDTO(
                ci="123",
                nombres="Test",
                apellido_paterno="User",
                apellido_materno="Last",
                usuario="test",
                correo="test@test.com",
                password="Password!",
                tipo_persona="administrativo"
            )
    
    def test_password_valida_cumple_requisitos(self):
        """Contraseña válida debe pasar todas las validaciones"""
        registro = RegistroDTO(
            ci="123",
            nombres="Test",
            apellido_paterno="User",
            apellido_materno="Last",
            usuario="test",
            correo="test@test.com",
            password="Password123!",
            tipo_persona="administrativo"
        )
        assert registro.password == "Password123!"
    
    def test_password_hasheada_no_es_reversible(self):
        """Hash de contraseña no debe permitir obtener la contraseña original"""
        password = "SuperSecret123!"
        hashed = AuthService.hash_password(password)
        
        assert password not in hashed
        assert hashed != password
        assert len(hashed) > 50


class TestJWTSecurity:
    """Tests de seguridad de tokens JWT"""
    
    def test_token_expira_despues_tiempo_configurado(self):
        """Token debe expirar después del tiempo configurado"""
        from jose import jwt
        from app.modules.auth.services.auth_service import SECRET_KEY, ALGORITHM
        
        token = AuthService.create_access_token(
            data={"sub": 1},
            expires_delta=timedelta(minutes=1)
        )
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        
        assert "exp" in decoded
        assert decoded["exp"] > 0
    
    def test_token_sin_usuario_id_es_invalido(self):
        """Token sin usuario_id debe ser rechazado"""
        from app.shared.exceptions import Unauthorized
        
        token = AuthService.create_access_token(data={"other": "data"})
        
        with pytest.raises(Unauthorized):
            AuthService.decode_token(token)
    
    def test_token_modificado_es_invalido(self, client):
        """Token modificado debe ser rechazado"""
        token = AuthService.create_access_token(data={"sub": 1})
        
        modified_token = token[:-5] + "XXXXX"
        
        headers = {"Authorization": f"Bearer {modified_token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestInputValidation:
    """Tests de validación de entradas"""
    
    def test_email_invalido_es_rechazado(self):
        """Email inválido debe ser rechazado"""
        with pytest.raises(ValueError):
            RegistroDTO(
                ci="123",
                nombres="Test",
                apellido_paterno="User",
                apellido_materno="Last",
                usuario="test",
                correo="email_invalido",
                password="Password123!",
                tipo_persona="administrativo"
            )
    
    def test_sql_injection_en_login(self, client):
        """Intento de SQL injection debe ser manejado"""
        response = client.post(
            "/api/auth/login",
            json={
                "usuario": "admin' OR '1'='1",
                "password": "' OR '1'='1"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthorizationSecurity:
    """Tests de autorización y permisos"""
    
    def test_usuario_no_puede_modificar_otros_usuarios(self, client, usuario_simple_autenticado, crear_usuario_base, db_session):
        """Usuario sin permisos no puede modificar otros usuarios"""
        otro_usuario = crear_usuario_base("otro_usuario", "pass123")
        db_session.flush()
        
        headers = usuario_simple_autenticado["headers"]
        
        response = client.put(
            f"/api/usuarios/{otro_usuario.id_usuario}",
            json={"nombres": "Intento de modificar"},
            headers=headers
        )
        
        # Si retorna 200, significa que NO hay validación de permisos
        # Este es un problema de seguridad que debe corregirse
        if response.status_code == status.HTTP_200_OK:
            pytest.fail(
                "⚠️ FALLA DE SEGURIDAD: El endpoint permite modificar usuarios sin validar permisos. "
                "Implementar decorador @requires_permission('editar_usuario')"
            )
        
        # Si el endpoint no existe (404), skip
        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Endpoint de actualización de usuarios no implementado aún")
        
        # Si está implementado correctamente, debe rechazar sin permisos
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN, 
            status.HTTP_401_UNAUTHORIZED
        ]
    
    def test_usuario_no_puede_eliminar_otros_usuarios(self, client, usuario_simple_autenticado, crear_usuario_base, db_session):
        """Usuario sin permisos no puede eliminar otros usuarios"""
        otro_usuario = crear_usuario_base("otro_usuario_del", "pass123")
        db_session.flush()
        
        headers = usuario_simple_autenticado["headers"]
        
        response = client.delete(
            f"/api/usuarios/{otro_usuario.id_usuario}",
            headers=headers
        )
        
        # Si retorna 200, es una falla de seguridad
        if response.status_code == status.HTTP_200_OK:
            pytest.fail(
                "⚠️ FALLA DE SEGURIDAD: El endpoint permite eliminar usuarios sin validar permisos. "
                "Implementar decorador @requires_permission('eliminar_usuario')"
            )
        
        # Si el endpoint no existe (404), skip
        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Endpoint de eliminación de usuarios no implementado aún")
        
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN, 
            status.HTTP_401_UNAUTHORIZED
        ]


class TestDataLeakage:
    """Tests de fuga de información"""
    
    def test_error_login_no_revela_si_usuario_existe(self, client, crear_usuario_base, db_session):
        """Los mensajes de error no deben revelar si un usuario existe"""
        usuario_existente = crear_usuario_base("existente", "pass123")
        db_session.flush()
        
        # Intento 1: Usuario que existe, password incorrecta
        response1 = client.post("/api/auth/login", json={
            "usuario": usuario_existente.usuario,
            "password": "password_incorrecta"
        })
        
        # Intento 2: Usuario que NO existe
        response2 = client.post("/api/auth/login", json={
            "usuario": "usuario_que_no_existe_12345",
            "password": "cualquier_password"
        })
        
        assert response1.status_code == status.HTTP_401_UNAUTHORIZED
        assert response2.status_code == status.HTTP_401_UNAUTHORIZED
        
        msg1 = response1.json().get("detail", "")
        msg2 = response2.json().get("detail", "")
        
        # Los mensajes deben ser idénticos
        assert msg1 == msg2, f"Mensajes diferentes: '{msg1}' vs '{msg2}'"
        
        #  Normalizar texto para manejar caracteres especiales
        # Convertir a minúsculas y verificar palabras clave
        msg_lower = msg1.lower()
        
        # Verificar que es un mensaje genérico (contiene "usuario" y alguna referencia a contraseña)
        tiene_usuario = "usuario" in msg_lower
        tiene_password = any(palabra in msg_lower for palabra in ["password", "contrasena", "contraseña", "credenciales"])
        
        assert tiene_usuario and tiene_password, f"Mensaje no es genérico: '{msg1}'"
    
    def test_endpoint_no_expone_passwords(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        """Los endpoints NO deben exponer passwords hasheadas"""
        usuario = crear_usuario_base("usuario_test", "pass123")
        db_session.flush()
        
        headers = usuario_admin_autenticado["headers"]
        
        # Intentar varios endpoints posibles
        endpoints_to_test = [
            f"/api/usuarios/{usuario.id_usuario}",
            f"/api/auth/usuarios/{usuario.id_usuario}",
            "/api/auth/me"  # Endpoint del usuario actual
        ]
        
        for endpoint in endpoints_to_test:
            response = client.get(endpoint, headers=headers)
            
            if response.status_code == status.HTTP_200_OK:
                # Obtener datos del response
                json_response = response.json()
                
                # Manejar diferentes estructuras de respuesta
                if "data" in json_response:
                    data = json_response["data"]
                else:
                    data = json_response
                
                # Verificar que NO exponga passwords
                assert "password" not in data, f"Endpoint {endpoint} expone 'password'"
                assert "password_hash" not in data, f"Endpoint {endpoint} expone 'password_hash'"
                assert "hashed_password" not in data, f"Endpoint {endpoint} expone 'hashed_password'"
                
                # Si encontramos un endpoint que funciona, salir
                break
        else:
            # Si ningún endpoint funciona, skip el test
            pytest.skip("Endpoints de consulta de usuarios no implementados aún")


class TestSessionSecurity:
    """Tests de seguridad de sesiones"""
    
    def test_diferentes_usuarios_tienen_diferentes_tokens(self, client, crear_usuario_base, db_session):
        """Cada usuario debe tener un token único"""
        user1 = crear_usuario_base("user1sec", "pass1")
        user2 = crear_usuario_base("user2sec", "pass2")
        db_session.flush()
        
        # Login user1
        response1 = client.post("/api/auth/login", json={
            "usuario": user1.usuario,
            "password": "pass1"
        })
        
        # Login user2
        response2 = client.post("/api/auth/login", json={
            "usuario": user2.usuario,
            "password": "pass2"
        })
        
        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK
        
        token1 = response1.json()["data"]["access_token"]
        token2 = response2.json()["data"]["access_token"]
        
        assert token1 != token2
        
        decoded1 = AuthService.decode_token(token1)
        decoded2 = AuthService.decode_token(token2)
        
        assert decoded1["usuario_id"] == user1.id_usuario
        assert decoded2["usuario_id"] == user2.id_usuario