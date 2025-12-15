# Profesores y Materias - models
# app/modules/profesores/models/__init__.py
"""
Modelos del módulo de profesores
"""
from .profesor_models import Profesor
from app.shared.models import ProfesorCursoMateria

__all__ = ["Profesor", "ProfesorCursoMateria"]