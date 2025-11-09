"""
tests/conftest.py - USANDO BASE DE DATOS MYSQL REAL
Configuración global de pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
import random
import time
from app.shared.security import hash_password

# Importar la configuración real de la aplicación
from app.core.database import engine, Base, get_db
from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona1, Rol, Permiso, LoginLog, RolHistorial, Bitacora,
    usuario_roles_table, rol_permisos_table
)
from app.modules.auth.services.auth_service import AuthService
from app.main import app

# ============================================
# USAR LA BASE DE DATOS REAL DE LA APLICACIÓN (MYSQL)
# ============================================

@pytest.fixture(scope="function")
def db_session():
    """Sesión de base de datos REAL con rollback automático"""
    # Crear una sesión de prueba
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        # ROLLBACK automático - los cambios NO se guardan en la BD
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de pruebas de FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()

# ============================================
# FIXTURES DE CREACIÓN DE DATOS
# ============================================

@pytest.fixture
def crear_permiso_base(db_session):
    """Fixture para crear permisos básicos"""
    def _crear_permiso(nombre: str, modulo: str, descripcion: str = ""):
        permiso = Permiso(
            nombre=nombre,
            modulo=modulo,
            descripcion=descripcion,
            is_active=True
        )
        db_session.add(permiso)
        db_session.flush()
        return permiso
    return _crear_permiso

@pytest.fixture
def crear_rol_base(db_session):
    """Fixture para crear roles básicos"""
    def _crear_rol(nombre: str, descripcion: str = "", permisos: list = None):
        rol = Rol(
            nombre=nombre,
            descripcion=descripcion,
            is_active=True
        )
        if permisos:
            rol.permisos = permisos
        db_session.add(rol)
        db_session.flush()
        return rol
    return _crear_rol

@pytest.fixture
def crear_persona_base(db_session):
    """Fixture para crear personas con identificadores únicos"""
    def _crear_persona(ci: str = None, nombres: str = None, tipo_persona: str = "administrativo"):
        # Usar timestamp en milisegundos + random para garantizar unicidad
        timestamp_ms = int(time.time() * 1000)
        rand_suffix = random.randint(10000, 99999)
        
        if ci is None:
            ci = f"TEST_CI_{timestamp_ms}_{rand_suffix}"
        if nombres is None:
            nombres = f"TestPersona_{timestamp_ms}"
        
        # Correo único usando timestamp + random
        correo_unico = f"test_{timestamp_ms}_{rand_suffix}@test.com"
            
        persona = Persona1(
            ci=ci,
            nombres=nombres,
            apellido_paterno="TestApellido",
            apellido_materno="TestMaterno",
            correo=correo_unico,
            telefono="12345678",
            direccion="Dirección test",
            tipo_persona=tipo_persona
        )
        db_session.add(persona)
        db_session.flush()
        return persona
    return _crear_persona

@pytest.fixture
def crear_usuario_base(db_session, crear_persona_base):
    def _crear_usuario(usuario: str, password: str, roles: list = None, mantener_nombre=False):
        timestamp_ms = int(time.time() * 1000)
        rand_suffix = random.randint(1000, 9999)

        ci_unico = f"TEST_{timestamp_ms}_{rand_suffix}"
        if mantener_nombre:
            usuario_unico = usuario  # usamos el nombre exacto
        else:
            usuario_unico = f"{usuario}_{rand_suffix}"  # sufijo aleatorio

        persona = crear_persona_base(ci=ci_unico, nombres=f"Usuario {usuario}")

        correo_unico = f"{usuario}_{timestamp_ms}@test.com"
        password_hasheado = AuthService.hash_password(password)

        usuario_obj = Usuario(
            id_persona=persona.id_persona,
            usuario=usuario_unico,
            correo=correo_unico,
            password=password_hasheado,
            is_active=True
        )

        db_session.add(usuario_obj)
        db_session.commit()  # <-- commit para que sea visible en otros queries

        if roles:
            usuario_obj.roles = roles
            db_session.commit()

        return usuario_obj
    return _crear_usuario



@pytest.fixture
def usuario_admin_autenticado(db_session, crear_usuario_base, crear_rol_base, crear_permiso_base):
    """Fixture para usuario administrador autenticado con token"""
    # Usar timestamp para garantizar nombres únicos
    timestamp_ms = int(time.time() * 1000)
    
    # Crear permisos únicos
    permisos = [
        crear_permiso_base(f"crear_usuario_{timestamp_ms}_{random.randint(1,999)}", "usuarios"),
        crear_permiso_base(f"ver_usuario_{timestamp_ms}_{random.randint(1,999)}", "usuarios"),
        crear_permiso_base(f"editar_usuario_{timestamp_ms}_{random.randint(1,999)}", "usuarios"),
        crear_permiso_base(f"eliminar_usuario_{timestamp_ms}_{random.randint(1,999)}", "usuarios"),
        crear_permiso_base(f"crear_rol_{timestamp_ms}_{random.randint(1,999)}", "usuarios"),
        crear_permiso_base(f"asignar_permisos_{timestamp_ms}_{random.randint(1,999)}", "usuarios"),
    ]
    
    # Crear rol con permisos
    rol_admin = crear_rol_base(f"Admin_{timestamp_ms}", "Rol administrativo", permisos)
    db_session.flush()
    
    # Crear usuario con rol
    usuario = crear_usuario_base(f"admin_test_{timestamp_ms}", "admin123", [rol_admin])
    db_session.flush()
    
    # Generar token
    token = AuthService.create_access_token(
        data={"sub": usuario.id_usuario, "usuario": usuario.usuario}
    )
    
    return {
        "usuario": usuario,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }

@pytest.fixture
def usuario_simple_autenticado(db_session, crear_usuario_base, crear_rol_base):
    """Fixture para usuario sin permisos especiales"""
    timestamp_ms = int(time.time() * 1000)
    
    rol_simple = crear_rol_base(f"Usuario_{timestamp_ms}", "Rol básico")
    db_session.flush()
    
    usuario = crear_usuario_base(f"user1_test_{timestamp_ms}", "user123", [rol_simple])
    db_session.flush()
    
    token = AuthService.create_access_token(
        data={"sub": usuario.id_usuario, "usuario": usuario.usuario}
    )
    
    return {
        "usuario": usuario,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }

@pytest.fixture
def datos_usuario_valido():
    """Datos válidos para crear un usuario"""
    timestamp_ms = int(time.time() * 1000)
    rand_num = random.randint(10000, 99999)
    return {
        "ci": f"TEST_{timestamp_ms}_{rand_num}",
        "nombres": "Juan",
        "apellido_paterno": "Pérez",
        "apellido_materno": "García",
        "usuario": f"jperez_test_{timestamp_ms}_{rand_num}",
        "correo": f"jperez_test_{timestamp_ms}_{rand_num}@test.com",
        "password": "Password123!",
        "telefono": "12345678",
        "direccion": "Calle Test 123",
        "tipo_persona": "profesor"
    }

@pytest.fixture
def datos_login_valido():
    """Datos válidos para login"""
    return {
        "usuario": "admin_test",
        "password": "admin123"
    }