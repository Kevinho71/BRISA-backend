"""
Modelos compartidos entre módulos
"""

from .base_models import BaseModel
from .persona import Persona, TipoPersonaEnum
from .cargo import Cargo
from .profesor_curso_materia import ProfesorCursoMateria

__all__ = [
    "BaseModel",
    "Persona",
    "TipoPersonaEnum",
    "Cargo",
    "ProfesorCursoMateria",
]