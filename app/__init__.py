import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import config
from app.core.extensions import init_extensions

def create_app(config_name=None):
    """
    Factory para crear la aplicación FastAPI del sistema BRISA
    
    Args:
        config_name: Nombre de la configuración a usar
    
    Returns:
        FastAPI: Instancia de la aplicación configurada
    """
    # Obtener configuración del entorno
    if config_name is None:
        config_name = os.environ.get('ENV', 'development')
    
    # Crear instancia de FastAPI
    app = FastAPI(
        title="BRISA Backend API",
        description="Sistema de Gestión Académica",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Obtener config
    app_config = config[config_name]
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Cambiar según ambiente
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Inicializar extensiones (base de datos, etc)
    init_extensions(app)
    
    # Registrar rutas
    register_routes(app)
    
    return app

def register_routes(app):
    """Registrar todas las rutas de la aplicación"""
    
    # Health check
    from app.modules.health.routes import health_router
    app.include_router(health_router, prefix="/api")
    
    # Retiros Tempranos
    from app.modules.retiros_tempranos.controllers.autorizacion_retiro_controller import router as autorizacion_router
    from app.modules.retiros_tempranos.controllers.motivo_retiro_controller import router as motivo_router
    from app.modules.retiros_tempranos.controllers.registro_salida_controller import router as registro_router
    from app.modules.retiros_tempranos.controllers.solicitud_retiro_controller import router as solicitud_router
    from app.modules.retiros_tempranos.controllers.estudiante_apoderado_controller import router as estudiante_apoderado_router
    
    app.include_router(autorizacion_router, tags=["Retiros Tempranos - Autorizaciones"])
    app.include_router(motivo_router, tags=["Retiros Tempranos - Motivos"])
    app.include_router(registro_router, tags=["Retiros Tempranos - Registros"])
    app.include_router(solicitud_router, tags=["Retiros Tempranos - Solicitudes"])
    app.include_router(estudiante_apoderado_router, tags=["Retiros Tempranos - Relaciones"])
    
    # Los módulos específicos serán implementados por cada equipo
    # Ejemplo de cómo registrar un módulo:
    # from app.modules.usuarios.controllers.usuario_controller import usuarios_router
    # app.include_router(usuarios_router, prefix="/api", tags=["Usuarios"])

# Import de modelos para SQLAlchemy
# Los equipos agregarán sus imports aquí cuando implementen sus módulos
# Ejemplo:
# from app.modules.usuarios.models.usuario_models import *