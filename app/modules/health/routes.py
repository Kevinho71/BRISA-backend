from flask import Blueprint, jsonify
from datetime import datetime
import os
from app.core.utils import success_response

# Crear blueprint para health
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
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
        'environment': os.environ.get('FLASK_ENV', 'development'),
        'uptime': 'running'
    }
    
    return success_response(
        data=health_data,
        message="API is running successfully"
    )

@health_bp.route('/status', methods=['GET'])
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
            'type': 'sqlite'
        },
        'modules': {
            'equipo1': 'active',
            'equipo2': 'active',
            'equipo3': 'active'
        },
        'system': {
            'timestamp': datetime.utcnow().isoformat(),
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
        }
    }
    
    return success_response(
        data=status_data,
        message="Detailed system status"
    )