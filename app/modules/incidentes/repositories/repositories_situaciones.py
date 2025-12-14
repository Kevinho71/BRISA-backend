# app\modules\incidentes\repositories\repositories_situaciones.py
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import SituacionIncidente

class SituacionRepository:

    def create(self, db: Session, dto):
        nueva = SituacionIncidente(**dto.dict())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    def get_by_id(self, db: Session, id_situacion: int):
        return db.query(SituacionIncidente).filter(
            SituacionIncidente.id_situacion == id_situacion
        ).first()

    def get_all(self, db: Session):
        return db.query(SituacionIncidente).all()

    def update(self, db: Session, situacion, dto):
        data = dto.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(situacion, key, value)
        db.commit()
        db.refresh(situacion)
        return situacion

    def delete(self, db: Session, situacion):
        db.delete(situacion)
        db.commit()
        return True
