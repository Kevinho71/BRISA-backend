"""
Tests de flujo completo para retiros tempranos
Ejecuta: pytest tests/test_retiros_tempranos_flow.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Variables globales para IDs
TOKEN_RECEPCIONISTA = None
TOKEN_REGENTE = None
TOKEN_APODERADO = None
ID_SOLICITUD_MASIVA = None
ID_AUTORIZACION = None


@pytest.fixture(scope="module")
def setup_tokens():
    """Obtener tokens de autenticación"""
    global TOKEN_RECEPCIONISTA, TOKEN_REGENTE, TOKEN_APODERADO
    
    # Login recepcionista
    response = client.post("/api/auth/login", json={
        "usuario": "recepcionista1",
        "password": "W2ETpXygIQsw"
    })
    assert response.status_code == 200, f"Login falló: {response.json()}"
    TOKEN_RECEPCIONISTA = response.json()["data"]["access_token"]
    
    # Login regente
    response = client.post("/api/auth/login", json={
        "usuario": "regente1",
        "password": "TmANpg@Zalxy"
    })
    assert response.status_code == 200, f"Login falló: {sponse.json()}"
    TOKEN_REGENTE = response.json()["data"]["access_token"]
    
    # Login apoderado
    response = client.post("/api/auth/login", json={
        "usuario": "apoderado1",
        "password": "LLXjVp9SdbQN"
    })
    assert response.status_code == 200, f"Login falló: {response.json()}"
    TOKEN_APODERADO = response.json()["data"]["access_token"]


def test_01_crear_solicitud_masiva(setup_tokens):
    """Test: Crear solicitud masiva"""
    global ID_SOLICITUD_MASIVA
    
    response = client.post(
        "/api/retiros-tempranos/solicitudes-masivas/",
        headers={"Authorization": f"Bearer {TOKEN_RECEPCIONISTA}"},
        json={
            "id_motivo": 1,
            "fecha_hora_salida": "2025-12-16T09:00:00",
            "fecha_hora_retorno_previsto": "2025-12-16T15:00:00",
            "foto_evidencia": "https://ejemplo.com/foto.jpg",
            "observacion": "Excursión educativa",
            "estudiantes": [
                {"id_estudiante": 1, "observacion_individual": None}
            ]
        }
    )
    
    print(f"\n✓ Crear solicitud masiva: {response.status_code}")
    assert response.status_code == 201
    ID_SOLICITUD_MASIVA = response.json()["id_solicitud"]
    print(f"  ID Solicitud: {ID_SOLICITUD_MASIVA}")


def test_02_listar_solicitudes_recibidas(setup_tokens):
    """Test: Listar solicitudes recibidas"""
    response = client.get(
        "/api/retiros-tempranos/solicitudes-masivas/recibidas",
        headers={"Authorization": f"Bearer {TOKEN_RECEPCIONISTA}"}
    )
    
    print(f"\n✓ Listar recibidas: {response.status_code}")
    assert response.status_code == 200
    print(f"  Total recibidas: {len(response.json())}")


def test_03_derivar_solicitud(setup_tokens):
    """Test: Derivar solicitud al regente"""
    response = client.put(
        f"/api/retiros-tempranos/solicitudes-masivas/{ID_SOLICITUD_MASIVA}/derivar",
        headers={"Authorization": f"Bearer {TOKEN_RECEPCIONISTA}"},
        json={
            "observacion_derivacion": "Derivado para aprobación"
        }
    )
    
    print(f"\n✓ Derivar solicitud: {response.status_code}")
    assert response.status_code == 200


def test_04_listar_solicitudes_derivadas(setup_tokens):
    """Test: Listar solicitudes derivadas (regente)"""
    response = client.get(
        "/api/retiros-tempranos/solicitudes-masivas/derivadas",
        headers={"Authorization": f"Bearer {TOKEN_REGENTE}"}
    )
    
    print(f"\n✓ Listar derivadas: {response.status_code}")
    assert response.status_code == 200
    print(f"  Total derivadas: {len(response.json())}")


def test_05_aprobar_solicitud_masiva(setup_tokens):
    """Test: Aprobar solicitud masiva"""
    global ID_AUTORIZACION
    
    response = client.put(
        f"/api/autorizaciones-retiro/masiva/{ID_SOLICITUD_MASIVA}/decision",
        headers={"Authorization": f"Bearer {TOKEN_REGENTE}"},
        json={
            "decision": "aprobada",
            "motivo_decision": "Actividad educativa válida"
        }
    )
    
    print(f"\n✓ Aprobar solicitud: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    print(f"  Estado: {data.get('estado')}")
    ID_AUTORIZACION = data.get('id_autorizacion')


def test_06_obtener_solicitud_detallada(setup_tokens):
    """Test: Obtener solicitud con detalles"""
    response = client.get(
        f"/api/retiros-tempranos/solicitudes-masivas/{ID_SOLICITUD_MASIVA}",
        headers={"Authorization": f"Bearer {TOKEN_RECEPCIONISTA}"}
    )
    
    print(f"\n✓ Obtener detalle: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    print(f"  Estado: {data.get('estado')}")
    print(f"  Estudiantes: {len(data.get('estudiantes', []))}")


# Test de endpoints de consulta general
def test_07_listar_todas_solicitudes(setup_tokens):
    """Test: Listar todas las solicitudes"""
    response = client.get(
        "/api/retiros-tempranos/solicitudes-masivas/",
        headers={"Authorization": f"Bearer {TOKEN_RECEPCIONISTA}"}
    )
    
    print(f"\n✓ Listar todas: {response.status_code}")
    assert response.status_code == 200
    print(f"  Total solicitudes: {len(response.json())}")


def test_08_listar_autorizaciones(setup_tokens):
    """Test: Listar autorizaciones"""
    response = client.get(
        "/api/autorizaciones-retiro/",
        headers={"Authorization": f"Bearer {TOKEN_REGENTE}"}
    )
    
    print(f"\n✓ Listar autorizaciones: {response.status_code}")
    assert response.status_code == 200
    print(f"  Total autorizaciones: {len(response.json())}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
