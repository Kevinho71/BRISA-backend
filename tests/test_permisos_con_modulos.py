"""
Script de prueba para verificar el sistema de permisos con módulos

Guarda este archivo como: tests/test_permisos_con_modulos.py

Para ejecutar:
    pytest tests/test_permisos_con_modulos.py -v
"""

import sys
sys.path.append('..')

from app.modules.usuarios.models.usuario_models import Usuario, Rol, Permiso
from app.shared.permission_mapper import (
    tiene_permiso,
    obtener_permisos_usuario,
    obtener_permisos_por_modulo,
    obtener_modulos_permitidos,
    puede_acceder_modulo,
    es_administrador
)


def crear_usuario_mock_profesor():
    """
    Simular un Profesor según tu BD:
    - Puede ver/agregar/modificar ESQUELAS
    - Puede ver/agregar/modificar INCIDENTES
    - Puede ver/agregar/modificar PROFESORES
    """
    # Crear permisos
    p_leer_esquelas = Permiso(
        id_permiso=5,
        nombre="Lectura",
        modulo="esquelas",
        is_active=True
    )
    p_agregar_esquelas = Permiso(
        id_permiso=6,
        nombre="Agregar",
        modulo="esquelas",
        is_active=True
    )
    p_modificar_esquelas = Permiso(
        id_permiso=7,
        nombre="Modificar",
        modulo="esquelas",
        is_active=True
    )
    
    p_leer_incidentes = Permiso(
        id_permiso=9,
        nombre="Lectura",
        modulo="incidentes",
        is_active=True
    )
    p_agregar_incidentes = Permiso(
        id_permiso=10,
        nombre="Agregar",
        modulo="incidentes",
        is_active=True
    )
    p_modificar_incidentes = Permiso(
        id_permiso=11,
        nombre="Modificar",
        modulo="incidentes",
        is_active=True
    )
    
    p_leer_profesores = Permiso(
        id_permiso=21,
        nombre="Lectura",
        modulo="profesores",
        is_active=True
    )
    p_agregar_profesores = Permiso(
        id_permiso=22,
        nombre="Agregar",
        modulo="profesores",
        is_active=True
    )
    p_modificar_profesores = Permiso(
        id_permiso=23,
        nombre="Modificar",
        modulo="profesores",
        is_active=True
    )
    
    # Crear rol Profesor
    rol_profesor = Rol(
        id_rol=2,
        nombre="Profesor",
        is_active=True,
        permisos=[
            p_leer_esquelas, p_agregar_esquelas, p_modificar_esquelas,
            p_leer_incidentes, p_agregar_incidentes, p_modificar_incidentes,
            p_leer_profesores, p_agregar_profesores, p_modificar_profesores
        ]
    )
    
    # Crear usuario
    usuario = Usuario(
        id_usuario=1,
        usuario="jperez",
        is_active=True,
        roles=[rol_profesor]
    )
    
    return usuario


def crear_usuario_mock_recepcion():
    """
    Simular Recepción según tu BD:
    - Solo puede ver/agregar RETIROS TEMPRANOS
    """
    p_leer_retiros = Permiso(
        id_permiso=13,
        nombre="Lectura",
        modulo="retiros_tempranos",
        is_active=True
    )
    p_agregar_retiros = Permiso(
        id_permiso=14,
        nombre="Agregar",
        modulo="retiros_tempranos",
        is_active=True
    )
    
    rol_recepcion = Rol(
        id_rol=7,
        nombre="Recepción",
        is_active=True,
        permisos=[p_leer_retiros, p_agregar_retiros]
    )
    
    usuario = Usuario(
        id_usuario=2,
        usuario="mgarcia",
        is_active=True,
        roles=[rol_recepcion]
    )
    
    return usuario


def crear_usuario_mock_director():
    """Simular Director con acceso total"""
    rol_director = Rol(
        id_rol=1,
        nombre="Director",
        is_active=True,
        permisos=[]  # No necesita permisos específicos, es admin
    )
    
    usuario = Usuario(
        id_usuario=3,
        usuario="director",
        is_active=True,
        roles=[rol_director]
    )
    
    return usuario


def test_profesor_permisos():
    """Probar que el Profesor tiene los permisos correctos"""
    print("\n" + "="*60)
    print("TEST 1: Permisos de PROFESOR")
    print("="*60)
    
    profesor = crear_usuario_mock_profesor()
    
    # Debe tener acceso a esquelas
    assert tiene_permiso(profesor, "ver_esquela"), "❌ Profesor debería poder ver esquelas"
    assert tiene_permiso(profesor, "crear_esquela"), "❌ Profesor debería poder crear esquelas"
    assert tiene_permiso(profesor, "editar_esquela"), "❌ Profesor debería poder editar esquelas"
    print("✅ Profesor PUEDE acceder a módulo ESQUELAS")
    
    # Debe tener acceso a incidentes
    assert tiene_permiso(profesor, "ver_incidente"), "❌ Profesor debería poder ver incidentes"
    assert tiene_permiso(profesor, "crear_incidente"), "❌ Profesor debería poder crear incidentes"
    print("✅ Profesor PUEDE acceder a módulo INCIDENTES")
    
    # NO debe tener acceso a usuarios
    assert not tiene_permiso(profesor, "ver_usuario"), "❌ Profesor NO debería poder ver usuarios"
    assert not tiene_permiso(profesor, "crear_usuario"), "❌ Profesor NO debería poder crear usuarios"
    print("✅ Profesor NO PUEDE acceder a módulo USUARIOS")
    
    # Verificar módulos permitidos
    modulos = obtener_modulos_permitidos(profesor)
    assert "esquelas" in modulos, "❌ Falta módulo esquelas"
    assert "incidentes" in modulos, "❌ Falta módulo incidentes"
    assert "profesores" in modulos, "❌ Falta módulo profesores"
    assert "usuarios" not in modulos, "❌ No debería tener módulo usuarios"
    print(f"✅ Módulos permitidos: {modulos}")
    
    # Verificar permisos agrupados
    permisos_agrupados = obtener_permisos_por_modulo(profesor)
    print(f"✅ Permisos por módulo: {permisos_agrupados}")


def test_recepcion_permisos():
    """Probar que Recepción solo tiene acceso a retiros tempranos"""
    print("\n" + "="*60)
    print("TEST 2: Permisos de RECEPCIÓN")
    print("="*60)
    
    recepcion = crear_usuario_mock_recepcion()
    
    # Debe tener acceso a retiros
    assert tiene_permiso(recepcion, "ver_retiro"), "❌ Recepción debería poder ver retiros"
    assert tiene_permiso(recepcion, "crear_retiro"), "❌ Recepción debería poder crear retiros"
    print("✅ Recepción PUEDE acceder a módulo RETIROS TEMPRANOS")
    
    # NO debe tener acceso a otros módulos
    assert not tiene_permiso(recepcion, "ver_esquela"), "❌ Recepción NO debería ver esquelas"
    assert not tiene_permiso(recepcion, "ver_usuario"), "❌ Recepción NO debería ver usuarios"
    assert not tiene_permiso(recepcion, "ver_incidente"), "❌ Recepción NO debería ver incidentes"
    print("✅ Recepción NO PUEDE acceder a otros módulos")
    
    # Verificar módulos
    modulos = obtener_modulos_permitidos(recepcion)
    assert modulos == ["retiros_tempranos"], f"❌ Debería tener solo retiros_tempranos, tiene: {modulos}"
    print(f"✅ Módulos permitidos: {modulos}")


def test_director_acceso_total():
    """Probar que el Director tiene acceso total"""
    print("\n" + "="*60)
    print("TEST 3: Permisos de DIRECTOR (Admin)")
    print("="*60)
    
    director = crear_usuario_mock_director()
    
    # Verificar que es administrador
    assert es_administrador(director), "❌ Director debería ser identificado como admin"
    print("✅ Director ES administrador")
    
    # Debe tener acceso a TODOS los módulos
    assert tiene_permiso(director, "ver_usuario"), "❌ Director debería ver usuarios"
    assert tiene_permiso(director, "crear_usuario"), "❌ Director debería crear usuarios"
    assert tiene_permiso(director, "ver_esquela"), "❌ Director debería ver esquelas"
    assert tiene_permiso(director, "ver_incidente"), "❌ Director debería ver incidentes"
    assert tiene_permiso(director, "ver_retiro"), "❌ Director debería ver retiros"
    assert tiene_permiso(director, "generar_reportes"), "❌ Director debería generar reportes"
    print("✅ Director TIENE ACCESO TOTAL a todos los módulos")


def test_acceso_modulo():
    """Probar función puede_acceder_modulo"""
    print("\n" + "="*60)
    print("TEST 4: Función puede_acceder_modulo()")
    print("="*60)
    
    profesor = crear_usuario_mock_profesor()
    recepcion = crear_usuario_mock_recepcion()
    
    # Profesor puede acceder a esquelas
    assert puede_acceder_modulo(profesor, "esquelas"), "❌ Profesor debería acceder a esquelas"
    assert puede_acceder_modulo(profesor, "incidentes"), "❌ Profesor debería acceder a incidentes"
    print("✅ Profesor puede acceder a sus módulos")
    
    # Profesor NO puede acceder a usuarios
    assert not puede_acceder_modulo(profesor, "usuarios"), "❌ Profesor NO debería acceder a usuarios"
    print("✅ Profesor NO puede acceder a usuarios")
    
    # Recepción solo a retiros
    assert puede_acceder_modulo(recepcion, "retiros_tempranos"), "❌ Recepción debería acceder a retiros"
    assert not puede_acceder_modulo(recepcion, "esquelas"), "❌ Recepción NO debería acceder a esquelas"
    print("✅ Recepción solo accede a retiros tempranos")


if __name__ == "__main__":
    print("\n" + "🧪 INICIANDO PRUEBAS DE SISTEMA DE PERMISOS CON MÓDULOS".center(80, "="))
    
    try:
        test_profesor_permisos()
        test_recepcion_permisos()
        test_director_acceso_total()
        test_acceso_modulo()
        
        print("\n" + "="*80)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE".center(80))
        print("="*80 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ PRUEBA FALLÓ: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}\n")
        raise