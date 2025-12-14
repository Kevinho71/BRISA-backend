# app/modules/incidentes/services/services_detalles.py

from app.modules.incidentes.repositories.repositories_detalles import DetallesRepository
from app.modules.incidentes.dto.dto_detalles import IncidenteDetalles


class DetallesService:

    def __init__(self, db):
        self.repo = DetallesRepository(db)

    def obtener_detalles(self, id_incidente: int):
        inc = self.repo.obtener_incidente(id_incidente)

        if inc is None:
            return None

        return IncidenteDetalles(
            id_incidente=inc.id_incidente,
            fecha=inc.fecha,
            antecedentes=inc.antecedentes,
            acciones_tomadas=inc.acciones_tomadas,
            seguimiento=inc.seguimiento,
            estado=inc.estado,
            id_responsable=inc.id_responsable,

            estudiantes=self.repo.obtener_estudiantes(inc),
            profesores=self.repo.obtener_profesores(inc),
            situaciones=self.repo.obtener_situaciones(inc),
        )
