"""Servicio para lógica de negocio de Cursos"""

from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException
from datetime import datetime

from app.modules.cursos.repositories.curso_repository import CursoRepository
from app.modules.cursos.dto.curso_dto import (
    CursoCreateDTO,
    CursoUpdateDTO,
    CursoResponseDTO,
    CursoListDTO,
    EstudianteBasicoDTO,
    CopiarGestionDTO,
    CopiarGestionResponseDTO,
    NivelEducativo
)


class CursoService:
    """Servicio para gestión de cursos"""
    
    # ============= CRUD Básico =============
    
    @staticmethod
    def crear_curso(db: Session, datos: CursoCreateDTO) -> CursoResponseDTO:
        """RF-CUR-001: Crear Curso"""
        datos_dict = datos.model_dump()
        
        # Mapear campos del DTO a campos de la base de datos
        nivel_valor = datos_dict['nivel_educativo'].value if isinstance(datos_dict['nivel_educativo'], NivelEducativo) else datos_dict['nivel_educativo']
        datos_bd = {
            'nombre_curso': datos_dict['nombre'],
            'nivel': nivel_valor.lower(),  # Convertir a minúsculas para BD (Inicial -> inicial)
            'gestion': datos_dict['gestion']
        }
        
        curso = CursoRepository.crear_curso(db, datos_bd)
        return CursoService._convertir_a_dto(curso)
    
    @staticmethod
    def obtener_todos(
        db: Session,
        gestion: Optional[str] = None,
        nivel: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> CursoListDTO:
        """RF-CUR-002: Listar Todos los Cursos"""
        # Si se especifica "current", usar año actual
        if gestion and gestion.lower() == 'current':
            gestion = str(datetime.now().year)
        # Si se pasa "all" o "todos" o None, no filtrar por gestión (mostrar todos)
        elif not gestion or gestion.lower() in ['all', 'todos', '*']:
            gestion = None
        
        # Convertir nivel a minúsculas para búsqueda en BD (Inicial -> inicial)
        nivel_bd = nivel.lower() if nivel else None
        
        cursos = CursoRepository.obtener_todos(db, gestion, nivel_bd, skip, limit)
        total = CursoRepository.contar_total(db, gestion, nivel_bd)
        
        cursos_dto = [CursoService._convertir_a_dto(curso) for curso in cursos]
        
        return CursoListDTO(
            total=total,
            cursos=cursos_dto
        )
    
    @staticmethod
    def obtener_por_id(db: Session, id_curso: int) -> CursoResponseDTO:
        """RF-CUR-003: Obtener Curso por ID"""
        curso = CursoRepository.obtener_por_id(db, id_curso)
        
        if not curso:
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        return CursoService._convertir_a_dto(curso)
    
    @staticmethod
    def actualizar_curso(
        db: Session,
        id_curso: int,
        datos: CursoUpdateDTO
    ) -> CursoResponseDTO:
        """RF-CUR-004: Actualizar Curso"""
        # Verificar que exista
        curso_existe = CursoRepository.obtener_por_id(db, id_curso)
        if not curso_existe:
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        # Preparar datos para actualizar - mapear campos del DTO a BD
        datos_dict = datos.model_dump(exclude_unset=True)
        datos_bd = {}
        
        if 'nombre' in datos_dict:
            datos_bd['nombre_curso'] = datos_dict['nombre']
        if 'nivel_educativo' in datos_dict:
            nivel = datos_dict['nivel_educativo']
            nivel_valor = nivel.value if isinstance(nivel, NivelEducativo) else nivel
            datos_bd['nivel'] = nivel_valor.lower()  # Convertir a minúsculas para BD
        if 'gestion' in datos_dict:
            datos_bd['gestion'] = datos_dict['gestion']
        # capacidad_maxima no se almacena en BD
        
        curso_actualizado = CursoRepository.actualizar_curso(db, id_curso, datos_bd)
        
        return CursoService._convertir_a_dto(curso_actualizado)
    
    @staticmethod
    def eliminar_curso(db: Session, id_curso: int) -> dict:
        """RF-CUR-005: Eliminar Curso"""
        # Verificar que exista
        curso = CursoRepository.obtener_por_id(db, id_curso)
        if not curso:
            raise HTTPException(
                status_code=404,
                detail=f"Curso con ID {id_curso} no encontrado"
            )
        
        nombre_curso = curso.nombre_curso
        
        # Eliminar (cascada automática en asignaciones)
        CursoRepository.eliminar_curso(db, id_curso)
        
        return {
            "mensaje": f"Curso '{nombre_curso}' eliminado exitosamente",
            "id_curso": id_curso
        }
    
    # ============= Filtros Avanzados =============
    
    @staticmethod
    def listar_por_gestion_nivel(
        db: Session,
        gestion: Optional[str] = None,
        nivel: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> CursoListDTO:
        """RF-CUR-006: Listar Cursos por Gestión y Nivel"""
        # Si no se especifica gestión, usar año actual
        if not gestion:
            gestion = str(datetime.now().year)
        
        # Validar nivel si se proporciona
        if nivel:
            niveles_validos = [n.value for n in NivelEducativo]
            if nivel not in niveles_validos:
                raise HTTPException(
                    status_code=400,
                    detail=f"Nivel '{nivel}' no válido. Niveles válidos: {', '.join(niveles_validos)}"
                )
        
        # Convertir nivel a minúsculas para búsqueda en BD (Inicial -> inicial)
        nivel_bd = nivel.lower() if nivel else None
        
        cursos = CursoRepository.obtener_por_gestion_nivel(db, gestion, nivel_bd, skip, limit)
        total = CursoRepository.contar_por_gestion_nivel(db, gestion, nivel_bd)
        
        cursos_dto = [CursoService._convertir_a_dto(curso) for curso in cursos]
        
        return CursoListDTO(
            total=total,
            cursos=cursos_dto
        )
    
    # ============= Gestión de Gestiones =============
    
    @staticmethod
    def copiar_cursos_entre_gestiones(
        db: Session,
        datos: CopiarGestionDTO
    ) -> CopiarGestionResponseDTO:
        """RF-CUR-007: Copiar Cursos entre Gestiones"""
        gestion_origen = datos.gestion_origen
        gestion_destino = datos.gestion_destino
        
        # Validar que gestiones sean diferentes
        if gestion_origen == gestion_destino:
            raise HTTPException(
                status_code=400,
                detail="La gestión origen y destino deben ser diferentes"
            )
        
        # Validar que existan cursos en la gestión origen
        if not CursoRepository.existe_gestion(db, gestion_origen):
            raise HTTPException(
                status_code=404,
                detail=f"No existen cursos en la gestión {gestion_origen}"
            )
        
        # Si ya existen cursos en la gestión destino, eliminarlos primero
        if CursoRepository.existe_gestion(db, gestion_destino):
            # Eliminar cursos existentes de la gestión destino
            CursoRepository.eliminar_cursos_por_gestion(db, gestion_destino)
        
        # Copiar cursos
        cursos_copiados = CursoRepository.copiar_cursos_entre_gestiones(
            db, gestion_origen, gestion_destino
        )
        
        return CopiarGestionResponseDTO(
            mensaje=f"Se copiaron {cursos_copiados} cursos de la gestión {gestion_origen} a {gestion_destino}",
            gestion_origen=gestion_origen,
            gestion_destino=gestion_destino,
            cursos_copiados=cursos_copiados
        )
    
    # ============= Utilidades =============
    
    @staticmethod
    def _convertir_a_dto(curso) -> CursoResponseDTO:
        """Convertir modelo a DTO - mapea campos de BD a formato API"""
        estudiantes_dto = [
            EstudianteBasicoDTO(
                id_estudiante=est.id_estudiante,
                ci=est.ci,
                nombres=est.nombres,
                apellido_paterno=est.apellido_paterno,
                apellido_materno=est.apellido_materno,
                estado=est.estado
            )
            for est in curso.estudiantes
        ]
        
        # Capitalizar el nivel para que coincida con el enum (inicial -> Inicial)
        nivel_capitalizado = curso.nivel.capitalize() if curso.nivel else curso.nivel
        
        return CursoResponseDTO(
            id=curso.id_curso,  # Mapear id_curso -> id
            nombre=curso.nombre_curso,  # Mapear nombre_curso -> nombre
            nivel_educativo=nivel_capitalizado,  # Mapear y capitalizar nivel -> nivel_educativo
            gestion=curso.gestion,
            capacidad_maxima=30,  # Valor por defecto, ya que no está en BD
            estudiantes=estudiantes_dto
        )
