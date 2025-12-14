"""
Script de prueba para los endpoints de profesores
Ejecutar con: python test_profesores.py
Funciona desde cualquier carpeta gracias al ajuste del path
"""

import requests
import json
import sys
import os

# ===================================================================
# Ajuste automático del path para encontrar el módulo 'app' (si lo necesitas en el futuro)
# ===================================================================
# Si en algún momento quieres importar desde tu proyecto (ej. models, config), descomenta esto:
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.append(project_root)

# ===================================================================
# Configuración
# ===================================================================
BASE_URL = "http://localhost:8000/api"

# ⚠️ ACTUALIZA ESTE TOKEN CON UNO VÁLIDO Y RECIENTE
# Si el token ha expirado, haz login manualmente y copia el nuevo access_token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMSIsInVzdWFyaW9faWQiOjMxLCJ1c3VhcmlvIjoiQWRtaW4yMDI1IiwiZXhwIjoxNzY1NTcwMzY0fQ.ucP2_7xjQlpzMjN_yJi47m0Yt7Yn3Y5N9EICVFlPwUk"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# ===================================================================
# Funciones de prueba
# ===================================================================
def test_crear_profesor():
    """Prueba crear un profesor"""
    print("\n=== TEST: Crear Profesor ===")
    data = {
        "ci": "1234567901231",
        "nombres": "Juan Carlos",
        "apellido_paterno": "Pérez",
        "apellido_materno": "García",
        "direccion": "Av. Principal 123",
        "telefono": "77712345",
        "correo": "juan.perez@colegio.edu.bo",
        "especialidad": "Matemáticas",
        "titulo_academico": "Licenciado en Matemáticas",
        "nivel_enseñanza": "secondary",
        "anos_experiencia": 5
    }
    
    response = requests.post(f"{BASE_URL}/profesores", json=data, headers=HEADERS)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")
    
    if response.status_code == 201:
        return response.json().get("id_profesor")
    else:
        return None


def test_obtener_profesores():
    """Prueba obtener todos los profesores"""
    print("\n=== TEST: Obtener Profesores ===")
    response = requests.get(f"{BASE_URL}/profesores", headers=HEADERS)
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Total profesores: {len(data)}")
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")


def test_obtener_profesor(id_profesor):
    """Prueba obtener un profesor específico"""
    print(f"\n=== TEST: Obtener Profesor {id_profesor} ===")
    response = requests.get(f"{BASE_URL}/profesores/{id_profesor}", headers=HEADERS)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")


def test_actualizar_profesor(id_profesor):
    """Prueba actualizar un profesor"""
    print(f"\n=== TEST: Actualizar Profesor {id_profesor} ===")
    data = {
        "telefono": "77799999",
        "especialidad": "Física y Matemáticas",
        "anos_experiencia": 7
    }
    
    response = requests.put(f"{BASE_URL}/profesores/{id_profesor}", json=data, headers=HEADERS)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")


def test_asignar_curso_materia(id_profesor):
    """Prueba asignar curso y materia"""
    print(f"\n=== TEST: Asignar Curso y Materia al Profesor {id_profesor} ===")
    data = {
        "id_profesor": id_profesor,
        "id_curso": 1,      # Ajusta si es necesario
        "id_materia": 1    # Ajusta si es necesario
    }
    
    response = requests.post(f"{BASE_URL}/profesores/asignar-curso-materia", json=data, headers=HEADERS)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")


def test_obtener_asignaciones(id_profesor):
    """Prueba obtener asignaciones del profesor"""
    print(f"\n=== TEST: Obtener Asignaciones del Profesor {id_profesor} ===")
    response = requests.get(f"{BASE_URL}/profesores/{id_profesor}/asignaciones", headers=HEADERS)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")


def test_eliminar_asignacion(id_profesor, id_curso=1, id_materia=1):
    """Prueba eliminar una asignación"""
    print("\n=== TEST: Eliminar Asignación ===")
    url = f"{BASE_URL}/profesores/{id_profesor}/asignaciones/{id_curso}/{id_materia}"
    response = requests.delete(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    if response.status_code != 204:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Response (text): {response.text}")
    else:
        print("Asignación eliminada correctamente (204 No Content)")


def test_eliminar_profesor(id_profesor):
    """Prueba eliminar un profesor (opcional)"""
    print(f"\n=== TEST: Eliminar Profesor {id_profesor} ===")
    response = requests.delete(f"{BASE_URL}/profesores/{id_profesor}", headers=HEADERS)
    print(f"Status: {response.status_code}")
    if response.status_code != 204:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Response (text): {response.text}")
    else:
        print("Profesor eliminado correctamente")


# ===================================================================
# Ejecución principal
# ===================================================================
def main():
    print("🧪 INICIANDO PRUEBAS DEL MÓDULO DE PROFESORES 🧪")
    
    # 1. Crear profesor
    id_profesor = test_crear_profesor()
    
    if not id_profesor:
        print("❌ Error al crear profesor. Deteniendo pruebas.")
        return
    
    # 2. Listar todos
    test_obtener_profesores()
    
    # 3. Obtener específico
    test_obtener_profesor(id_profesor)
    
    # 4. Actualizar
    test_actualizar_profesor(id_profesor)
    
    # 5. Asignar curso/materia
    test_asignar_curso_materia(id_profesor)
    
    # 6. Ver asignaciones
    test_obtener_asignaciones(id_profesor)
    
    # 7. Eliminar asignación
    test_eliminar_asignacion(id_profesor, id_curso=1, id_materia=1)
    
    # 8. Verificar que se eliminó
    test_obtener_asignaciones(id_profesor)
    
    # 9. (Opcional) Eliminar profesor creado
    # test_eliminar_profesor(id_profesor)
    
    print("\n✅ PRUEBAS COMPLETADAS ✅")


if __name__ == "__main__":
    main()