# app\modules\incidentes\services\services_notificaciones.py
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.incidentes.models.models_incidentes import Notificacion
from app.modules.incidentes.repositories.repositories_notificaciones import NotificacionRepository
from app.modules.incidentes.dto.dto_notificaiones import NotificacionCreateDTO


class NotificacionService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = NotificacionRepository()

    #   CREAR NOTIFICACIÓN
    def crear_notificacion(self, dto: NotificacionCreateDTO) -> Notificacion:
        noti = Notificacion(
            id_usuario=dto.id_usuario,
            id_incidente=dto.id_incidente,
            id_derivacion=dto.id_derivacion,
            titulo=dto.titulo,
            mensaje=dto.mensaje,
        )
        return self.repo.create(self.db, noti)

    #   OBTENER UNA NOTIFICACIÓN
    def obtener_notificacion(self, id_notificacion: int) -> Notificacion:
        noti = self.repo.get_by_id(self.db, id_notificacion)
        if not noti:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        return noti

    #   LISTAR NOTIFICACIONES DE USUARIO
    def listar_por_usuario(
        self,
        id_usuario: int,
        solo_no_leidas: bool = False,
        limit: Optional[int] = None,
    ) -> List[Notificacion]:
        return self.repo.get_by_usuario(
            self.db,
            id_usuario=id_usuario,
            solo_no_leidas=solo_no_leidas,
            limit=limit,
        )

    #   MARCAR UNA COMO LEÍDA
    def marcar_como_leida(
        self,
        id_notificacion: int,
        id_usuario_actual: Optional[int] = None,
    ) -> Notificacion:
        noti = self.repo.get_by_id(self.db, id_notificacion)
        if not noti:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")

        if id_usuario_actual is not None and noti.id_usuario != id_usuario_actual:
            raise HTTPException(status_code=403, detail="No tiene permiso para esta notificación")

        return self.repo.marcar_como_leida(self.db, noti)

    #   MARCAR TODAS LAS NOTIFICACIONES LEÍDAS
    def marcar_todas_como_leidas(self, id_usuario: int) -> int:
        return self.repo.marcar_todas_como_leidas(self.db, id_usuario)
