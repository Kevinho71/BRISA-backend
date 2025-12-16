"""Repositorio para operaciones de base de datos de Cursos"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, text
from typing import List, Optional

from app.modules.estudiantes.models.Curso import Curso
from app.modules.administracion.models.persona_models import Estudiante


class CursoRepository:
    """Repositorio para gestión de cursos"""
    
    @staticmethod
    def crear_curso(db: Session, curso_data: dict) -> Curso:
        """Crear un nuevo curso"""
        curso = Curso(**curso_data)
        db.add(curso)
        db.commit()
        db.refresh(curso)
        return curso
    
    @staticmethod
    def obtener_por_id(db: Session, id_curso: int) -> Optional[Curso]:
        """Obtener curso por ID con sus estudiantes"""
        return db.query(Curso).options(
            joinedload(Curso.estudiantes)
        ).filter(Curso.id_curso == id_curso).first()
    
    @staticmethod
    def obtener_todos(
        db: Session,
        gestion: Optional[str] = None,
        nivel: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Curso]:
        """Obtener todos los cursos con filtros opcionales"""
        query = db.query(Curso).options(joinedload(Curso.estudiantes))
        
        if gestion:
            query = query.filter(Curso.gestion == gestion)
        
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_total(
        db: Session,
        gestion: Optional[str] = None,
        nivel: Optional[str] = None
    ) -> int:
        """Contar total de cursos con filtros"""
        query = db.query(func.count(Curso.id_curso))
        
        if gestion:
            query = query.filter(Curso.gestion == gestion)
        
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        return query.scalar()
    
    @staticmethod
    def actualizar_curso(db: Session, id_curso: int, datos: dict) -> Optional[Curso]:
        """Actualizar datos de un curso"""
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            return None
        
        for key, value in datos.items():
            if value is not None and hasattr(curso, key):
                setattr(curso, key, value)
        
        db.commit()
        db.refresh(curso)
        
        # Recargar con relaciones
        return CursoRepository.obtener_por_id(db, id_curso)
    
    @staticmethod
    def eliminar_curso(db: Session, id_curso: int) -> bool:
        """Eliminar un curso (cascada automática en asignaciones)"""
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            return False
        
        db.delete(curso)
        db.commit()
        return True
    
    # ============= Filtros por Gestión =============
    
    @staticmethod
    def obtener_por_gestion_nivel(
        db: Session,
        gestion: str,
        nivel: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Curso]:
        """Obtener cursos por gestión y opcionalmente por nivel"""
        query = db.query(Curso).options(
            joinedload(Curso.estudiantes)
        ).filter(Curso.gestion == gestion)
        
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        # Ordenar por nivel y nombre
        query = query.order_by(Curso.nivel, Curso.nombre_curso)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_por_gestion_nivel(
        db: Session,
        gestion: str,
        nivel: Optional[str] = None
    ) -> int:
        """Contar cursos por gestión y nivel"""
        query = db.query(func.count(Curso.id_curso)).filter(Curso.gestion == gestion)
        
        if nivel:
            query = query.filter(Curso.nivel == nivel)
        
        return query.scalar()
    
    # ============= Gestión de Gestiones =============
    
    @staticmethod
    def obtener_gestiones_disponibles(db: Session) -> List[str]:
        """Obtener lista de todas las gestiones con cursos"""
        gestiones = db.query(Curso.gestion).distinct().order_by(Curso.gestion.desc()).all()
        return [g[0] for g in gestiones]
    
    @staticmethod
    def existe_gestion(db: Session, gestion: str) -> bool:
        """Verificar si existe al menos un curso en una gestión"""
        count = db.query(func.count(Curso.id_curso)).filter(
            Curso.gestion == gestion
        ).scalar()
        return count > 0
    
    @staticmethod
    def eliminar_cursos_por_gestion(db: Session, gestion: str) -> int:
        """Eliminar todos los cursos de una gestión específica"""
        deleted = db.query(Curso).filter(Curso.gestion == gestion).delete()
        db.commit()
        return deleted
    
    @staticmethod
    def copiar_cursos_entre_gestiones(
        db: Session,
        gestion_origen: str,
        gestion_destino: str
    ) -> int:
        """
        Copiar estructura de cursos de una gestión a otra.
        Solo copia nombre_curso, nivel y nueva gestión (NO estudiantes).
        Retorna cantidad de cursos copiados.
        """
        # Usar SQL directo para mejor rendimiento
        sql = text("""
            INSERT INTO cursos (nombre_curso, nivel, gestion)
            SELECT nombre_curso, nivel, :gestion_destino
            FROM cursos
            WHERE gestion = :gestion_origen
        """)
        
        result = db.execute(
            sql,
            {"gestion_origen": gestion_origen, "gestion_destino": gestion_destino}
        )
        db.commit()
        
        return result.rowcount
