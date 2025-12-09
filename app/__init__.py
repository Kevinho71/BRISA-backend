# app\__init__.py
import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import config
from app.core.extensions import init_extensions
from app.modules.esquelas import esquelas_router
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
        # Soportar ambas variables de entorno: ENV y APP_ENV
        config_name = os.environ.get('ENV')
    
    # Crear instancia de FastAPI
    app = FastAPI(
        title="BRISA Backend API",
        description="Sistema de Gestión Académica",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Obtener config e inyectarla en la app para que las extensiones la lean
    # config es un dict que mapea nombre -> clase de configuración
    app_config_class = config[config_name]
    app.config = app_config_class()
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Cambiar según ambiente
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Inicializar extensiones (base de datos, etc) usando la configuración cargada
    init_extensions(app)
    
    # Registrar rutas
    register_routes(app)
    
    return app

def register_routes(app):
    """Registrar todas las rutas de la aplicación"""

    # Health check
    from app.modules.health.routes import health_router
    app.include_router(health_router, prefix="/api")
    
    # Esquelas (de main)
    from app.modules.esquelas import esquelas_router, codigos_esquelas_router
    app.include_router(esquelas_router, prefix="/api", tags=["Esquelas"])
    app.include_router(codigos_esquelas_router, prefix="/api", tags=["Códigos de Esquela"])
    
    # Cursos (de main)
    from app.modules.administracion.controllers.curso_controller import router as cursos_router
    app.include_router(cursos_router, prefix="/api", tags=["Courses"])
    
    # Estudiantes (de main - consultas de esquelas)
    from app.modules.administracion.controllers.estudiante_controller import router as estudiantes_router
    app.include_router(estudiantes_router, prefix="/api", tags=["Students"])
    
    # Reportes (de main)
    from app.modules.reportes.controllers.reporte_controller import router as reportes_router
    app.include_router(reportes_router, prefix="/api", tags=["Reports"])
    
    # Incidentes
    from app.modules.incidentes.controllers.controllers_incidentes import router as reportes_router
    app.include_router(reportes_router, prefix="/api", tags=["Incidentes"])
    
    # Administración (Personas)
    from app.modules.administracion import (
        estudiantes_router as admin_estudiantes_router,
        profesores_router,
        registradores_router
    )
    app.include_router(admin_estudiantes_router, prefix="/api", tags=["Estudiantes"])
    app.include_router(profesores_router, prefix="/api", tags=["Profesores"])
    app.include_router(registradores_router, prefix="/api", tags=["Registradores"])
    
    # ✅ Retiros Tempranos (TU MÓDULO - CONSERVADO)
    from app.modules.retiros_tempranos.controllers.autorizacion_retiro_controller import router as autorizacion_router
    from app.modules.retiros_tempranos.controllers.motivo_retiro_controller import router as motivo_router
    from app.modules.retiros_tempranos.controllers.registro_salida_controller import router as registro_router
    from app.modules.retiros_tempranos.controllers.solicitud_retiro_controller import router as solicitud_router
    from app.modules.retiros_tempranos.controllers.estudiante_apoderado_controller import router as estudiante_apoderado_router
    from app.modules.incidentes.controllers.controllers_incidentes import router as reportes_router
    app.include_router(reportes_router, prefix="/api", tags=["Incidentes"])
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

# Modelos de Esquelas
from app.modules.esquelas.models.esquela_models import Esquela, CodigoEsquela

# Modelos de Administración (Personas, Cursos, Estudiantes)
from app.modules.administracion.models.persona_models import Estudiante
from app.shared.models.persona import Persona
from app.modules.estudiantes.models.Curso import Curso
from app.modules.estudiantes.models.Materia import Materia