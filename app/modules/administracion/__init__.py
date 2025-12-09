"""Módulo de Administración de Personas (Estudiantes, Profesores, Registradores, Administrativos)

Expone los routers para que puedan ser importados desde app.modules.administracion
"""

from .controllers.persona_controller import (
    estudiantes_router,
    profesores_router,
    registradores_router
)
from .controllers.administrativo_controller import router as administrativos_router

__all__ = [
    "estudiantes_router",
    "profesores_router",
    "registradores_router",
    "administrativos_router"
]
