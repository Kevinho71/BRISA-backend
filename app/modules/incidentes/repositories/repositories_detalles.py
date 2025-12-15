from sqlalchemy.orm import Session, joinedload
from app.modules.incidentes.models.models_incidentes import Incidente


class DetallesRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_incidente(self, id_incidente: int):
        return (
            self.db.query(Incidente)
            .options(
                joinedload(Incidente.estudiantes),
                joinedload(Incidente.profesores),
                joinedload(Incidente.situaciones),
            )
            .filter(Incidente.id_incidente == id_incidente)
            .first()
        )
