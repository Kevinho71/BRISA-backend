# app/modules/incidentes/repositories/repositories_derivaciones.py

from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import Derivacion

class DerivacionRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, id_incidente: int, data: dict):
        deriv = Derivacion(
            id_incidente=id_incidente,
            **data
        )
        self.db.add(deriv)
        self.db.commit()
        self.db.refresh(deriv)
        return deriv
