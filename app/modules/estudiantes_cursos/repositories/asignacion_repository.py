"""Repositorio para operaciones de Asignaciones Estudiante-Curso"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, exists
from typing import List, Optional, Tuple

from app.modules.administracion.models.persona_models import Estudiante
from app.modules.estudiantes.models.Curso import Curso
from app.modules.estudiantes.models.EstudianteCurso import EstudianteCurso


class AsignacionRepository:
    """Repositorio para gestión de asignaciones estudiante-curso"""
    
    # ============= Asignaciones Individuales =============
    
    @staticmethod
    def asignar_estudiante_a_curso(
        db: Session,
        id_estudiante: int,
        id_curso: int
    ) -> bool:
        """
        Asignar estudiante a curso.
        Retorna True si se creó la asignación, False si ya existía.
        """
        # Verificar si ya existe la asignación
        existe = db.query(EstudianteCurso).filter(
            and_(
                EstudianteCurso.id_estudiante == id_estudiante,
                EstudianteCurso.id_curso == id_curso
            )
        ).first()
        
        if existe:
            return False
        
        # Crear asignación
        asignacion = EstudianteCurso(
            id_estudiante=id_estudiante,
            id_curso=id_curso
        )
        db.add(asignacion)
        db.commit()
        return True
    
    @staticmethod
    def desasignar_estudiante_de_curso(
        db: Session,
        id_estudiante: int,
        id_curso: int
    ) -> bool:
        """
        Desasignar estudiante de curso.
        Retorna True si se eliminó, False si no existía.
        """
        asignacion = db.query(EstudianteCurso).filter(
            and_(
                EstudianteCurso.id_estudiante == id_estudiante,
                EstudianteCurso.id_curso == id_curso
            )
        ).first()
        
        if not asignacion:
            return False
        
        db.delete(asignacion)
        db.commit()
        return True
    
    @staticmethod
    def obtener_estudiantes_de_curso(db: Session, id_curso: int) -> Tuple[Curso, List[Estudiante]]:
        """Obtener curso con sus estudiantes"""
        curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
        
        if not curso:
            return None, []
        
        estudiantes = db.query(Estudiante).join(
            EstudianteCurso,
            Estudiante.id_estudiante == EstudianteCurso.id_estudiante
        ).filter(
            EstudianteCurso.id_curso == id_curso
        ).order_by(
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno,
            Estudiante.nombres
        ).all()
        
        return curso, estudiantes
    
    @staticmethod
    def obtener_cursos_de_estudiante(db: Session, id_estudiante: int) -> Tuple[Estudiante, List[Curso]]:
        """Obtener estudiante con sus cursos"""
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        
        if not estudiante:
            return None, []
        
        cursos = db.query(Curso).join(
            EstudianteCurso,
            Curso.id_curso == EstudianteCurso.id_curso
        ).filter(
            EstudianteCurso.id_estudiante == id_estudiante
        ).order_by(
            Curso.gestion.desc(),
            Curso.nivel,
            Curso.nombre_curso
        ).all()
        
        return estudiante, cursos
    
    # ============= Inscripción Masiva =============
    
    @staticmethod
    def obtener_gestiones_disponibles(db: Session) -> List[str]:
        """Obtener lista de gestiones con cursos"""
        gestiones = db.query(Curso.gestion).distinct().order_by(Curso.gestion.desc()).all()
        return [g[0] for g in gestiones]
    
    @staticmethod
    def obtener_cursos_por_gestion(db: Session, gestion: str) -> List[Curso]:
        """Obtener cursos de una gestión para inscripción"""
        return db.query(Curso).filter(
            Curso.gestion == gestion
        ).order_by(
            Curso.nivel,
            Curso.nombre_curso
        ).all()
    
    @staticmethod
    def obtener_estudiantes_para_inscripcion(
        db: Session,
        id_curso_origen: int,
        gestion_destino: str
    ) -> Tuple[Curso, List[dict]]:
        """
        Obtener estudiantes activos de un curso origen con indicador de si ya están
        inscritos en algún curso de la gestión destino.
        """
        curso_origen = db.query(Curso).filter(Curso.id_curso == id_curso_origen).first()
        
        if not curso_origen:
            return None, []
        
        # Obtener estudiantes activos del curso origen
        estudiantes = db.query(Estudiante).join(
            EstudianteCurso,
            Estudiante.id_estudiante == EstudianteCurso.id_estudiante
        ).filter(
            and_(
                EstudianteCurso.id_curso == id_curso_origen,
                Estudiante.estado == "Activo"
            )
        ).order_by(
            Estudiante.apellido_paterno,
            Estudiante.apellido_materno,
            Estudiante.nombres
        ).all()
        
        # Para cada estudiante, verificar si ya está inscrito en la gestión destino
        resultado = []
        for est in estudiantes:
            # Verificar si el estudiante ya tiene asignación en algún curso de la gestión destino
            ya_inscrito = db.query(
                exists().where(
                    and_(
                        EstudianteCurso.id_estudiante == est.id_estudiante,
                        EstudianteCurso.id_curso == Curso.id_curso,
                        Curso.gestion == gestion_destino
                    )
                )
            ).scalar()
            
            resultado.append({
                "estudiante": est,
                "ya_inscrito": ya_inscrito
            })
        
        return curso_origen, resultado
    
    @staticmethod
    def inscribir_multiples_estudiantes(
        db: Session,
        id_curso_destino: int,
        ids_estudiantes: List[int]
    ) -> Tuple[int, int]:
        """
        Inscribir múltiples estudiantes a un curso.
        Retorna (inscritos_nuevos, ya_inscritos)
        """
        inscritos_nuevos = 0
        ya_inscritos = 0
        
        for id_estudiante in ids_estudiantes:
            # Verificar si ya existe la asignación
            existe = db.query(EstudianteCurso).filter(
                and_(
                    EstudianteCurso.id_estudiante == id_estudiante,
                    EstudianteCurso.id_curso == id_curso_destino
                )
            ).first()
            
            if existe:
                ya_inscritos += 1
            else:
                # Crear asignación
                asignacion = EstudianteCurso(
                    id_estudiante=id_estudiante,
                    id_curso=id_curso_destino
                )
                db.add(asignacion)
                inscritos_nuevos += 1
        
        db.commit()
        return inscritos_nuevos, ya_inscritos
    
    @staticmethod
    def verificar_estudiante_existe(db: Session, id_estudiante: int) -> bool:
        """Verificar si un estudiante existe"""
        return db.query(
            exists().where(Estudiante.id_estudiante == id_estudiante)
        ).scalar()
    
    @staticmethod
    def verificar_curso_existe(db: Session, id_curso: int) -> bool:
        """Verificar si un curso existe"""
        return db.query(
            exists().where(Curso.id_curso == id_curso)
        ).scalar()
    
    @staticmethod
    def verificar_estudiante_activo(db: Session, id_estudiante: int) -> bool:
        """Verificar si un estudiante está activo"""
        estudiante = db.query(Estudiante).filter(
            Estudiante.id_estudiante == id_estudiante
        ).first()
        return estudiante and estudiante.estado == "Activo"
