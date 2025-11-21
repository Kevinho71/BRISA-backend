"""
tests/test_personas.py
Tests esenciales de generación automática de credenciales
"""
import pytest
from datetime import datetime
import random
import time

from app.modules.usuarios.services.usuario_service import PersonaService
from app.modules.usuarios.dto.usuario_dto import PersonaCreateDTO, PersonaUpdateDTO
from app.modules.usuarios.models.usuario_models import Usuario, Bitacora, Rol, Permiso, Persona1
from app.shared.security import verify_password


class TestGeneracionCredenciales:
    """Tests esenciales de generación de credenciales"""
    
    @pytest.fixture
    def persona_dto(self):
        """DTO básico para crear persona"""
        rand = random.randint(10000, 99999)
        return PersonaCreateDTO(
            ci=f"T{rand}",  # ✅ CI corto (máx 20 chars)
            nombres="Juan Carlos",
            apellido_paterno="Pérez",
            apellido_materno="García",
            correo=f"juan{rand}@test.com",
            tipo_persona="profesor",
            tiene_acceso=True
        )
    
    def test_generar_username_basico(self, db_session, persona_dto):
        """
        TEST 1: Generación básica de username
        Regla: primera_letra_apellido + nombres_sin_espacios
        Ejemplo: Juan Carlos Pérez → pjuancarlos (o pjuancarlos1, pjuancarlos2 si ya existe)
        """
        resultado = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=None)
        
        username = resultado['credenciales']['usuario']
        
        # Verificar que empieza con 'p' y contiene 'juancarlos'
        assert username.startswith('p'), f"Debe empezar con 'p', obtenido: '{username}'"
        assert 'juancarlos' in username, f"Debe contener 'juancarlos', obtenido: '{username}'"
        assert username.islower(), "Debe estar en minúsculas"
        assert ' ' not in username, "No debe tener espacios"
        
        db_session.rollback()
    
    def test_colision_username_duplicado(self, db_session, persona_dto):
        """
        TEST 2: Manejo de colisión de usernames
        Si existe pjuancarlos → pjuancarlos1 → pjuancarlos2
        """
        rand = random.randint(10000, 99999)
        
        # Primera persona
        resultado1 = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=None)
        username1 = resultado1['credenciales']['usuario']
        assert 'pjuancarlos' in username1, f"Username debe contener 'pjuancarlos', obtenido: {username1}"
        
        # Segunda persona (mismo nombre y apellido, debe generar username diferente)
        persona_dto2 = PersonaCreateDTO(
            ci=f"T{rand}",
            nombres="Juan Carlos",
            apellido_paterno="Pérez",
            apellido_materno="López",
            correo=f"juan2{rand}@test.com",
            tipo_persona="profesor",
            tiene_acceso=True
        )
        
        resultado2 = PersonaService.crear_persona_con_usuario(db_session, persona_dto2, user_id=None)
        username2 = resultado2['credenciales']['usuario']
        
        # Verificar que son diferentes y el segundo tiene número
        assert username1 != username2, "Los usernames deben ser diferentes"
        assert 'pjuancarlos' in username2, f"Username debe contener 'pjuancarlos', obtenido: {username2}"
        
        # Extraer número del username2
        numero = username2.replace('pjuancarlos', '')
        assert numero.isdigit() or numero == '', f"Debe terminar en número o estar vacío, obtenido: {numero}"
        
        db_session.rollback()
    
    def test_limpieza_acentos(self, db_session):
        """
        TEST 3: Limpieza de acentos y eñes
        José María Núñez → njosemaria
        """
        rand = random.randint(10000, 99999)
        
        persona_dto = PersonaCreateDTO(
            ci=f"T{rand}",
            nombres="José María",
            apellido_paterno="Núñez",
            apellido_materno="Ramírez",
            correo=f"jose{rand}@test.com",
            tipo_persona="profesor",
            tiene_acceso=True
        )
        
        resultado = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=None)
        username = resultado['credenciales']['usuario']
        
        # Verificar que empieza con 'n' y contiene 'josemaria'
        assert username.startswith('n'), f"Debe empezar con 'n', obtenido: '{username}'"
        assert 'josemaria' in username, f"Debe contener 'josemaria', obtenido: '{username}'"
        assert 'ñ' not in username and 'á' not in username and 'é' not in username
        
        db_session.rollback()
    
    def test_password_temporal_formato(self, db_session, persona_dto):
        """
        TEST 4: Formato de password temporal
        Formato: Temporal{año}*{números}
        """
        resultado = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=None)
        
        password = resultado['credenciales']['password_temporal']
        año = datetime.now().year
        
        assert password.startswith('Temporal'), "Debe empezar con 'Temporal'"
        assert str(año) in password, f"Debe contener año {año}"
        assert any(s in password for s in ['*', '#', '@', '!']), "Debe tener símbolo"
        assert len(password) >= 12, "Debe tener mínimo 12 caracteres"
        
        db_session.rollback()
    
    def test_password_hasheada_en_bd(self, db_session, persona_dto):
        """
        TEST 5: Password se guarda hasheada (NO en texto plano)
        """
        resultado = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=None)
        
        password_temporal = resultado['credenciales']['password_temporal']
        id_usuario = resultado['persona']['id_usuario']
        
        usuario = db_session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        
        # NO debe estar en texto plano
        assert usuario.password != password_temporal, "Password NO debe guardarse en texto plano"
        
        # Verificar que el hash funciona
        assert verify_password(password_temporal, usuario.password), "Hash debe coincidir"
        
        db_session.rollback()
    
    def test_persona_sin_acceso_no_genera_credenciales(self, db_session):
        """
        TEST 6: Persona sin acceso NO genera credenciales
        """
        rand = random.randint(10000, 99999)
        
        persona_dto = PersonaCreateDTO(
            ci=f"T{rand}",
            nombres="María",
            apellido_paterno="González",
            apellido_materno="Silva",
            correo=f"maria{rand}@test.com",
            tipo_persona="administrativo",
            tiene_acceso=False  # ⚠️ Sin acceso
        )
        
        resultado = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=None)
        
        assert resultado['credenciales'] is None, "No debe generar credenciales"
        assert resultado['persona']['tiene_acceso'] is False
        assert resultado['persona']['usuario'] is None
        
        db_session.rollback()


class TestBitacoraPersonas:
    """Tests de auditoría en bitácora"""
    
    @pytest.fixture
    def usuario_admin(self, db_session, crear_permiso_base, crear_rol_base, crear_persona_base):
        """Usuario admin para tests de auditoría"""
        rand = random.randint(10000, 99999)
        
        # Crear permisos
        permiso_eliminar = crear_permiso_base("eliminar_usuario", "usuarios")
        permiso_editar = crear_permiso_base("editar_usuario", "usuarios")
        
        # Crear rol con permisos
        rol = crear_rol_base(f"Admin{rand}", "Admin completo", [permiso_eliminar, permiso_editar])
        
        # Crear persona y usuario
        persona = crear_persona_base(ci=f"ADM{rand}", nombres="Admin Test")
        
        usuario = Usuario(
            id_persona=persona.id_persona,
            usuario=f"admin{rand}",
            correo=f"admin{rand}@test.com",
            password="hashed",
            is_active=True
        )
        usuario.roles.append(rol)
        db_session.add(usuario)
        db_session.flush()
        
        return usuario
    
    def test_crear_persona_registra_bitacora(self, db_session):
        """TEST 7: Crear persona registra en bitácora"""
        rand = random.randint(10000, 99999)
        
        persona_dto = PersonaCreateDTO(
            ci=f"T{rand}",
            nombres="Pedro",
            apellido_paterno="López",
            apellido_materno="Martínez",
            correo=f"pedro{rand}@test.com",
            tipo_persona="profesor",
            tiene_acceso=False
        )
        
        user_id_admin = 1
        resultado = PersonaService.crear_persona_con_usuario(db_session, persona_dto, user_id=user_id_admin)
        id_persona = resultado['persona']['id_persona']
        
        # Verificar bitácora
        bitacora = db_session.query(Bitacora).filter(
            Bitacora.tipo_objetivo == "Persona",
            Bitacora.id_objetivo == id_persona,
            Bitacora.accion == "CREAR_PERSONA"
        ).first()
        
        assert bitacora is not None, "Debe existir registro en bitácora"
        assert bitacora.id_usuario_admin == user_id_admin
        
        db_session.rollback()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])