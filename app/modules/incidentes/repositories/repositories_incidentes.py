# app\modules\incidentes\repositories\repositories_incidentes.py
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import (
    Incidente,
    SituacionIncidente
)
from app.modules.administracion.models.persona_models import Estudiante
from app.shared.models import Persona

class IncidenteRepository:

    def create_with_relations(self, db: Session, incidente: Incidente, dto):
        # relaciones
        if dto.estudiantes:
            estudiantes = db.query(Estudiante).filter(
                Estudiante.id_estudiante.in_(dto.estudiantes)
            ).all()
            incidente.estudiantes = estudiantes

        if dto.profesores:
            profesores = db.query(Persona1).filter(
                Persona1.id_persona.in_(dto.profesores)
            ).all()
            incidente.profesores = profesores

        if dto.situaciones:
            situaciones = db.query(SituacionIncidente).filter(
                SituacionIncidente.id_situacion.in_(dto.situaciones)
            ).all()
            incidente.situaciones = situaciones

        db.add(incidente)
        db.commit()
        db.refresh(incidente)
        return incidente

    def get_all_with_usuario(self, db: Session):
        return db.query(Incidente).options(joinedload(Incidente.responsable)).all()

    def update(self, db: Session, incidente: Incidente):
        db.add(incidente)
        db.commit()
        db.refresh(incidente)
        return incidente
