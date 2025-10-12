import pytest
from app import create_app
from app.core.extensions import db

@pytest.fixture
def app():
    """Crear aplicación para testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de test"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner de comandos CLI"""
    return app.test_cli_runner()

def test_health_endpoint(client):
    """Test del endpoint de health"""
    response = client.get('/api/health')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['status'] == 'healthy'
    assert data['data']['service'] == 'BRISA Backend API'

def test_status_endpoint(client):
    """Test del endpoint de status detallado"""
    response = client.get('/api/status')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert 'api' in data['data']
    assert 'modules' in data['data']

def test_equipo1_endpoint(client):
    """Test del endpoint del equipo 1"""
    response = client.get('/api/equipo1/')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['module'] == 'Equipo 1'

def test_equipo2_endpoint(client):
    """Test del endpoint del equipo 2"""
    response = client.get('/api/equipo2/')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['module'] == 'Equipo 2'

def test_equipo3_endpoint(client):
    """Test del endpoint del equipo 3"""
    response = client.get('/api/equipo3/')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['module'] == 'Equipo 3'

def test_404_error(client):
    """Test del manejo de errores 404"""
    response = client.get('/api/endpoint-inexistente')
    
    assert response.status_code == 404
    
    data = response.get_json()
    assert data['success'] is False
    assert 'not found' in data['message'].lower()