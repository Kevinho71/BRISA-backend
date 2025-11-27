# app\modules\incidentes\repositories\repositories_incidentes.py
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import (
    Incidente,
    SituacionIncidente
)
from app.modules.administracion.models.persona_models import Persona, Estudiante

class IncidenteRepository:

    def create(self, db: Session, incidente: Incidente):
        db.add(incidente)
        db.commit()
        db.refresh(incidente)
        return incidente
    
    def get_all(self, db: Session):
        return db.query(Incidente).all()

    def add_relations(self, db: Session, incidente: Incidente, dto):

        if dto.estudiantes:
            estudiantes = db.query(Estudiante).filter(
                Estudiante.id_estudiante.in_(dto.estudiantes)
            ).all()
            incidente.estudiantes.extend(estudiantes)

        if dto.profesores:
            profesores = db.query(Persona).filter(
                Persona.id_persona.in_(dto.profesores)
            ).all()
            incidente.profesores.extend(profesores)

        if dto.situaciones:
            situaciones = db.query(SituacionIncidente).filter(
                SituacionIncidente.id_situacion.in_(dto.situaciones)
            ).all()
            incidente.situaciones.extend(situaciones)

        db.commit()
        db.refresh(incidente)
        return incidente
    
    def update(self, db: Session, incidente: Incidente):
        db.add(incidente)
        db.commit()
        db.refresh(incidente)
        return incidente
