"""Controlador (Router) para Asignaciones Estudiante-Curso"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.estudiantes_cursos.services.asignacion_service import AsignacionService
from app.modules.estudiantes_cursos.dto.asignacion_dto import (
    AsignarEstudianteDTO,
    AsignacionResponseDTO,
    EstudiantesDeCursoDTO,
    CursosDeEstudianteDTO,
    GestionesDisponiblesDTO,
    CursosPorGestionDTO,
    EstudiantesParaInscripcionDTO,
    InscripcionMasivaDTO,
    InscripcionMasivaResponseDTO
)


router = APIRouter(prefix="/asignaciones", tags=["Asignaciones Estudiante-Curso"])


# ============= Asignaciones Individuales =============

@router.post("/asignar", response_model=AsignacionResponseDTO, summary="RF-ASG-001: Asignar Estudiante a Curso")
def asignar_estudiante_a_curso(
    datos: AsignarEstudianteDTO,
    db: Session = Depends(get_db)
):
    """
    Asignar un estudiante a un curso específico.
    
    Crea la relación entre estudiante y curso.
    
    **Validaciones:**
    - El estudiante debe existir
    - El curso debe existir
    - No debe existir asignación previa (rechaza duplicados)
    """
    return AsignacionService.asignar_estudiante_a_curso(db, datos)


@router.post("/desasignar", response_model=AsignacionResponseDTO, summary="RF-ASG-002: Desasignar Estudiante de Curso")
def desasignar_estudiante_de_curso(
    datos: AsignarEstudianteDTO,
    db: Session = Depends(get_db)
):
    """
    Retirar a un estudiante de un curso específico.
    
    Elimina la relación entre estudiante y curso.
    
    **Validaciones:**
    - El estudiante debe existir
    - El curso debe existir
    - Debe existir la asignación (rechaza si no existe)
    """
    return AsignacionService.desasignar_estudiante_de_curso(db, datos)


@router.get("/curso/{id_curso}/estudiantes", response_model=EstudiantesDeCursoDTO, summary="RF-ASG-003: Obtener Estudiantes de un Curso")
def obtener_estudiantes_de_curso(
    id_curso: int,
    db: Session = Depends(get_db)
):
    """
    Obtener lista completa de estudiantes asignados a un curso.
    
    Retorna información del curso y lista de estudiantes con datos básicos.
    """
    return AsignacionService.obtener_estudiantes_de_curso(db, id_curso)


@router.get("/estudiante/{id_estudiante}/cursos", response_model=CursosDeEstudianteDTO, summary="RF-ASG-004: Obtener Cursos de un Estudiante")
def obtener_cursos_de_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db)
):
    """
    Obtener lista completa de cursos a los que está asignado un estudiante.
    
    Retorna información del estudiante y lista de cursos con datos completos.
    """
    return AsignacionService.obtener_cursos_de_estudiante(db, id_estudiante)


# ============= Inscripción Masiva =============

@router.get("/gestiones", response_model=GestionesDisponiblesDTO, summary="RF-ASG-005: Obtener Gestiones Disponibles")
def obtener_gestiones_disponibles(db: Session = Depends(get_db)):
    """
    Obtener lista de todas las gestiones (años académicos) con cursos registrados.
    
    Lista ordenada descendentemente (más reciente primero).
    Útil para poblar selectores en interfaces de usuario.
    """
    return AsignacionService.obtener_gestiones_disponibles(db)


@router.get("/gestiones/{gestion}/cursos", response_model=CursosPorGestionDTO, summary="RF-ASG-006: Obtener Cursos por Gestión")
def obtener_cursos_por_gestion(
    gestion: str,
    db: Session = Depends(get_db)
):
    """
    Obtener cursos disponibles de una gestión específica.
    
    Retorna información básica de cursos (ID, nombre, nivel).
    Ordenados por nivel y nombre.
    Útil para seleccionar curso origen en inscripción masiva.
    """
    return AsignacionService.obtener_cursos_por_gestion(db, gestion)


@router.get("/inscripcion/estudiantes", response_model=EstudiantesParaInscripcionDTO, summary="RF-ASG-007: Obtener Estudiantes para Inscripción Masiva")
def obtener_estudiantes_para_inscripcion(
    id_curso_origen: int = Query(..., description="ID del curso origen"),
    gestion_destino: str = Query(..., description="Gestión destino (ej: 2025)"),
    db: Session = Depends(get_db)
):
    """
    Obtener estudiantes activos de un curso origen con indicador de inscripción.
    
    Para cada estudiante indica si ya está inscrito en algún curso de la gestión destino.
    Solo incluye estudiantes con estado "Activo".
    
    **Caso de uso:**
    Al inscribir estudiantes de "1ro A 2024" a "2do A 2025",
    muestra qué estudiantes ya fueron inscritos en algún curso de 2025.
    """
    return AsignacionService.obtener_estudiantes_para_inscripcion(
        db, id_curso_origen, gestion_destino
    )


@router.post("/inscripcion/masiva", response_model=InscripcionMasivaResponseDTO, summary="RF-ASG-008: Inscribir Múltiples Estudiantes")
def inscribir_multiples_estudiantes(
    datos: InscripcionMasivaDTO,
    db: Session = Depends(get_db)
):
    """
    Inscribir varios estudiantes simultáneamente a un curso destino.
    
    **Comportamiento:**
    - Si el estudiante ya está inscrito en el curso: se omite (no genera error)
    - Si el estudiante no está inscrito: se crea la asignación
    - Todos los estudiantes deben existir y estar activos
    
    **Retorna:**
    - Resumen con cantidad de inscritos exitosamente y ya inscritos
    
    **Caso de uso:**
    Inscribir 30 estudiantes de "1ro A 2024" al nuevo curso "2do A 2025" en una sola operación.
    """
    return AsignacionService.inscribir_multiples_estudiantes(db, datos)
