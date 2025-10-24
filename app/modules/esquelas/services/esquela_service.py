# app/modules/esquelas/services/esquela_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.esquelas.models.esquela_models import Esquela
from app.modules.esquelas.repositories.esquela_repository import EsquelaRepository
from app.modules.esquelas.dto.esquela_dto import EsquelaBaseDTO

class EsquelaService:

    @staticmethod
    def listar_esquelas(db: Session):
        return EsquelaRepository.get_all(db)

    @staticmethod
    def obtener_esquela(db: Session, id: int):
        esquela = EsquelaRepository.get_by_id(db, id)
        if not esquela:
            raise HTTPException(status_code=404, detail="Esquela no encontrada")
        return esquela

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
