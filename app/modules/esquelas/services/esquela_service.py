# app/modules/esquelas/services/esquela_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.esquelas.models.esquela_models import Esquela
from app.modules.esquelas.repositories.esquela_repository import EsquelaRepository
from app.modules.esquelas.dto.esquela_dto import EsquelaBaseDTO
from datetime import date
from typing import Optional


class EsquelaService:

    @staticmethod
    def listar_esquelas(db: Session):
        return EsquelaRepository.get_all(db)

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
        page_size: int = 10
    ):
        """
        Lista esquelas con filtros avanzados
        """
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
            page_size=page_size
        )

    @staticmethod
    def obtener_esquela(db: Session, id: int):
        esquela = EsquelaRepository.get_by_id(db, id)
        if not esquela:
            raise HTTPException(status_code=404, detail="Esquela no encontrada")
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
    def crear_esquela(db: Session, esquela_data: EsquelaBaseDTO):
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

