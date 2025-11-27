# app/modules/incidentes/services/services_modificaciones.py

from sqlalchemy.orm import Session
from app.modules.incidentes.dto.dto_modificaciones import ModificacionCreateDTO
from app.modules.incidentes.repositories.repositories_modificaciones import (
    crear_modificacion_repo,
    obtener_modificaciones_incidente_repo
)

def registrar_modificacion_service(db: Session, dto: ModificacionCreateDTO):
    return crear_modificacion_repo(db, dto)


def historial_incidente_service(db: Session, id_incidente: int):
    return obtener_modificaciones_incidente_repo(db, id_incidente)
