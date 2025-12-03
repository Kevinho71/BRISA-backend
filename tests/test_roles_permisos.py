"""
tests/test_roles_permisos.py 
Pruebas de integración para roles y permisos
"""
import pytest
from fastapi import status
import random


class TestCrearRolEndpoint:
    """Pruebas del endpoint de creación de roles"""
    
    def test_crear_rol_exitoso(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        datos_rol = {"nombre": f"Profesor{rand}", "descripcion": "Rol para profesores"}
        
        response = client.post("/api/auth/roles", json=datos_rol, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        # ResponseModel usa "success": True
        assert data["success"] == True
        assert "data" in data
    
    def test_crear_rol_sin_autenticacion(self, client):
        datos_rol = {"nombre": "Test", "descripcion": "Test"}
        response = client.post("/api/auth/roles", json=datos_rol)
        # Sin autenticación debe ser 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_crear_rol_nombre_duplicado(self, client, usuario_admin_autenticado, crear_rol_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        crear_rol_base("RolExistente", "Descripción")
        datos_rol = {"nombre": "RolExistente", "descripcion": "Intento duplicado"}
        
        response = client.post("/api/auth/roles", json=datos_rol, headers=headers)
        assert response.status_code == status.HTTP_409_CONFLICT


class TestListarRolesEndpoint:
    """Pruebas del endpoint de listado de roles"""
    
    def test_listar_roles_exitoso(self, client, usuario_admin_autenticado, crear_rol_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        crear_rol_base(f"Rol1_{rand}", "Descripción 1")
        crear_rol_base(f"Rol2_{rand}", "Descripción 2")
        
        response = client.get("/api/auth/roles", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # ResponseModel usa "success": True
        assert data["success"] == True
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_listar_roles_sin_autenticacion(self, client):
        response = client.get("/api/auth/roles")
        # Sin autenticación debe ser 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestObtenerRolEndpoint:
    """Pruebas del endpoint de obtener rol específico"""
    
    def test_obtener_rol_existente(self, client, usuario_admin_autenticado, crear_rol_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        rol = crear_rol_base(f"RolTest_{rand}", "Descripción test")
        
        response = client.get(f"/api/auth/roles/{rol.id_rol}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # ResponseModel usa "success": True
        assert data["success"] == True
        assert "data" in data
    
    def test_obtener_rol_no_existe(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.get("/api/auth/roles/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAsignarRolUsuarioEndpoint:
    """Pruebas del endpoint de asignación de roles a usuarios"""
    
    def test_asignar_rol_usuario_exitoso(self, client, usuario_admin_autenticado, crear_usuario_base, crear_rol_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        usuario = crear_usuario_base(f"testuser_{rand}", "pass123")
        rol = crear_rol_base(f"NuevoRol_{rand}", "Descripción")
        
        response = client.post(f"/api/auth/usuarios/{usuario.id_usuario}/roles/{rol.id_rol}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] == True
    
    def test_asignar_rol_usuario_no_existe(self, client, usuario_admin_autenticado, crear_rol_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        rol = crear_rol_base(f"Rol_{rand}", "Desc")
        
        response = client.post(f"/api/auth/usuarios/99999/roles/{rol.id_rol}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_asignar_rol_no_existe(self, client, usuario_admin_autenticado, crear_usuario_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        usuario = crear_usuario_base(f"testuser_{rand}", "pass123")
        
        response = client.post(f"/api/auth/usuarios/{usuario.id_usuario}/roles/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestListarPermisosEndpoint:
    """Pruebas del endpoint de listado de permisos"""
    
    def test_listar_permisos_exitoso(self, client, usuario_admin_autenticado, crear_permiso_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        crear_permiso_base(f"permiso1_{rand}", "modulo1", "Descripción 1")
        crear_permiso_base(f"permiso2_{rand}", "modulo2", "Descripción 2")
        
        response = client.get("/api/auth/permisos", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] == True
        assert isinstance(data["data"], list)
    
    def test_listar_permisos_filtrado_por_modulo(self, client, usuario_admin_autenticado, crear_permiso_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        crear_permiso_base(f"perm1_{rand}", "usuarios", "Desc 1")
        crear_permiso_base(f"perm2_{rand}", "usuarios", "Desc 2")
        
        response = client.get("/api/auth/permisos?modulo=usuarios", headers=headers)
        assert response.status_code == status.HTTP_200_OK


class TestObtenerPermisoEndpoint:
    """Pruebas del endpoint de obtener permiso específico"""
    
    def test_obtener_permiso_existente(self, client, usuario_admin_autenticado, crear_permiso_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        permiso = crear_permiso_base(f"test_perm_{rand}", "modulo", "Desc")
        
        response = client.get(f"/api/auth/permisos/{permiso.id_permiso}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] == True
    
    def test_obtener_permiso_no_existe(self, client, usuario_admin_autenticado):
        headers = usuario_admin_autenticado["headers"]
        response = client.get("/api/auth/permisos/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAsignarPermisosRolEndpoint:
    """Pruebas del endpoint de asignación de permisos a roles"""
    
    def test_asignar_permisos_rol_exitoso(self, client, usuario_admin_autenticado, crear_rol_base, crear_permiso_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        rol = crear_rol_base(f"TestRol_{rand}", "Descripción")
        perm1 = crear_permiso_base(f"perm1_{rand}", "mod1", "Desc 1")
        perm2 = crear_permiso_base(f"perm2_{rand}", "mod2", "Desc 2")
        
        response = client.post(f"/api/auth/roles/{rol.id_rol}/permisos", json=[perm1.id_permiso, perm2.id_permiso], headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] == True
    
    def test_asignar_permisos_rol_no_existe(self, client, usuario_admin_autenticado, crear_permiso_base, db_session):
        headers = usuario_admin_autenticado["headers"]
        rand = random.randint(1000, 9999)
        perm = crear_permiso_base(f"perm_{rand}", "mod", "Desc")
        
        response = client.post("/api/auth/roles/99999/permisos", json=[perm.id_permiso], headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND