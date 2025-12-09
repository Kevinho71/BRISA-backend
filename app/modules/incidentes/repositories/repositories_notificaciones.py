# app/modules/incidentes/repositories/repositories_notificaciones.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.incidentes.models.models_incidentes import Notificacion


class NotificacionRepository:

    def create(self, db: Session, notificacion: Notificacion) -> Notificacion:
        db.add(notificacion)
        db.commit()
        db.refresh(notificacion)
        return notificacion

    def get_by_id(self, db: Session, id_notificacion: int) -> Optional[Notificacion]:
        return (
            db.query(Notificacion)
            .filter(Notificacion.id_notificacion == id_notificacion)
            .first()
        )

    def get_by_usuario(
        self,
        db: Session,
        id_usuario: int,
        solo_no_leidas: bool = False,
        limit: Optional[int] = None,
    ) -> List[Notificacion]:
        query = db.query(Notificacion).filter(Notificacion.id_usuario == id_usuario)

        if solo_no_leidas:
            query = query.filter(Notificacion.leido == False)  # noqa: E712

        # Ordenar de la más nueva a la más antigua
        query = query.order_by(Notificacion.fecha.desc())

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def marcar_como_leida(
        self,
        db: Session,
        notificacion: Notificacion,
        commit: bool = True,
    ) -> Notificacion:
        notificacion.leido = True
        if commit:
            db.commit()
            db.refresh(notificacion)
        return notificacion

    def marcar_todas_como_leidas(self, db: Session, id_usuario: int) -> int:
        result = (
            db.query(Notificacion)
            .filter(Notificacion.id_usuario == id_usuario, Notificacion.leido == False)  # noqa: E712
            .update({Notificacion.leido: True}, synchronize_session=False)
        )
        db.commit()
        return result

    def delete(self, db: Session, notificacion: Notificacion, commit: bool = True) -> None:
        db.delete(notificacion)
        if commit:
            db.commit()
