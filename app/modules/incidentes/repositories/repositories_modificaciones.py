# app/modules/incidentes/repositories/repositories_modificaciones.py

from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import HistorialDeModificacion
from app.modules.incidentes.dto.dto_modificaciones import ModificacionCreateDTO

def crear_modificacion_repo(db: Session, dto: ModificacionCreateDTO):
    nueva = HistorialDeModificacion(
        id_incidente=dto.id_incidente,
        id_usuario=dto.id_usuario,  # ✅ puede ser None
        campo_modificado=dto.campo_modificado,
        valor_anterior=dto.valor_anterior,
        valor_nuevo=dto.valor_nuevo
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def obtener_modificaciones_incidente_repo(db: Session, id_incidente: int):
    return (
        db.query(HistorialDeModificacion)
        .filter(HistorialDeModificacion.id_incidente == id_incidente)
        .order_by(HistorialDeModificacion.fecha_cambio.desc())
        .all()
    )
