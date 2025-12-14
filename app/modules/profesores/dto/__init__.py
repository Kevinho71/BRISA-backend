# Profesores y Materias - dto
# app/modules/profesores/dtos/__init__.py
"""
DTOs del módulo de profesores
"""
from .profesor_dto import (
    ProfesorCreateDTO,
    ProfesorUpdateDTO,
    ProfesorResponseDTO,
    AsignarCursoMateriaDTO,
    ProfesorCursoMateriaResponseDTO,
    NivelEnsenanzaEnum,
    EstadoLaboralEnum
)

__all__ = [
    "ProfesorCreateDTO",
    "ProfesorUpdateDTO",
    "ProfesorResponseDTO",
    "AsignarCursoMateriaDTO",
    "ProfesorCursoMateriaResponseDTO",
    "NivelEnsenanzaEnum",
    "EstadoLaboralEnum"
]