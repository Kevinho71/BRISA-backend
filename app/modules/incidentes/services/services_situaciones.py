# app\modules\incidentes\services\services_situaciones.py
from fastapi import HTTPException
from app.modules.incidentes.repositories.repositories_situaciones import SituacionRepository


class SituacionService:

    def __init__(self, db):
        self.db = db
        self.repo = SituacionRepository()

    def crear(self, dto):
        return self.repo.create(self.db, dto)

    def listar_por_area(self, id_area: int):
        return self.repo.get_all_by_area(self.db, id_area)

    def listar_todas(self):
        return self.repo.get_all(self.db)

    def actualizar(self, id_situacion: int, dto):
        situacion = self.repo.get_by_id(self.db, id_situacion)
        if not situacion:
            raise HTTPException(status_code=404, detail="Situación no encontrada")
        return self.repo.update(self.db, situacion, dto)

    def eliminar(self, id_situacion: int):
        situacion = self.repo.get_by_id(self.db, id_situacion)
        if not situacion:
            raise HTTPException(status_code=404, detail="Situación no encontrada")
        self.repo.delete(self.db, situacion)
        return {"message": "Situación eliminada correctamente"}
