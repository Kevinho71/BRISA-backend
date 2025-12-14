# app/modules/incidentes/repositories/repositories_detalles.py

from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import Incidente


class DetallesRepository:

    def __init__(self, db: Session):
        self.db = db

    # INCIDENTE
    def obtener_incidente(self, id_incidente: int):
        return (
            self.db.query(Incidente)
            .filter(Incidente.id_incidente == id_incidente)
            .first()
        )

    # ESTUDIANTES
    def obtener_estudiantes(self, incidente: Incidente):
        return incidente.estudiantes

    # PROFESORES
    def obtener_profesores(self, incidente: Incidente):
        return incidente.profesores

    # SITUACIONES
    def obtener_situaciones(self, incidente: Incidente):
        return incidente.situaciones
