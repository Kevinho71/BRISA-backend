from app.modules.incidentes.repositories.repositories_detalles import DetallesRepository
from app.modules.incidentes.dto.dto_detalles import (
    IncidenteDetalles, EstudianteItem, ProfesorItem, SituacionItem
)


class DetallesService:
    def __init__(self, db):
        self.repo = DetallesRepository(db)

    def obtener_detalles(self, id_incidente: int):
        inc = self.repo.obtener_incidente(id_incidente)
        if inc is None:
            return None

        estudiantes = [
            EstudianteItem(
                id_estudiante=e.id_estudiante,
                # si existe @property nombre_completo en tu modelo Estudiante, úsalo:
                nombre=getattr(e, "nombre_completo", f"{e.nombres} {e.apellido_paterno} {e.apellido_materno or ''}".strip()),
            )
            for e in (inc.estudiantes or [])
        ]

        profesores = [
            ProfesorItem(
                id_persona=p.id_persona,
                nombre=f"{p.nombres} {p.apellido_paterno} {p.apellido_materno or ''}".strip(),
            )
            for p in (inc.profesores or [])
        ]

        situaciones = [
            SituacionItem(
                id_situacion=s.id_situacion,
                nombre_situacion=s.nombre_situacion,
                nivel_gravedad=s.nivel_gravedad,
            )
            for s in (inc.situaciones or [])
        ]

        return IncidenteDetalles(
            id_incidente=inc.id_incidente,
            fecha=inc.fecha,
            antecedentes=inc.antecedentes,
            acciones_tomadas=inc.acciones_tomadas,
            seguimiento=inc.seguimiento,
            estado=inc.estado,
            id_responsable=inc.id_responsable,
            estudiantes=estudiantes,
            profesores=profesores,
            situaciones=situaciones,
        )
