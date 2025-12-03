"""
test_auth.py - Tests completos para HU-01 y HU-02
Refresca sesión después de operaciones para ver cambios en BD
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
import random

from app.main import app
from app.modules.usuarios.models.usuario_models import LoginLog, Bitacora
from app.modules.auth.services.auth_service import AuthService

client = TestClient(app)

# ==================== TESTS HU-01: LOGIN ====================

class TestLogin:
    """Tests para HU-01: Inicio de sesión"""
    
    def test_login_exitoso_registra_bitacora(self, db_session, crear_usuario_base, crear_rol_base):
        """HU-01: Login exitoso debe registrar en Bitácora"""
        timestamp = int(time.time() * 1000)
        username = f"jperez_{timestamp}"
        password = "Password123!"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password, [rol])
        db_session.commit()  # ✅ Commit para persistir
        
        response = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": password}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        
        # ✅ Refrescar sesión antes de consultar
        db_session.expire_all()
        
        # Verificar LoginLog
        login_log = db_session.query(LoginLog).filter(
            LoginLog.id_usuario == usuario.id_usuario,
            LoginLog.estado == "exitoso"
        ).order_by(LoginLog.fecha_hora.desc()).first()
        
        assert login_log is not None
        assert login_log.estado == "exitoso"
        
        # Verificar Bitacora
        bitacora = db_session.query(Bitacora).filter(
            Bitacora.id_usuario_admin == usuario.id_usuario,
            Bitacora.accion == "LOGIN"
        ).order_by(Bitacora.fecha_hora.desc()).first()
        
        assert bitacora is not None
        assert bitacora.accion == "LOGIN"
        assert bitacora.tipo_objetivo == "Usuario"
        assert bitacora.id_objetivo == usuario.id_usuario
    
    def test_login_credenciales_invalidas_registra_fallido(self, db_session, crear_usuario_base, crear_rol_base):
        """HU-01: Login fallido debe registrar en LoginLog"""
        timestamp = int(time.time() * 1000)
        username = f"jperez_{timestamp}"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, "Password123!", [rol])
        db_session.commit()
        
        response = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": "ContraseñaIncorrecta"}
        )
        
        assert response.status_code == 401
        
        # ✅ Refrescar sesión
        db_session.expire_all()
        
        # Verificar LoginLog con estado 'fallido'
        login_log = db_session.query(LoginLog).filter(
            LoginLog.id_usuario == usuario.id_usuario,
            LoginLog.estado == "fallido"
        ).order_by(LoginLog.fecha_hora.desc()).first()
        
        assert login_log is not None
        assert login_log.estado == "fallido"
    
    def test_login_usuario_inexistente_mensaje_generico(self, db_session):
        """HU-01: Usuario inexistente NO debe revelar información"""
        timestamp = int(time.time() * 1000)
        
        response = client.post(
            "/api/auth/login",
            json={
                "usuario": f"usuario_inexistente_{timestamp}",
                "password": "Password123!"
            }
        )
        
        assert response.status_code == 401
        assert "Usuario o contraseña incorrectos" in response.json()["detail"]
    
    def test_login_captura_ip_y_user_agent(self, db_session, crear_usuario_base, crear_rol_base):
        """HU-01: Login debe capturar IP y User-Agent"""
        timestamp = int(time.time() * 1000)
        username = f"jperez_{timestamp}"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, "Password123!", [rol])
        db_session.commit()
        
        response = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": "Password123!"},
            headers={
                "User-Agent": "TestClient/1.0",
                "X-Forwarded-For": "192.168.1.100"
            }
        )
        
        assert response.status_code == 200
        
        # ✅ Refrescar sesión
        db_session.expire_all()
        
        # Verificar LoginLog con IP y User-Agent
        login_log = db_session.query(LoginLog).filter(
            LoginLog.id_usuario == usuario.id_usuario
        ).order_by(LoginLog.fecha_hora.desc()).first()
        
        assert login_log is not None
        assert login_log.ip_address == "192.168.1.100"
        assert login_log.user_agent == "TestClient/1.0"


# ==================== TESTS HU-02: LOGOUT ====================

class TestLogout:
    """Tests para HU-02: Cierre de sesión"""
    
    def test_logout_exitoso_registra_bitacora(
        self, 
        db_session, 
        fresh_db_session,  # ✅ AGREGAR ESTE PARÁMETRO
        crear_usuario_base, 
        crear_rol_base
    ):
        """HU-02: Logout debe registrar en Bitácora"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        user = crear_usuario_base(username, "Password123!", [rol])
        db_session.commit()
        
        token = AuthService.create_access_token(
            data={
                "sub": user.id_usuario,
                "usuario_id": user.id_usuario,
                "usuario": user.usuario
            }
        )
        
        response = client.post(
            "/api/auth/logout",
            headers={
                "Authorization": f"Bearer {token}",
                "X-Forwarded-For": "192.168.1.100"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["token_invalidado"] == True
        
        # Usar fresh_db_session en lugar de db_session
        bitacora = fresh_db_session.query(Bitacora).filter(
            Bitacora.id_usuario_admin == user.id_usuario,
            Bitacora.accion == "LOGOUT"
        ).order_by(Bitacora.fecha_hora.desc()).first()
        
        assert bitacora is not None, "No se encontró registro de Bitacora para LOGOUT"
        assert bitacora.accion == "LOGOUT"
        assert "192.168.1.100" in bitacora.descripcion
    
    def test_logout_invalida_token(self, db_session, crear_usuario_base, crear_rol_base):
        """HU-02: Token no debe funcionar después de logout"""
        timestamp = int(time.time() * 1000)
        username = f"user_{timestamp}"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        user = crear_usuario_base(username, "Password123!", [rol])
        db_session.commit()
        
        token = AuthService.create_access_token(
            data={
                "sub": user.id_usuario,
                "usuario_id": user.id_usuario,
                "usuario": user.usuario
            }
        )
        
        # Hacer logout
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        
        # Intentar usar token después de logout
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 401
    
    def test_logout_sin_token_falla(self, db_session):
        """HU-02: Logout sin token debe fallar"""
        response = client.post("/api/auth/logout")
        assert response.status_code == 401
    
    def test_logout_token_invalido_falla(self, db_session):
        """HU-02: Logout con token inválido debe fallar"""
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": "Bearer token_invalido"}
        )
        assert response.status_code == 401


# ==================== TESTS MIDDLEWARE ====================

class TestMiddleware:
    """Tests para middleware JWT"""
    
    def test_middleware_valida_token_en_rutas_protegidas(self, db_session, crear_usuario_base, crear_rol_base):
        """Middleware debe validar token en rutas protegidas"""
        timestamp = int(time.time() * 1000)
        username = f"jperez_{timestamp}"
        password = "Password123!"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password, [rol])
        db_session.commit()
        
        response = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": password}
        )
        token = response.json()["data"]["access_token"]
        
        # Usar token
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["usuario"] == username
    
    def test_middleware_permite_rutas_publicas(self, db_session):
        """Middleware debe permitir acceso a rutas públicas"""
        response = client.get("/health")
        assert response.status_code == 200
        
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_middleware_rechaza_token_invalido(self, db_session):
        """Middleware debe rechazar tokens inválidos"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer token_invalido"}
        )
        assert response.status_code == 401
    
    def test_middleware_rechaza_sin_token(self, db_session):
        """Middleware debe rechazar requests sin token"""
        response = client.get("/api/auth/usuarios")
        assert response.status_code == 401


# ==================== TESTS SEGURIDAD ====================

class TestSeguridad:
    """Tests de seguridad"""
    
    def test_password_hasheado_bcrypt(self, db_session, crear_usuario_base, crear_rol_base):
        """Contraseñas deben estar hasheadas con bcrypt"""
        timestamp = int(time.time() * 1000)
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(f"test_{timestamp}", "Password123!", [rol])
        db_session.commit()
        
        assert usuario.password != "Password123!"
        assert usuario.password.startswith("$2b$")
    
    def test_no_sql_injection(self, db_session):
        """Protección contra SQL injection"""
        response = client.post(
            "/api/auth/login",
            json={
                "usuario": "admin' OR '1'='1",
                "password": "cualquiera"
            }
        )
        
        assert response.status_code == 401
        assert "SQL" not in response.json()["detail"]
    
    def test_multiples_intentos_fallidos(self, db_session, crear_usuario_base, crear_rol_base):
        """Registrar múltiples intentos fallidos"""
        timestamp = int(time.time() * 1000)
        username = f"jperez_{timestamp}"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, "Password123!", [rol])
        db_session.commit()
        
        # Intentar login 5 veces
        for _ in range(5):
            client.post(
                "/api/auth/login",
                json={"usuario": username, "password": "Incorrecta"}
            )
        
        # ✅ Refrescar sesión
        db_session.expire_all()
        
        intentos = db_session.query(LoginLog).filter(
            LoginLog.id_usuario == usuario.id_usuario,
            LoginLog.estado == "fallido"
        ).count()
        
        assert intentos >= 5


def test_database_type(db_session):
    """Verificar qué tipo de BD estamos usando"""
    engine_url = str(db_session.bind.url)
    print(f"\n🔍 Motor de BD: {engine_url}")
    
    if "sqlite" in engine_url.lower():
        print("✅ Usando SQLite en memoria (TESTS)")
    elif "mysql" in engine_url.lower():
        print("⚠️ Usando MySQL REAL")


# ==================== TEST INTEGRACIÓN ====================

class TestIntegracion:
    """Test del flujo completo"""
    
    def test_flujo_login_uso_logout(
        self, 
        db_session, 
        fresh_db_session,  # ✅ AGREGAR ESTE PARÁMETRO
        crear_usuario_base, 
        crear_rol_base
    ):
        """Test completo: login -> uso -> logout"""
        timestamp = int(time.time() * 1000)
        username = f"jperez_{timestamp}"
        password = "Password123!"
        
        rol = crear_rol_base(f"Rol_{timestamp}", "Test")
        usuario = crear_usuario_base(username, password, [rol])
        db_session.commit()
        
        # 1. Login
        response = client.post(
            "/api/auth/login",
            json={"usuario": username, "password": password},
            headers={"X-Forwarded-For": "192.168.1.100"}
        )
        assert response.status_code == 200
        token = response.json()["data"]["access_token"]
        
        # ✅ Refrescar para ver LoginLog y Bitacora de LOGIN
        db_session.expire_all()
        
        # 2. Verificar LoginLog
        login_log = db_session.query(LoginLog).filter(
            LoginLog.id_usuario == usuario.id_usuario,
            LoginLog.estado == "exitoso"
        ).first()
        assert login_log is not None
        assert login_log.ip_address == "192.168.1.100"
        
        # 3. Verificar Bitacora de LOGIN
        bitacora_login = db_session.query(Bitacora).filter(
            Bitacora.id_usuario_admin == usuario.id_usuario,
            Bitacora.accion == "LOGIN"
        ).first()
        assert bitacora_login is not None
        
        # 4. Usar API autenticado
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        
        # 5. Logout
        response = client.post(
            "/api/auth/logout",
            headers={
                "Authorization": f"Bearer {token}",
                "X-Forwarded-For": "192.168.1.100"
            }
        )
        assert response.status_code == 200
        
        # Usar fresh_db_session para ver LOGOUT en Bitacora
        bitacora_logout = fresh_db_session.query(Bitacora).filter(
            Bitacora.id_usuario_admin == usuario.id_usuario,
            Bitacora.accion == "LOGOUT"
        ).order_by(Bitacora.fecha_hora.desc()).first()
        
        assert bitacora_logout is not None, "No se encontró registro de LOGOUT en Bitacora"
        assert "192.168.1.100" in bitacora_logout.descripcion
        
        # 7. Verificar que token no funciona
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401
        
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])