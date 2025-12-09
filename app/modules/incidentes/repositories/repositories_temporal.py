# app\modules\incidentes\respositories\respositories_temporal.py
from sqlalchemy.orm import Session
from app.modules.administracion.models.persona_models import Estudiante
from app.modules.incidentes.models.models_incidentes import SituacionIncidente
from app.shared.models import Persona

def get_estudiantes_repo(db: Session):
    estudiantes = db.query(Estudiante).all()
    return [
        {"id": e.id_estudiante, "nombre": e.nombre_completo}
        for e in estudiantes
    ]

def get_profesores_repo(db: Session):
    profesores = db.query(Persona).filter(Persona.tipo_persona == "profesor").all()
    return [
        {"id": p.id_persona, "nombre": p.nombre_completo}
        for p in profesores
    ]

def get_situaciones_repo(db: Session):
    situaciones = db.query(SituacionIncidente).all()
    return [
        {
            "id": s.id_situacion,
            "nombre": s.nombre_situacion,
            "nivel": s.nivel_gravedad
        }
        for s in situaciones
    ]
