from sqlalchemy.orm import Session, joinedload
from sqlalchemy import delete

from app.modules.incidentes.models.models_incidentes import (
    Incidente,
    SituacionIncidente,
    incidentes_profesores,   # ✅ IMPORTA LA TABLA INTERMEDIA
)
from app.modules.administracion.models.persona_models import Estudiante
from app.modules.usuarios.models.usuario_models import Persona1


class IncidenteRepository:

    def create_with_relations(self, db: Session, incidente: Incidente, dto):
        # 1) Guarda incidente primero para obtener id_incidente
        db.add(incidente)
        db.flush()  # ✅ asegura incidente.id_incidente

        # ---- estudiantes ----
        if dto.estudiantes:
            estudiantes = db.query(Estudiante).filter(
                Estudiante.id_estudiante.in_(dto.estudiantes)
            ).all()
            incidente.estudiantes = estudiantes

        # ---- profesores (SIN ORM, porque viewonly=True) ----
        if dto.profesores:
            # (Opcional) validar que existan en personas
            existentes = db.query(Persona1.id_persona).filter(
                Persona1.id_persona.in_(dto.profesores)
            ).all()
            existentes_ids = {x[0] for x in existentes}

            # Inserta solo los válidos (o si prefieres: lanzar error si falta alguno)
            filas = [
                {"id_incidente": incidente.id_incidente, "id_profesor": pid}
                for pid in dto.profesores
                if pid in existentes_ids
            ]

            if filas:
                db.execute(incidentes_profesores.insert(), filas)

            # ✅ para que al devolver/leer se recargue la relación
            db.expire(incidente, ["profesores"])

        # ---- situaciones ----
        if dto.situaciones:
            situaciones = db.query(SituacionIncidente).filter(
                SituacionIncidente.id_situacion.in_(dto.situaciones)
            ).all()
            incidente.situaciones = situaciones

        db.commit()
        db.refresh(incidente)
        return incidente

    def get_all_with_usuario(self, db: Session):
        return db.query(Incidente).options(
            joinedload(Incidente.responsable)
        ).all()

    def update(self, db: Session, incidente: Incidente):
        db.add(incidente)
        db.commit()
        db.refresh(incidente)
        return incidente
