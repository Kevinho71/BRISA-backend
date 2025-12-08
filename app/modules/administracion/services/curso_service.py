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
    def listar_cursos_por_profesor(db: Session, id_persona: int):
        """Lista los cursos donde un profesor imparte clases"""
        return CursoRepository.get_by_profesor(db, id_persona)
    
    
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
    
    @staticmethod
    def listar_cursos_por_profesor(db: Session, id_persona: int):
        """
        Lista los cursos donde un profesor imparte clases.
        Usado para filtrar cursos disponibles al crear esquelas.
        """
        from app.modules.administracion.repositories.persona_repository import PersonaRepository
        
        # Verificar que la persona existe y es profesor
        persona = PersonaRepository.get_by_id(db, id_persona)
        if not persona:
            raise HTTPException(status_code=404, detail="Profesor no encontrado")
        
        if persona.tipo_persona != 'profesor':
            raise HTTPException(
                status_code=400,
                detail="La persona especificada no es un profesor"
            )
        
        return PersonaRepository.get_cursos_by_profesor(db, id_persona)
