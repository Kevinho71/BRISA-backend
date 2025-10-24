# app/modules/administracion/controllers/persona_controller.py
"""Controladores (routers) para personas"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.extensions import get_db
from app.modules.administracion.services.persona_service import (
    EstudianteService,
    ProfesorService,
    RegistradorService
)
from app.modules.administracion.dto.persona_dto import (
    EstudianteResponseDTO,
    PersonaResponseDTO
)


# Router para estudiantes
estudiantes_router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@estudiantes_router.get("/", response_model=List[EstudianteResponseDTO])
def listar_estudiantes(db: Session = Depends(get_db)):
    """Obtener todos los estudiantes para selección en formularios"""
    return EstudianteService.listar_estudiantes(db)


@estudiantes_router.get("/{id_estudiante}", response_model=EstudianteResponseDTO)
def obtener_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    """Obtener un estudiante por ID"""
    return EstudianteService.obtener_estudiante(db, id_estudiante)


# Router para profesores
profesores_router = APIRouter(prefix="/profesores", tags=["Profesores"])


@profesores_router.get("/", response_model=List[PersonaResponseDTO])
def listar_profesores(db: Session = Depends(get_db)):
    """Obtener todos los profesores para selección en formularios"""
    return ProfesorService.listar_profesores(db)


@profesores_router.get("/{id_persona}", response_model=PersonaResponseDTO)
def obtener_profesor(id_persona: int, db: Session = Depends(get_db)):
    """Obtener un profesor por ID"""
    return ProfesorService.obtener_profesor(db, id_persona)


# Router para registradores
registradores_router = APIRouter(prefix="/registradores", tags=["Registradores"])


@registradores_router.get("/", response_model=List[PersonaResponseDTO])
def listar_registradores(db: Session = Depends(get_db)):
    """Obtener todos los registradores para selección en formularios"""
    return RegistradorService.listar_registradores(db)


@registradores_router.get("/{id_persona}", response_model=PersonaResponseDTO)
def obtener_registrador(id_persona: int, db: Session = Depends(get_db)):
    """Obtener un registrador por ID"""
    return RegistradorService.obtener_registrador(db, id_persona)
