"""
Modelos compartidos entre módulos
"""

from .base_models import BaseModel
from .persona import Persona, TipoPersonaEnum
from .profesor_curso_materia import ProfesorCursoMateria

__all__ = [
    "BaseModel",
    "Persona",
    "TipoPersonaEnum",
    "ProfesorCursoMateria",
]