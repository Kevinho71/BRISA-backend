# app/modules/esquelas/services/esquela_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.esquelas.models.esquela_models import Esquela
from app.modules.esquelas.repositories.esquela_repository import EsquelaRepository
from app.modules.esquelas.dto.esquela_dto import EsquelaBaseDTO
from app.modules.usuarios.models.usuario_models import Usuario
from app.shared.permission_mapper import puede_ver_esquela, puede_ver_todas_esquelas
from datetime import date
from typing import Optional


class EsquelaService:

    @staticmethod
    def listar_esquelas(db: Session, current_user: Usuario = None):
        """
        Lista esquelas según permisos del usuario.
        - Admin/Regente: Ve todas
        - Profesor: Ve solo las que él asignó
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
            )
        
        # Si puede ver todas, retornar todas
        if puede_ver_todas_esquelas(current_user):
            return EsquelaRepository.get_all(db)
        
        # Si es profesor, filtrar por sus esquelas
        if current_user.id_persona:
            return EsquelaRepository.get_by_profesor(db, current_user.id_persona)
        
        # Si no tiene permisos, retornar vacío
        return []

    @staticmethod
    def listar_esquelas_con_filtros(
        db: Session,
        name: Optional[str] = None,
        course_id: Optional[int] = None,
        tipo: Optional[str] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
        current_user: Usuario = None
    ):
        """
        Lista esquelas con filtros avanzados según permisos.
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
            )
        
        # Determinar si debe filtrar por profesor
        id_profesor_filtro = None
        if not puede_ver_todas_esquelas(current_user):
            id_profesor_filtro = current_user.id_persona
        
        return EsquelaRepository.get_with_filters(
            db=db,
            name=name,
            course_id=course_id,
            tipo=tipo,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            year=year,
            month=month,
            page=page,
            page_size=page_size,
            id_profesor=id_profesor_filtro
        )

    @staticmethod
    def obtener_esquela(db: Session, id: int, current_user: Usuario = None):
        """Obtiene una esquela validando permisos"""
        esquela = EsquelaRepository.get_by_id(db, id)
        
        if not esquela:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Esquela no encontrada"
            )
        
        # Validar que el usuario pueda ver esta esquela
        if current_user and not puede_ver_esquela(current_user, esquela.id_profesor):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver esta esquela"
            )
        
        return esquela

    @staticmethod
    def obtener_agregado_por_curso(db: Session, year: Optional[int] = None):
        """
        Obtiene cantidad de esquelas de reconocimiento y orientación por curso
        """
        return EsquelaRepository.get_aggregate_by_course(db, year)

    @staticmethod
    def obtener_esquelas_estudiante(
        db: Session,
        student_id: int,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ):
        """
        Obtiene todas las esquelas de un estudiante con conteo de códigos
        """
        return EsquelaRepository.get_by_student_with_date_range(
            db, student_id, fecha_desde, fecha_hasta
        )

    @staticmethod
    def obtener_agregado_por_periodo(db: Session, group_by: str = "year"):
        """
        Obtiene agregación de esquelas por año o mes
        """
        return EsquelaRepository.get_aggregate_by_year_month(db, group_by)

    @staticmethod
    def crear_esquela(db: Session, esquela_data: EsquelaBaseDTO, current_user: Usuario = None):
        # Validación: profesor solo puede crear sus propias esquelas
        if current_user and not puede_ver_todas_esquelas(current_user):
            if esquela_data.id_profesor != current_user.id_persona:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo puede asignar esquelas en su propio nombre"
                )
        
        nueva_esquela = Esquela(
            id_estudiante=esquela_data.id_estudiante,
            id_profesor=esquela_data.id_profesor,
            id_registrador=esquela_data.id_registrador,
            fecha=esquela_data.fecha,
            observaciones=esquela_data.observaciones
        )
        return EsquelaRepository.create(db, nueva_esquela, esquela_data.codigos)

    @staticmethod
    def eliminar_esquela(db: Session, id: int):
        esquela = EsquelaRepository.delete(db, id)
        if not esquela:
            raise HTTPException(status_code=404, detail="Esquela no encontrada")
        return esquela

