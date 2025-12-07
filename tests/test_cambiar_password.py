"""
test_cambiar_password.py - Tests para funcionalidad de cambio de contraseña
✅ Tests completos para HU: Usuario cambia su propia contraseña
"""

import pytest
from fastapi.testclient import TestClient
import time

from app.main import app
from app.modules.usuarios.models.usuario_models import Bitacora, LoginLog
from app.modules.auth.services.auth_service import AuthService

client = TestClient(app)

class TestCambiarPassword:
    """Tests para funcionalidad de cambio de contraseña"""
    
    def test_cambiar_password_exitoso(self, client, db_session, crear_usuario_base, crear_rol_base):
        """Usuario puede cambiar su contraseña proporcionando la actual"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        password_actual = "Password123!"
        password_nueva = "NuevaPassword456!"
        
        # Crear usuario
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password_actual, [rol])
        db_session.commit()
        
        # Crear token
        token = AuthService.create_access_token(
            data={
                "sub": usuario.id_usuario,
                "usuario_id": usuario.id_usuario,
                "usuario": usuario.usuario
            }
        )
        
        # Cambiar contraseña
        response = client.post(
            "/api/auth/cambiar-password",
            json={
                "password_actual": password_actual,
                "password_nueva": password_nueva,
                "confirmar_password_nueva": password_nueva
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Contraseña cambiada exitosamente" in data["message"]
        
        # ✅ Verificar que se registró en Bitácora
        bitacora = db_session.query(Bitacora).filter(
            Bitacora.id_usuario_admin == usuario.id_usuario,
            Bitacora.accion == "CAMBIAR_PASSWORD"
        ).first()
        
        assert bitacora is not None, "No se registró en Bitácora"
        
        # ✅ Verificar que la nueva contraseña funciona
        response_login = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": password_nueva}
        )
        assert response_login.status_code == 200
        
        # ✅ Verificar que la contraseña vieja ya NO funciona
        response_login_vieja = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": password_actual}
        )
        assert response_login_vieja.status_code == 401
    
    def test_cambiar_password_actual_incorrecta(self, client, db_session, crear_usuario_base, crear_rol_base):
        """No se puede cambiar contraseña si la actual es incorrecta"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        password_actual = "Password123!"
        
        # Crear usuario
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password_actual, [rol])
        db_session.commit()
        
        # Crear token
        token = AuthService.create_access_token(
            data={
                "sub": usuario.id_usuario,
                "usuario_id": usuario.id_usuario,
                "usuario": usuario.usuario
            }
        )
        
        # Intentar cambiar con contraseña actual incorrecta
        response = client.post(
            "/api/auth/cambiar-password",
            json={
                "password_actual": "ContraseñaIncorrecta!",
                "password_nueva": "NuevaPassword456!",
                "confirmar_password_nueva": "NuevaPassword456!"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 401
        assert "contraseña actual es incorrecta" in response.json()["detail"].lower()
        
        # ✅ Verificar que se registró intento fallido en LoginLog
        login_log = db_session.query(LoginLog).filter(
            LoginLog.id_usuario == usuario.id_usuario,
            LoginLog.estado == "fallido"
        ).first()
        
        assert login_log is not None
    
    def test_cambiar_password_confirmacion_no_coincide(self, client, db_session, crear_usuario_base, crear_rol_base):
        """Validar que la confirmación de contraseña coincida"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        password_actual = "Password123!"
        
        # Crear usuario
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password_actual, [rol])
        db_session.commit()
        
        # Crear token
        token = AuthService.create_access_token(
            data={
                "sub": usuario.id_usuario,
                "usuario_id": usuario.id_usuario,
                "usuario": usuario.usuario
            }
        )
        
        # Intentar cambiar con confirmación diferente
        response = client.post(
            "/api/auth/cambiar-password",
            json={
                "password_actual": password_actual,
                "password_nueva": "NuevaPassword456!",
                "confirmar_password_nueva": "DiferentePassword789!"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 422  # Validation error
        assert "no coinciden" in str(response.json()).lower()
    
    def test_cambiar_password_nueva_igual_actual(self, client, db_session, crear_usuario_base, crear_rol_base):
        """La nueva contraseña debe ser diferente a la actual"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        password = "Password123!"
        
        # Crear usuario
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password, [rol])
        db_session.commit()
        
        # Crear token
        token = AuthService.create_access_token(
            data={
                "sub": usuario.id_usuario,
                "usuario_id": usuario.id_usuario,
                "usuario": usuario.usuario
            }
        )
        
        # Intentar cambiar a la misma contraseña
        response = client.post(
            "/api/auth/cambiar-password",
            json={
                "password_actual": password,
                "password_nueva": password,  # ❌ Misma que la actual
                "confirmar_password_nueva": password
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 422
        assert "diferente" in str(response.json()).lower()
    
    def test_cambiar_password_sin_autenticacion(self, client):
        """No se puede cambiar contraseña sin estar autenticado"""
        response = client.post(
            "/api/auth/cambiar-password",
            json={
                "password_actual": "Password123!",
                "password_nueva": "NuevaPassword456!",
                "confirmar_password_nueva": "NuevaPassword456!"
            }
        )
        
        assert response.status_code == 401
    
    def test_cambiar_password_nueva_debil(self, client, db_session, crear_usuario_base, crear_rol_base):
        """La nueva contraseña debe cumplir requisitos de seguridad"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        password_actual = "Password123!"
        
        # Crear usuario
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password_actual, [rol])
        db_session.commit()
        
        # Crear token
        token = AuthService.create_access_token(
            data={
                "sub": usuario.id_usuario,
                "usuario_id": usuario.id_usuario,
                "usuario": usuario.usuario
            }
        )
        
        # Lista de contraseñas débiles
        passwords_debiles = [
            "12345678",  # Solo números
            "abcdefgh",  # Solo minúsculas
            "ABCDEFGH",  # Solo mayúsculas
            "Pass123",   # Muy corta
            "Password",  # Sin números ni especiales
        ]
        
        for password_debil in passwords_debiles:
            response = client.post(
                "/api/auth/cambiar-password",
                json={
                    "password_actual": password_actual,
                    "password_nueva": password_debil,
                    "confirmar_password_nueva": password_debil
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 422, f"Debió rechazar: {password_debil}"
    
    def test_cambiar_password_multiple_veces(self, client, db_session, crear_usuario_base, crear_rol_base):
        """Usuario puede cambiar contraseña múltiples veces"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        passwords = [
            "Password1!",
            "Password2!",
            "Password3!"
        ]
        
        # Crear usuario
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, passwords[0], [rol])
        db_session.commit()
        
        for i in range(len(passwords) - 1):
            # Login con contraseña actual
            response_login = client.post(
                "/api/auth/login",
                json={"usuario": username, "password": passwords[i]}
            )
            assert response_login.status_code == 200
            token = response_login.json()["data"]["access_token"]
            
            # Cambiar a siguiente contraseña
            response = client.post(
                "/api/auth/cambiar-password",
                json={
                    "password_actual": passwords[i],
                    "password_nueva": passwords[i + 1],
                    "confirmar_password_nueva": passwords[i + 1]
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
        
        # ✅ Verificar que se registraron todos los cambios
        cambios = db_session.query(Bitacora).filter(
            Bitacora.id_usuario_admin == usuario.id_usuario,
            Bitacora.accion == "CAMBIAR_PASSWORD"
        ).count()
        
        assert cambios == len(passwords) - 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])