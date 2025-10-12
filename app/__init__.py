import os
from flask import Flask, jsonify
from datetime import datetime
from app.config.config import config
from app.core.extensions import init_extensions

def create_app(config_name=None):
    """
    Factory para crear la aplicación Flask del sistema BRISA
    
    Args:
        config_name: Nombre de la configuración a usar
    
    Returns:
        Flask: Instancia de la aplicación configurada
    """
    # Obtener configuración del entorno
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    # Registrar comandos CLI
    register_commands(app)
    
    return app

def register_blueprints(app):
    """Registrar todos los blueprints de la aplicación"""
    
    # Health check
    from app.modules.health.routes import health_bp
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Los módulos específicos serán implementados por cada equipo
    # Ejemplo de cómo registrar un módulo:
    # from app.modules.usuarios.controllers.usuario_controller import usuarios_bp
    # app.register_blueprint(usuarios_bp, url_prefix='/api')

def register_error_handlers(app):
    """Registrar manejadores de errores globales"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'timestamp': datetime.utcnow().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

def register_commands(app):
    """Registrar comandos CLI personalizados"""
    
    @app.cli.command()
    def init_db():
        """Inicializar base de datos"""
        from app.core.extensions import db
        db.create_all()
        print('✅ Database initialized!')
    
    @app.cli.command()
    def reset_db():
        """Resetear base de datos"""
        from app.core.extensions import db
        db.drop_all()
        db.create_all()
        print('🔄 Database reset!')

# Import de modelos para SQLAlchemy
# Los equipos agregarán sus imports aquí cuando implementen sus módulos
# Ejemplo:
# from app.modules.usuarios.models.usuario_models import *