"""Controlador (router) para el módulo de Cursos."""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import text


from app.core.database import get_db
from app.modules.administracion.services.curso_service import CursoService
from app.modules.administracion.dto.curso_dto import (
    CursoDTO,
    EstudianteListResponseDTO,
    ProfesorListResponseDTO
)
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.permission_mapper import puede_ver_todas_esquelas


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[CursoDTO])
def listar_cursos(
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Lista cursos disponibles según el rol del usuario.

    **Permisos:**
    - **Admin/Regente**: Ve todos los cursos
    - **Profesor**: Ve solo los cursos donde imparte clases
    """
    # Si es admin/regente, retornar todos los cursos
    if puede_ver_todas_esquelas(current_user):
        return CursoService.listar_cursos(db)

    # Si es profesor, retornar solo sus cursos
    rows = db.execute(
        text(
            """
            SELECT DISTINCT c.id_curso, c.nombre_curso, c.nivel, c.gestion
            FROM profesores p
            JOIN profesores_cursos_materias pcm ON pcm.id_profesor = p.id_profesor
            JOIN cursos c ON c.id_curso = pcm.id_curso
            WHERE p.id_persona = :id_persona
            ORDER BY c.nombre_curso
            """
        ),
        {"id_persona": current_user.id_persona},
    ).mappings().all()
    return [dict(r) for r in rows]

@router.get("/mis_cursos/{id_persona}", response_model=List[CursoDTO])
def listar_mis_cursos(
    id_persona: int,
        current_user: Usuario = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
    ):
        """
        Lista los cursos donde el profesor autenticado imparte clases.

        **Uso:** Para que un profesor vea sus propios cursos asignados.
        Solo muestra los cursos donde el profesor tiene asignadas materias.
        """
        rows = db.execute(
            text(
                """
                SELECT DISTINCT c.id_curso, c.nombre_curso, c.nivel, c.gestion
                FROM profesores p
                JOIN profesores_cursos_materias pcm ON pcm.id_profesor = p.id_profesor
                JOIN cursos c ON c.id_curso = pcm.id_curso
                WHERE p.id_persona = :id_persona
                ORDER BY c.nombre_curso
                """
            ),
            {"id_persona": current_user.id_persona},
        ).mappings().all()
        return [dict(r) for r in rows]



@router.get("/{curso_id}", response_model=CursoDTO)
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un curso específico por ID.
    """
    return CursoService.obtener_curso(db, curso_id)


@router.get("/{curso_id}/students", response_model=EstudianteListResponseDTO)
def listar_estudiantes_por_curso(
    curso_id: int,
    name: Optional[str] = Query(
        None, description="Filtrar por nombre del estudiante"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(
        10, ge=1, le=10000, description="Tamaño de página (máximo 10000)"),
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Lista estudiantes de un curso específico.

    **Permisos:**
    - **Admin/Regente**: Puede ver estudiantes de cualquier curso
    - **Profesor**: Solo puede ver estudiantes de los cursos donde imparte clases

    Parámetros:
    - **name**: Filtro por nombre, apellido paterno o materno del estudiante
    - **page**: Número de página (por defecto 1)
    - **page_size**: Cantidad de resultados por página (por defecto 10, máximo 10000)
    """
    # Validar que el profesor tenga acceso a este curso
    if not puede_ver_todas_esquelas(current_user):
        # Es profesor, verificar que imparte clases en este curso
        from app.modules.administracion.repositories.persona_repository import PersonaRepository

        row = db.execute(
            text("SELECT id_profesor FROM profesores WHERE id_persona = :id_persona"),
            {"id_persona": current_user.id_persona},
        ).first()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver estudiantes de este curso."
            )

        id_profesor = int(row[0])

        if not PersonaRepository.es_profesor_del_curso(db, id_profesor, curso_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permisos para ver estudiantes de este curso. Solo puede ver estudiantes de los cursos donde imparte clases."
            )

    return CursoService.listar_estudiantes_por_curso(db, curso_id, name, page, page_size)


@router.get("/{curso_id}/teachers", response_model=ProfesorListResponseDTO)
def listar_profesores_por_curso(
    curso_id: int,
    name: Optional[str] = Query(
        None, description="Filtrar por nombre del profesor"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Session = Depends(get_db)
):
    """
    Lista profesores de un curso específico.

    Parámetros:
    - **name**: Filtro por nombre, apellido paterno o materno del profesor
    - **page**: Número de página (por defecto 1)
    - **page_size**: Cantidad de resultados por página (por defecto 10, máximo 100)
    """
    return CursoService.listar_profesores_por_curso(db, curso_id, name, page, page_size)


@router.get("/teacher/{id_persona}/courses", response_model=List[CursoDTO])
def listar_cursos_por_profesor(
    id_persona: int,
    db: Session = Depends(get_db)
):
    """
    Lista los cursos donde un profesor específico imparte clases.

    **Uso:** Para filtrar cursos disponibles cuando un profesor crea una esquela.
    Solo muestra los cursos donde el profesor tiene asignadas materias.

    Parámetros:
    - **id_persona**: ID del profesor (id_persona en la tabla personas)
    """
    return CursoService.listar_cursos_por_profesor(db, id_persona)


@router.post("/", response_model=CursoDTO, status_code=status.HTTP_201_CREATED)
def crear_curso(
    curso: dict,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo curso
    """
    return CursoService.crear_curso(db, curso)


@router.put("/{curso_id}", response_model=CursoDTO)
def actualizar_curso(
    curso_id: int,
    curso: dict,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Actualiza un curso existente
    """
    return CursoService.actualizar_curso(db, curso_id, curso)


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_curso(
    curso_id: int,
    current_user: Usuario = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Elimina un curso
    """
    CursoService.eliminar_curso(db, curso_id)
    return None
