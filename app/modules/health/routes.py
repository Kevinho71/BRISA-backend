from fastapi import APIRouter
from datetime import datetime
import os
from app.core.utils import success_response

# Crear router para health
health_router = APIRouter(tags=["Health"])

@health_router.get('/health')
def health_check():
    """
    Endpoint para verificar el estado de la API
    
    Returns:
        JSON: Estado de la API y información del sistema
    """
    health_data = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'service': 'BRISA Backend API',
        'environment': os.environ.get('ENV', 'development'),
        'uptime': 'running'
    }
    
    return success_response(
        data=health_data,
        message="API is running successfully"
    )

@health_router.get('/status')
def detailed_status():
    """
    Endpoint con información detallada del estado
    
    Returns:
        JSON: Estado detallado del sistema
    """
    status_data = {
        'api': {
            'status': 'online',
            'version': '1.0.0',
            'name': 'BRISA Backend API'
        },
        'database': {
            'status': 'connected',
            'type': 'mysql'
        },
        'modules': {
            'usuarios': 'pending',
            'estudiantes': 'pending',
            'profesores': 'pending',
            'retiros_tempranos': 'pending',
            'incidentes': 'pending',
            'esquelas': 'pending',
            'administracion': 'pending',
            'reportes': 'pending'
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return success_response(
        data=status_data,
        message="System status retrieved successfully"
    )