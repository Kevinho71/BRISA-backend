"""Servicio para lógica de negocio de Asignaciones Estudiante-Curso"""

from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.modules.estudiantes_cursos.repositories.asignacion_repository import AsignacionRepository
from app.modules.estudiantes_cursos.dto.asignacion_dto import (
    AsignarEstudianteDTO,
    AsignacionResponseDTO,
    EstudiantesDeCursoDTO,
    CursosDeEstudianteDTO,
    EstudianteBasicoAsignacionDTO,
    CursoBasicoAsignacionDTO,
    GestionesDisponiblesDTO,
    CursosPorGestionDTO,
    CursoParaInscripcionDTO,
    EstudiantesParaInscripcionDTO,
    EstudianteParaInscripcionDTO,
    InscripcionMasivaDTO,
    InscripcionMasivaResponseDTO
)


class AsignacionService:
    """Servicio para gestión de asignaciones estudiante-curso"""
    
    # ============= Asignaciones Individuales =============
    
    @staticmethod
    def asignar_estudiante_a_curso(
        db: Session,
        datos: AsignarEstudianteDTO
    ) -> AsignacionResponseDTO:
        """RF-ASG-001: Asignar Estudiante a Curso"""
        # Validar que el estudiante exista
        if not AsignacionRepository.verificar_estudiante_existe(db, datos.id_estudiante):
            raise HTTPException(
                status_code=404,
                detail=f"Estudiante con ID {datos.id_estudiante} no encontrado"
            )
        
        # Validar que el curso exista
        if not AsignacionRepository.verificar_curso_existe(db, datos.id_curso):
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {datos.id_curso} no encontrado"
            )
        
        # Asignar
        fue_creado = AsignacionRepository.asignar_estudiante_a_curso(
            db, datos.id_estudiante, datos.id_curso
        )
        
        if not fue_creado:
            raise HTTPException(
                status_code=400,
                detail="El estudiante ya está asignado a este curso"
            )
        
        # Obtener nombres para respuesta
        estudiante, _ = AsignacionRepository.obtener_cursos_de_estudiante(db, datos.id_estudiante)
        curso, _ = AsignacionRepository.obtener_estudiantes_de_curso(db, datos.id_curso)
        
        return AsignacionResponseDTO(
            mensaje="Estudiante asignado exitosamente al curso",
            id_estudiante=datos.id_estudiante,
            id_curso=datos.id_curso,
            nombre_estudiante=f"{estudiante.nombres} {estudiante.apellido_paterno}",
            nombre_curso=curso.nombre_curso
        )
    
    @staticmethod
    def desasignar_estudiante_de_curso(
        db: Session,
        datos: AsignarEstudianteDTO
    ) -> AsignacionResponseDTO:
        """RF-ASG-002: Desasignar Estudiante de Curso"""
        # Validar que el estudiante exista
        if not AsignacionRepository.verificar_estudiante_existe(db, datos.id_estudiante):
            raise HTTPException(
                status_code=404,
                detail=f"Estudiante con ID {datos.id_estudiante} no encontrado"
            )
        
        # Validar que el curso exista
        if not AsignacionRepository.verificar_curso_existe(db, datos.id_curso):
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {datos.id_curso} no encontrado"
            )
        
        # Obtener nombres antes de desasignar
        estudiante, _ = AsignacionRepository.obtener_cursos_de_estudiante(db, datos.id_estudiante)
        curso, _ = AsignacionRepository.obtener_estudiantes_de_curso(db, datos.id_curso)
        
        # Desasignar
        fue_eliminado = AsignacionRepository.desasignar_estudiante_de_curso(
            db, datos.id_estudiante, datos.id_curso
        )
        
        if not fue_eliminado:
            raise HTTPException(
                status_code=400,
                detail="El estudiante no está asignado a este curso"
            )
        
        return AsignacionResponseDTO(
            mensaje="Estudiante desasignado exitosamente del curso",
            id_estudiante=datos.id_estudiante,
            id_curso=datos.id_curso,
            nombre_estudiante=f"{estudiante.nombres} {estudiante.apellido_paterno}",
            nombre_curso=curso.nombre_curso
        )
    
    @staticmethod
    def obtener_estudiantes_de_curso(db: Session, id_curso: int) -> EstudiantesDeCursoDTO:
        """RF-ASG-003: Obtener Estudiantes de un Curso"""
        curso, estudiantes = AsignacionRepository.obtener_estudiantes_de_curso(db, id_curso)
        
        if not curso:
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        estudiantes_dto = [
            EstudianteBasicoAsignacionDTO(
                id_estudiante=est.id_estudiante,
                ci=est.ci,
                nombres=est.nombres,
                apellido_paterno=est.apellido_paterno,
                apellido_materno=est.apellido_materno,
                estado=est.estado
            )
            for est in estudiantes
        ]
        
        return EstudiantesDeCursoDTO(
            id_curso=curso.id_curso,
            nombre_curso=curso.nombre_curso,
            nivel=curso.nivel,
            gestion=curso.gestion,
            total_estudiantes=len(estudiantes),
            estudiantes=estudiantes_dto
        )
    
    @staticmethod
    def obtener_cursos_de_estudiante(db: Session, id_estudiante: int) -> CursosDeEstudianteDTO:
        """RF-ASG-004: Obtener Cursos de un Estudiante"""
        estudiante, cursos = AsignacionRepository.obtener_cursos_de_estudiante(db, id_estudiante)
        
        if not estudiante:
            raise HTTPException(
                status_code=404,
                detail=f"Estudiante con ID {id_estudiante} no encontrado"
            )
        
        cursos_dto = [
            CursoBasicoAsignacionDTO(
                id_curso=curso.id_curso,
                nombre_curso=curso.nombre_curso,
                nivel=curso.nivel,
                gestion=curso.gestion
            )
            for curso in cursos
        ]
        
        return CursosDeEstudianteDTO(
            id_estudiante=estudiante.id_estudiante,
            nombres=estudiante.nombres,
            apellido_paterno=estudiante.apellido_paterno,
            apellido_materno=estudiante.apellido_materno,
            estado=estudiante.estado,
            total_cursos=len(cursos),
            cursos=cursos_dto
        )
    
    # ============= Inscripción Masiva =============
    
    @staticmethod
    def obtener_gestiones_disponibles(db: Session) -> GestionesDisponiblesDTO:
        """RF-ASG-005: Obtener Gestiones Disponibles"""
        gestiones = AsignacionRepository.obtener_gestiones_disponibles(db)
        
        if not gestiones:
            raise HTTPException(
                status_code=404,
                detail="No hay gestiones con cursos registrados"
            )
        
        return GestionesDisponiblesDTO(
            total=len(gestiones),
            gestiones=gestiones
        )
    
    @staticmethod
    def obtener_cursos_por_gestion(db: Session, gestion: str) -> CursosPorGestionDTO:
        """RF-ASG-006: Obtener Cursos por Gestión para Inscripción"""
        cursos = AsignacionRepository.obtener_cursos_por_gestion(db, gestion)
        
        if not cursos:
            raise HTTPException(
                status_code=404,
                detail=f"No hay cursos registrados en la gestión {gestion}"
            )
        
        cursos_dto = [
            CursoParaInscripcionDTO(
                id_curso=curso.id_curso,
                nombre_curso=curso.nombre_curso,
                nivel=curso.nivel.capitalize() if curso.nivel else curso.nivel  # Capitalizar para API
            )
            for curso in cursos
        ]
        
        return CursosPorGestionDTO(
            gestion=gestion,
            total=len(cursos),
            cursos=cursos_dto
        )
    
    @staticmethod
    def obtener_estudiantes_para_inscripcion(
        db: Session,
        id_curso_origen: int,
        gestion_destino: str
    ) -> EstudiantesParaInscripcionDTO:
        """RF-ASG-007: Obtener Estudiantes para Inscripción Masiva"""
        curso_origen, estudiantes_data = AsignacionRepository.obtener_estudiantes_para_inscripcion(
            db, id_curso_origen, gestion_destino
        )
        
        if not curso_origen:
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {id_curso_origen} no encontrado"
            )
        
        estudiantes_dto = [
            EstudianteParaInscripcionDTO(
                id_estudiante=data["estudiante"].id_estudiante,
                ci=data["estudiante"].ci,
                nombres=data["estudiante"].nombres,
                apellido_paterno=data["estudiante"].apellido_paterno,
                apellido_materno=data["estudiante"].apellido_materno,
                ya_inscrito=data["ya_inscrito"]
            )
            for data in estudiantes_data
        ]
        
        return EstudiantesParaInscripcionDTO(
            id_curso_origen=curso_origen.id_curso,
            nombre_curso_origen=curso_origen.nombre_curso,
            gestion_origen=curso_origen.gestion,
            gestion_destino=gestion_destino,
            total_estudiantes=len(estudiantes_dto),
            estudiantes=estudiantes_dto
        )
    
    @staticmethod
    def inscribir_multiples_estudiantes(
        db: Session,
        datos: InscripcionMasivaDTO
    ) -> InscripcionMasivaResponseDTO:
        """RF-ASG-008: Inscribir Múltiples Estudiantes a un Curso"""
        # Validar que el curso destino exista
        if not AsignacionRepository.verificar_curso_existe(db, datos.id_curso_destino):
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {datos.id_curso_destino} no encontrado"
            )
        
        # Validar que todos los estudiantes existan
        for id_est in datos.ids_estudiantes:
            if not AsignacionRepository.verificar_estudiante_existe(db, id_est):
                raise HTTPException(
                    status_code=404,
                    detail=f"Estudiante con ID {id_est} no encontrado"
                )
        
        # Validar que todos los estudiantes estén activos
        for id_est in datos.ids_estudiantes:
            if not AsignacionRepository.verificar_estudiante_activo(db, id_est):
                raise HTTPException(
                    status_code=400,
                    detail=f"Estudiante con ID {id_est} no está activo"
                )
        
        # Inscribir estudiantes
        inscritos, ya_inscritos = AsignacionRepository.inscribir_multiples_estudiantes(
            db, datos.id_curso_destino, datos.ids_estudiantes
        )
        
        # Obtener nombre del curso
        curso, _ = AsignacionRepository.obtener_estudiantes_de_curso(db, datos.id_curso_destino)
        
        return InscripcionMasivaResponseDTO(
            mensaje=f"Inscripción masiva completada: {inscritos} nuevos, {ya_inscritos} ya inscritos",
            id_curso_destino=datos.id_curso_destino,
            nombre_curso_destino=f"{curso.nombre_curso} - {curso.gestion}",
            total_procesados=len(datos.ids_estudiantes),
            inscritos_exitosamente=inscritos,
            ya_inscritos=ya_inscritos
        )
