"""Repositorio para operaciones de base de datos de Estudiantes"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict
from datetime import datetime

from app.modules.administracion.models.persona_models import Estudiante
from app.modules.estudiantes.models.Curso import Curso
from app.modules.estudiantes.models.EstudianteCurso import EstudianteCurso


class EstudianteRepository:
    """Repositorio para gestión de estudiantes"""
    
    @staticmethod
    def crear_estudiante(db: Session, estudiante_data: dict) -> Estudiante:
        """Crear un nuevo estudiante"""
        estudiante = Estudiante(**estudiante_data)
        db.add(estudiante)
        db.commit()
        db.refresh(estudiante)
        return estudiante
    
    @staticmethod
    def obtener_por_id(db: Session, id_estudiante: int) -> Optional[Estudiante]:
        """Obtener estudiante por ID con sus cursos"""
        return db.query(Estudiante).options(
            joinedload(Estudiante.cursos)
        ).filter(Estudiante.id_estudiante == id_estudiante).first()
    
    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        """Obtener todos los estudiantes con paginación"""
        return db.query(Estudiante).options(
            joinedload(Estudiante.cursos)
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_total(db: Session) -> int:
        """Contar total de estudiantes"""
        return db.query(func.count(Estudiante.id_estudiante)).scalar()
    
    @staticmethod
    def actualizar_estudiante(db: Session, id_estudiante: int, datos: dict) -> Optional[Estudiante]:
        """Actualizar datos de un estudiante"""
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            return None
        
        for key, value in datos.items():
            if value is not None and hasattr(estudiante, key):
                setattr(estudiante, key, value)
        
        db.commit()
        db.refresh(estudiante)
        
        # Recargar con relaciones
        return EstudianteRepository.obtener_por_id(db, id_estudiante)
    
    @staticmethod
    def eliminar_estudiante(db: Session, id_estudiante: int) -> bool:
        """Eliminar un estudiante (cascada automática en asignaciones)"""
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            return False
        
        db.delete(estudiante)
        db.commit()
        return True
    
    # ============= Gestión de Estados =============
    
    @staticmethod
    def cambiar_estado(db: Session, id_estudiante: int, nuevo_estado: str) -> Optional[Dict]:
        """Cambiar el estado de un estudiante"""
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            return None
        
        estado_anterior = estudiante.estado
        estudiante.estado = nuevo_estado
        db.commit()
        db.refresh(estudiante)
        
        return {
            "estudiante": estudiante,
            "estado_anterior": estado_anterior,
            "estado_nuevo": nuevo_estado
        }
    
    @staticmethod
    def obtener_por_estado(db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        """Obtener estudiantes por estado"""
        return db.query(Estudiante).options(
            joinedload(Estudiante.cursos)
        ).filter(Estudiante.estado == estado).offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_por_estado(db: Session, estado: str) -> int:
        """Contar estudiantes por estado"""
        return db.query(func.count(Estudiante.id_estudiante)).filter(
            Estudiante.estado == estado
        ).scalar()
    
    # ============= Filtros por Gestión =============
    
    @staticmethod
    def obtener_por_gestion(
        db: Session,
        gestion: str,
        nivel: Optional[str] = None,
        id_curso: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Estudiante]:
        """Obtener estudiantes inscritos en una gestión específica"""
        query = db.query(Estudiante).join(
            EstudianteCurso,
            Estudiante.id_estudiante == EstudianteCurso.id_estudiante
        ).join(
            Curso,
            EstudianteCurso.id_curso == Curso.id_curso
        ).filter(Curso.gestion == gestion)
        
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        if id_curso:
            query = query.filter(Curso.id_curso == id_curso)
        
        # Obtener solo estudiantes únicos
        query = query.distinct()
        
        estudiantes = query.offset(skip).limit(limit).all()
        
        # Cargar manualmente los cursos de la gestión para cada estudiante
        for est in estudiantes:
            est.cursos = db.query(Curso).join(
                EstudianteCurso,
                Curso.id_curso == EstudianteCurso.id_curso
            ).filter(
                and_(
                    EstudianteCurso.id_estudiante == est.id_estudiante,
                    Curso.gestion == gestion
                )
            ).all()
        
        return estudiantes
    
    @staticmethod
    def contar_por_gestion(
        db: Session,
        gestion: str,
        nivel: Optional[str] = None,
        id_curso: Optional[int] = None
    ) -> int:
        """Contar estudiantes por gestión"""
        query = db.query(func.count(func.distinct(Estudiante.id_estudiante))).join(
            EstudianteCurso,
            Estudiante.id_estudiante == EstudianteCurso.id_estudiante
        ).join(
            Curso,
            EstudianteCurso.id_curso == Curso.id_curso
        ).filter(Curso.gestion == gestion)
        
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        if id_curso:
            query = query.filter(Curso.id_curso == id_curso)
        
        return query.scalar() or 0
    
    # ============= Importación =============
    
    @staticmethod
    def obtener_por_ci(db: Session, ci: str) -> Optional[Estudiante]:
        """Obtener estudiante por cédula de identidad"""
        return db.query(Estudiante).filter(Estudiante.ci == ci).first()
    
    @staticmethod
    def crear_o_actualizar_por_ci(db: Session, datos: dict) -> tuple[Estudiante, bool]:
        """
        Crear o actualizar estudiante según CI
        Retorna (estudiante, fue_creado: bool)
        """
        ci = datos.get('ci')
        if not ci:
            # Si no hay CI, crear siempre
            estudiante = Estudiante(**datos)
            db.add(estudiante)
            db.commit()
            db.refresh(estudiante)
            return estudiante, True
        
        # Buscar por CI
        estudiante = EstudianteRepository.obtener_por_ci(db, ci)
        
        if estudiante:
            # Actualizar existente
            for key, value in datos.items():
                if hasattr(estudiante, key) and value is not None:
                    setattr(estudiante, key, value)
            db.commit()
            db.refresh(estudiante)
            return estudiante, False
        else:
            # Crear nuevo
            estudiante = Estudiante(**datos)
            db.add(estudiante)
            db.commit()
            db.refresh(estudiante)
            return estudiante, True
    
    @staticmethod
    def obtener_todos_sin_paginacion(db: Session) -> List[Estudiante]:
        """Obtener todos los estudiantes sin paginación (para exportar)"""
        return db.query(Estudiante).all()
