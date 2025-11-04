# app/modules/administracion/services/curso_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.administracion.repositories.curso_repository import CursoRepository
from typing import Optional


class CursoService:

    @staticmethod
    def listar_cursos(db: Session):
        """Lista todos los cursos disponibles"""
        return CursoRepository.get_all(db)

    @staticmethod
    def obtener_curso(db: Session, curso_id: int):
        """Obtiene un curso por ID"""
        curso = CursoRepository.get_by_id(db, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return curso

    @staticmethod
    def listar_estudiantes_por_curso(
        db: Session,
        curso_id: int,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ):
        """
        Lista estudiantes de un curso con filtro opcional por nombre
        """
        curso = CursoRepository.get_by_id(db, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        
        return CursoRepository.get_estudiantes_by_curso(
            db, curso_id, name, page, page_size
        )

    @staticmethod
    def listar_profesores_por_curso(
        db: Session,
        curso_id: int,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ):
        """
        Lista profesores de un curso con filtro opcional por nombre
        """
        curso = CursoRepository.get_by_id(db, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        
        return CursoRepository.get_profesores_by_curso(
            db, curso_id, name, page, page_size
        )
