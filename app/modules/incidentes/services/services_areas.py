# app\modules\incidentes\services\services_areas.py
from fastapi import HTTPException
from app.modules.incidentes.repositories.repositories_areas import AreaRepository

class AreaService:

    def __init__(self):
        self.repo = AreaRepository()

    def listar_areas(self, db):
        return self.repo.get_all(db)

    def obtener_area(self, db, id_area: int):
        area = self.repo.get_by_id(db, id_area)
        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")
        return area

    def crear_area(self, db, dto):
        return self.repo.create(db, dto)

    def actualizar_area(self, db, id_area, dto):
        area = self.repo.update(db, id_area, dto)
        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")
        return area

    def eliminar_area(self, db, id_area):
        eliminado = self.repo.delete(db, id_area)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Área no encontrada")
        return {"message": "Área eliminada correctamente"}
