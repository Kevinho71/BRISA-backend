"""
Decoradores compartidos para autenticación y autorización

Los equipos pueden importar estos decoradores para proteger sus endpoints.
El equipo del Módulo 1 implementará la lógica completa.
"""

from app.shared.decorators.auth_decorators import (
    require_permissions,
    require_roles,
    get_current_user,
    require_auth,
    get_token_from_request
)

__all__ = [
    "require_permissions",
    "require_roles",
    "get_current_user",
    "require_auth",
    "get_token_from_request"
]