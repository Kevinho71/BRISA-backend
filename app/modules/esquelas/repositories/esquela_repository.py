# app/modules/esquelas/repositories/esquela_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.modules.esquelas.models.esquela_models import Esquela, CodigoEsquela

class EsquelaRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Esquela).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Esquela).filter(Esquela.id_esquela == id).first()

    @staticmethod
    def create(db: Session, esquela: Esquela, codigo_ids: list[int]):
        db.add(esquela)
        db.commit()
        db.refresh(esquela)

        # Insertar relaciones en la tabla intermedia usando SQL directo
        for cid in codigo_ids:
            db.execute(
                text("INSERT INTO esquelas_codigos (id_esquela, id_codigo) VALUES (:id_esquela, :id_codigo)"),
                {"id_esquela": esquela.id_esquela, "id_codigo": cid}
            )
        db.commit()
        db.refresh(esquela)  # Refrescar para cargar las relaciones
        return esquela

    @staticmethod
    def delete(db: Session, id: int):
        esquela = db.query(Esquela).filter(Esquela.id_esquela == id).first()
        if esquela:
            db.delete(esquela)
            db.commit()
        return esquela
