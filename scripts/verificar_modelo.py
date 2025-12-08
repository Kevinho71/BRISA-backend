"""
verificar_modelo.py - Verifica que el modelo esté correcto
"""
import sys
print("=" * 50)
print("VERIFICANDO MODELO")
print("=" * 50)

# Limpiar imports previos
if 'app.modules.usuarios.models.usuario_models' in sys.modules:
    del sys.modules['app.modules.usuarios.models.usuario_models']

try:
    from app.modules.usuarios.models.usuario_models import Persona1, Usuario
    from sqlalchemy import inspect

    
    # Verificar Persona1
    persona_columns = [col.name for col in Persona1.__table__.columns]
    print("\n✓ Columnas de Persona1:")
    for col in persona_columns:
        print(f"  - {col}")
    
    if 'id_persona' in persona_columns:
        print("\n✅ ¡CORRECTO! id_persona está mapeado en Persona1")
    else:
        print("\n❌ ERROR: id_persona NO está en Persona1")
        sys.exit(1)
    
    # Verificar Usuario
    usuario_columns = [col.name for col in Usuario.__table__.columns]
    print("\n✓ Columnas de Usuario:")
    for col in usuario_columns:
        print(f"  - {col}")
    
    # Verificar relaciones
    print("\n✓ Relaciones de Persona1:")
    for rel in inspect(Persona1).relationships:
        print(f"  - {rel.key} -> {rel.mapper.class_.__name__}")
    
    print("\n✓ Relaciones de Usuario:")
    for rel in inspect(Usuario).relationships:
        print(f"  - {rel.key} -> {rel.mapper.class_.__name__}")
    
    print("\n" + "=" * 50)
    print("✅ MODELO CORRECTO - Puedes ejecutar los tests")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ ERROR AL CARGAR MODELO:")
    print(f"   {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)