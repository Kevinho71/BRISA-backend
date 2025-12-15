# app\modules\incidentes\repositories\repositories_adjuntos.py

from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import Adjunto

class AdjuntoRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: dict):
        adj = Adjunto(**data)
        self.db.add(adj)
        self.db.commit()
        self.db.refresh(adj)
        return adj

    def obtener_por_incidente(self, id_incidente: int):
        return (
            self.db.query(Adjunto)
            .filter(Adjunto.id_incidente == id_incidente)
            .all()
        )

    def obtener_por_id(self, id_adjunto: int):
        return (
            self.db.query(Adjunto)
            .filter(Adjunto.id_adjunto == id_adjunto)
            .first()
        )

    def borrar_por_id(self, id_adjunto: int):
        adj = self.obtener_por_id(id_adjunto)
        if not adj:
            return False

        self.db.delete(adj)
        self.db.commit()
        return True
