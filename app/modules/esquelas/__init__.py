"""Paquete del módulo Esquelas (Reconocimiento y Orientación).

Expone el router principal del módulo como `esquelas_router` para que pueda
ser importado desde `app.modules.esquelas`.
"""

# Importar y exponer el router del controlador principal
from .controllers.esquela_controller import router as esquelas_router
from .controllers.codigo_esquela_controller import router as codigos_esquelas_router

__all__ = ["esquelas_router", "codigos_esquelas_router"]
