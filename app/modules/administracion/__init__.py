"""Módulo de Administración de Personas (Estudiantes, Profesores, Registradores)

Expone los routers para que puedan ser importados desde app.modules.administracion
"""

from .controllers.persona_controller import (
    estudiantes_router,
    profesores_router,
    registradores_router
)

__all__ = [
    "estudiantes_router",
    "profesores_router",
    "registradores_router"
]
