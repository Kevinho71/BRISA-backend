# app\modules\incidentes\repositories\repositories_areas.py
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import AreaIncidente


class AreaRepository:

    def get_all(self, db: Session):
        return db.query(AreaIncidente).all()

    def get_by_id(self, db: Session, id_area: int):
        return db.query(AreaIncidente).filter(
            AreaIncidente.id_area == id_area
        ).first()

    def create(self, db: Session, dto):
        area = AreaIncidente(**dto.dict())
        db.add(area)
        db.commit()
        db.refresh(area)
        return area

    def update(self, db: Session, id_area: int, dto):
        area = db.query(AreaIncidente).filter(
            AreaIncidente.id_area == id_area
        ).first()

        if not area:
            return None

        for key, value in dto.dict().items():
            setattr(area, key, value)

        db.commit()
        db.refresh(area)
        return area

    def delete(self, db: Session, id_area: int):
        area = db.query(AreaIncidente).filter(
            AreaIncidente.id_area == id_area
        ).first()

        if not area:
            return None

        db.delete(area)
        db.commit()
        return True
