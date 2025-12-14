# app/modules/profesores/services/profesor_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.profesores.repositories.profesor_repository import ProfesorRepository
from app.modules.profesores.models.profesor_models import Profesor
from app.shared.models import ProfesorCursoMateria
from app.shared.models.persona import Persona, TipoPersonaEnum
from app.modules.profesores.dto.profesor_dto import (
    ProfesorCreateDTO, 
    ProfesorUpdateDTO, 
    ProfesorResponseDTO,
    AsignarCursoMateriaDTO,
    ProfesorCursoMateriaResponseDTO
)
from app.shared.exceptions.custom_exceptions import NotFoundException, BadRequestException
from datetime import datetime


class ProfesorService:
    """Servicio para la lógica de negocio de profesores"""

    @staticmethod
    def get_all_profesores(db: Session, skip: int = 0, limit: int = 100) -> List[ProfesorResponseDTO]:
        """Obtiene todos los profesores"""
        profesores = ProfesorRepository.get_all(db, skip, limit)
        response_list = []
        
        for profesor in profesores:
            persona = ProfesorRepository.get_persona_by_id(db, profesor.id_persona)
            if persona:
                response_list.append(ProfesorService._build_response_dto(profesor, persona))
        
        return response_list

    @staticmethod
    def get_profesor_by_id(db: Session, id_profesor: int) -> ProfesorResponseDTO:
        """Obtiene un profesor por ID"""
        profesor = ProfesorRepository.get_by_id(db, id_profesor)
        if not profesor:
            raise NotFoundException(f"Profesor con ID {id_profesor} no encontrado")
        
        persona = ProfesorRepository.get_persona_by_id(db, profesor.id_persona)
        if not persona:
            raise NotFoundException(f"Persona asociada al profesor no encontrada")
        
        return ProfesorService._build_response_dto(profesor, persona)

    @staticmethod
    def create_profesor(db: Session, data: ProfesorCreateDTO) -> ProfesorResponseDTO:
        """Crea un nuevo profesor"""
        # Verificar si ya existe una persona con ese CI
        persona_existente = ProfesorRepository.get_persona_by_ci(db, data.ci)
        if persona_existente:
            raise BadRequestException(f"Ya existe una persona con CI {data.ci}")
        
        try:
            # Crear la persona
            nueva_persona = Persona(
                ci=data.ci,
                nombres=data.nombres,
                apellido_paterno=data.apellido_paterno,
                apellido_materno=data.apellido_materno,
                direccion=data.direccion,
                telefono=data.telefono,
                correo=data.correo,
                tipo_persona=TipoPersonaEnum.profesor,
                id_cargo=data.id_cargo,
                estado_laboral=data.estado_laboral,
                anos_experiencia=data.anos_experiencia,
                fecha_ingreso=data.fecha_ingreso,
                is_active=True
            )
            
            persona_creada = ProfesorRepository.create_persona(db, nueva_persona)
            
            # Crear el profesor
            nuevo_profesor = Profesor(
                id_persona=persona_creada.id_persona,
                especialidad=data.especialidad,
                titulo_academico=data.titulo_academico,
                nivel_enseñanza=data.nivel_enseñanza.value if data.nivel_enseñanza else "todos",
                observaciones=data.observaciones
            )
            
            profesor_creado = ProfesorRepository.create_profesor(db, nuevo_profesor)
            
            db.commit()
            db.refresh(profesor_creado)
            
            return ProfesorService._build_response_dto(profesor_creado, persona_creada)
            
        except Exception as e:
            db.rollback()
            raise BadRequestException(f"Error al crear profesor: {str(e)}")

    @staticmethod
    def update_profesor(db: Session, id_profesor: int, data: ProfesorUpdateDTO) -> ProfesorResponseDTO:
        """Actualiza un profesor existente"""
        profesor = ProfesorRepository.get_by_id(db, id_profesor)
        if not profesor:
            raise NotFoundException(f"Profesor con ID {id_profesor} no encontrado")
        
        persona = ProfesorRepository.get_persona_by_id(db, profesor.id_persona)
        if not persona:
            raise NotFoundException(f"Persona asociada al profesor no encontrada")
        
        try:
            # Actualizar datos de persona
            if data.ci is not None:
                # Verificar que el CI no esté en uso por otra persona
                persona_con_ci = ProfesorRepository.get_persona_by_ci(db, data.ci)
                if persona_con_ci and persona_con_ci.id_persona != persona.id_persona:
                    raise BadRequestException(f"El CI {data.ci} ya está en uso")
                persona.ci = data.ci
            
            if data.nombres is not None:
                persona.nombres = data.nombres
            if data.apellido_paterno is not None:
                persona.apellido_paterno = data.apellido_paterno
            if data.apellido_materno is not None:
                persona.apellido_materno = data.apellido_materno
            if data.direccion is not None:
                persona.direccion = data.direccion
            if data.telefono is not None:
                persona.telefono = data.telefono
            if data.correo is not None:
                persona.correo = data.correo

            # Use dict with exclude_unset=True to know what was sent, allowing None for id_cargo
            update_data = data.dict(exclude_unset=True)
            if "id_cargo" in update_data:
                persona.id_cargo = data.id_cargo

            if data.estado_laboral is not None:
                persona.estado_laboral = data.estado_laboral
            if data.anos_experiencia is not None:
                persona.anos_experiencia = data.anos_experiencia
            if data.fecha_ingreso is not None:
                persona.fecha_ingreso = data.fecha_ingreso
            if data.fecha_retiro is not None:
                persona.fecha_retiro = data.fecha_retiro
            if data.motivo_retiro is not None:
                persona.motivo_retiro = data.motivo_retiro
            if data.is_active is not None:
                persona.is_active = data.is_active
            
            ProfesorRepository.update_persona(db, persona)
            
            # Actualizar datos específicos del profesor
            if data.especialidad is not None:
                profesor.especialidad = data.especialidad
            if data.titulo_academico is not None:
                profesor.titulo_academico = data.titulo_academico
            if data.nivel_enseñanza is not None:
                profesor.nivel_enseñanza = data.nivel_enseñanza.value
            if data.observaciones is not None:
                profesor.observaciones = data.observaciones
            
            ProfesorRepository.update_profesor(db, profesor)
            
            db.commit()
            db.refresh(profesor)
            db.refresh(persona)
            
            return ProfesorService._build_response_dto(profesor, persona)
            
        except Exception as e:
            db.rollback()
            raise BadRequestException(f"Error al actualizar profesor: {str(e)}")

    @staticmethod
    def delete_profesor(db: Session, id_profesor: int):
        """Elimina un profesor"""
        profesor = ProfesorRepository.get_by_id(db, id_profesor)
        if not profesor:
            raise NotFoundException(f"Profesor con ID {id_profesor} no encontrado")
        
        try:
            # El repository ya maneja la eliminación de asignaciones
            ProfesorRepository.delete(db, profesor)
            db.commit()
        except Exception as e:
            db.rollback()
            raise BadRequestException(f"Error al eliminar profesor: {str(e)}")

    # ==================== ASIGNACIÓN CURSO-MATERIA ====================

    @staticmethod
    def asignar_curso_materia(db: Session, data: AsignarCursoMateriaDTO) -> ProfesorCursoMateriaResponseDTO:
        """Asigna un curso y materia a un profesor"""
        # Validar que el profesor existe
        profesor = ProfesorRepository.get_by_id(db, data.id_profesor)
        if not profesor:
            raise NotFoundException(f"Profesor con ID {data.id_profesor} no encontrado")
        
        # Validar que el curso existe
        curso = ProfesorRepository.get_curso_by_id(db, data.id_curso)
        if not curso:
            raise NotFoundException(f"Curso con ID {data.id_curso} no encontrado")
        
        # Validar que la materia existe
        materia = ProfesorRepository.get_materia_by_id(db, data.id_materia)
        if not materia:
            raise NotFoundException(f"Materia con ID {data.id_materia} no encontrada")
        
        # Verificar si ya existe la asignación
        asignacion_existente = ProfesorRepository.get_asignacion(db, data.id_profesor, data.id_curso, data.id_materia)
        if asignacion_existente:
            raise BadRequestException("Esta asignación ya existe")
        
        try:
            nueva_asignacion = ProfesorCursoMateria(
                id_profesor=data.id_profesor,
                id_curso=data.id_curso,
                id_materia=data.id_materia
            )
            
            asignacion_creada = ProfesorRepository.asignar_curso_materia(db, nueva_asignacion)
            db.commit()
            
            persona = ProfesorRepository.get_persona_by_id(db, profesor.id_persona)
            nombre_profesor = f"{persona.nombres} {persona.apellido_paterno}"
            
            return ProfesorCursoMateriaResponseDTO(
                id_profesor=data.id_profesor,
                id_curso=data.id_curso,
                id_materia=data.id_materia,
                nombre_profesor=nombre_profesor,
                nombre_curso=curso.nombre_curso,
                nombre_materia=materia.nombre_materia
            )
            
        except Exception as e:
            db.rollback()
            raise BadRequestException(f"Error al asignar curso y materia: {str(e)}")

    @staticmethod
    def get_asignaciones_profesor(db: Session, id_profesor: int) -> List[ProfesorCursoMateriaResponseDTO]:
        """Obtiene todas las asignaciones de un profesor"""
        profesor = ProfesorRepository.get_by_id(db, id_profesor)
        if not profesor:
            raise NotFoundException(f"Profesor con ID {id_profesor} no encontrado")
        
        asignaciones = ProfesorRepository.get_asignaciones_profesor(db, id_profesor)
        response_list = []
        
        persona = ProfesorRepository.get_persona_by_id(db, profesor.id_persona)
        nombre_profesor = f"{persona.nombres} {persona.apellido_paterno}"
        
        for asignacion in asignaciones:
            curso = ProfesorRepository.get_curso_by_id(db, asignacion.id_curso)
            materia = ProfesorRepository.get_materia_by_id(db, asignacion.id_materia)
            
            response_list.append(ProfesorCursoMateriaResponseDTO(
                id_profesor=asignacion.id_profesor,
                id_curso=asignacion.id_curso,
                id_materia=asignacion.id_materia,
                nombre_profesor=nombre_profesor,
                nombre_curso=curso.nombre_curso if curso else "N/A",
                nombre_materia=materia.nombre_materia if materia else "N/A"
            ))
        
        return response_list

    @staticmethod
    def eliminar_asignacion(db: Session, id_profesor: int, id_curso: int, id_materia: int):
        """Elimina una asignación de curso-materia"""
        try:
            # El repository ahora retorna el número de filas eliminadas
            result = ProfesorRepository.eliminar_asignacion(db, id_profesor, id_curso, id_materia)
            
            if result == 0:
                raise NotFoundException("Asignación no encontrada")
            
            db.commit()
        except NotFoundException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise BadRequestException(f"Error al eliminar asignación: {str(e)}")

    # ==================== MÉTODOS AUXILIARES ====================

    @staticmethod
    def _build_response_dto(profesor: Profesor, persona: Persona) -> ProfesorResponseDTO:
        """Construye el DTO de respuesta combinando profesor y persona"""
        return ProfesorResponseDTO(
            id_profesor=profesor.id_profesor,
            id_persona=persona.id_persona,
            ci=persona.ci,
            nombres=persona.nombres,
            apellido_paterno=persona.apellido_paterno,
            apellido_materno=persona.apellido_materno,
            direccion=persona.direccion,
            telefono=persona.telefono,
            correo=persona.correo,
            id_cargo=persona.id_cargo,
            estado_laboral=persona.estado_laboral.value if persona.estado_laboral else None,
            anos_experiencia=persona.anos_experiencia,
            fecha_ingreso=persona.fecha_ingreso,
            fecha_retiro=persona.fecha_retiro,
            motivo_retiro=persona.motivo_retiro,
            is_active=persona.is_active,
            especialidad=profesor.especialidad,
            titulo_academico=profesor.titulo_academico,
            nivel_enseñanza=profesor.nivel_enseñanza,
            observaciones=profesor.observaciones
        )