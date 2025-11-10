"""
Script para verificar que todo el backend está configurado correctamente
Ejecutar: python scripts/verify_setup.py
"""

import os
import sys
from pathlib import Path

# Aseguramos que 'app' esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.shared.security import verify_token  # la dependencia que usamos en los endpoints

def check_imports():
    """Verifica que todos los imports críticos funcionen"""
    print("\n[1] Verificando imports...")
    try:
        from app.core import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_URL
        print(f"  ✓ Config imports OK")
        print(f"    - SECRET_KEY: {'*' * 10}")
        print(f"    - ALGORITHM: {ALGORITHM}")
        print(f"    - ACCESS_TOKEN_EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")
        return True
    except Exception as e:
        print(f"  ✗ Error en config imports: {e}")
        return False

def check_database_connection():
    """Verifica la conexión a la base de datos (solo conexión, sin crear tablas)"""
    print("\n[2] Verificando conexión a BD...")
    try:
        from app.core import engine
        with engine.connect() as connection:
            print("  ✓ Conexión a BD exitosa")
            return True
    except Exception as e:
        print(f"  ✗ Error de conexión a BD: {e}")
        return False

def check_models():
    """Verifica que los modelos SQLAlchemy estén correctos"""
    print("\n[3] Verificando modelos SQLAlchemy...")
    try:
        from app.modules.usuarios.models.usuario_models import Persona1, Usuario, Rol, Permiso
        from app.modules.bitacora.models.bitacora_models import Bitacora
        try:
            from app.modules.usuarios.models.usuario_models import LoginLog
            print("  ✓ LoginLog importado correctamente")
        except ImportError:
            print("  ⚠ LoginLog no existe, saltando verificación")
        print("  ✓ Modelos de usuarios importados correctamente")
        print("  ✓ Modelos de bitácora importados correctamente")
        return True
    except Exception as e:
        print(f"  ✗ Error en modelos: {e}")
        return False


def check_services():
    """Verifica que los servicios estén correctos"""
    print("\n[4] Verificando servicios...")
    try:
        from app.modules.auth.services.auth_service import AuthService
        from app.modules.usuarios.services import usuario_service
        print("  ✓ AuthService importado correctamente")
        print("  ✓ UsuarioService importado correctamente")
        return True
    except Exception as e:
        print(f"  ✗ Error en servicios: {e}")
        return False

def check_dtos():
    """Verifica que los DTOs estén correctos"""
    print("\n[5] Verificando DTOs (Pydantic)...")
    try:
        from app.modules.auth.dto.auth_dto import LoginDTO, TokenResponseDTO
        from app.modules.usuarios.dto.usuario_dto import PersonaCreateDTO, UsuarioCreateDTO
        print("  ✓ Auth DTOs importados correctamente")
        print("  ✓ Usuario DTOs importados correctamente")
        return True
    except Exception as e:
        print(f"  ✗ Error en DTOs: {e}")
        return False

def check_decorators():
    """Verifica que los decoradores funcionen"""
    print("\n[6] Verificando decoradores...")
    try:
        from app.shared.decorators.auth_decorators import require_auth, require_roles
        print("  ✓ Decoradores de autenticación importados correctamente")
        return True
    except Exception as e:
        print(f"  ✗ Error en decoradores: {e}")
        return False

def main():
    print("=" * 60)
    print("VERIFICADOR DE BACKEND FASTAPI")
    print("=" * 60)
    
    checks = [
        check_imports,
        check_database_connection,
        check_models,
        check_services,
        check_dtos,
        check_decorators,
        # check_tables_exist,  <-- eliminado para no tocar la BD
    ]
    
    results = []
    for check in checks:
        try:
            results.append(check())
        except Exception as e:
            print(f"  ✗ Error inesperado: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"RESUMEN: {sum(results)}/{len(results)} verificaciones pasadas")
    print("=" * 60)
    
    if all(results):
        print("\n✓ ¡Todo está listo! Tu backend está funcionando correctamente.")
        print("\nPara iniciar el servidor:")
        print("  python run.py")
        sys.exit(0)
    else:
        print("\n✗ Hay problemas que necesitan ser resueltos.")
        sys.exit(1)

if __name__ == "__main__":
    main()
