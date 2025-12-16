from sqlalchemy.orm import Session
from app.modules.estudiantes.models.Materia import Materia
from app.modules.administracion.dto.materia_dto import MateriaCreateDTO, MateriaUpdateDTO

class MateriaRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Materia).all()

    @staticmethod
    def get_by_id(db: Session, materia_id: int):
        return db.query(Materia).filter(Materia.id_materia == materia_id).first()

    @staticmethod
    def create(db: Session, materia_dto: MateriaCreateDTO):
        db_materia = Materia(
            nombre_materia=materia_dto.nombre_materia,
            nivel=materia_dto.nivel
        )
        db.add(db_materia)
        db.commit()
        db.refresh(db_materia)
        return db_materia

    @staticmethod
    def update(db: Session, materia_id: int, materia_dto: MateriaUpdateDTO):
        db_materia = db.query(Materia).filter(Materia.id_materia == materia_id).first()
        if db_materia:
            db_materia.nombre_materia = materia_dto.nombre_materia
            db_materia.nivel = materia_dto.nivel
            db.commit()
            db.refresh(db_materia)
        return db_materia

    @staticmethod
    def delete(db: Session, materia_id: int):
        db_materia = db.query(Materia).filter(Materia.id_materia == materia_id).first()
        if db_materia:
            db.delete(db_materia)
            db.commit()
            return True
        return False
