from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.incidentes.repositories.repositories_incidentes import IncidenteRepository
from app.modules.incidentes.models.models_incidentes import Incidente
from app.modules.incidentes.dto.dto_incidentes import IncidenteResponseDTO

from app.modules.incidentes.dto.dto_modificaciones import ModificacionCreateDTO
from app.modules.incidentes.services.services_modificaciones import registrar_modificacion_service


class IncidenteService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = IncidenteRepository()

    def crear_incidente(self, dto):
        incidente = Incidente(
            fecha=dto.fecha,
            antecedentes=dto.antecedentes,
            acciones_tomadas=dto.acciones_tomadas,
            seguimiento=dto.seguimiento,
            estado=dto.estado,
            id_responsable=dto.id_responsable
        )

        return self.repo.create_with_relations(self.db, incidente, dto)

    def obtener_incidentes(self):
        incidentes = self.repo.get_all_with_usuario(self.db)
        return [
            IncidenteResponseDTO(
                id_incidente=inc.id_incidente,
                fecha=inc.fecha,
                antecedentes=inc.antecedentes,
                acciones_tomadas=inc.acciones_tomadas,
                seguimiento=inc.seguimiento,
                estado=inc.estado,
                id_responsable=inc.id_responsable,
                responsable_usuario=inc.responsable.usuario if inc.responsable else None
            )
            for inc in incidentes
        ]

    def modificar_incidente(self, id_incidente: int, dto):
        incidente = self.db.query(Incidente).filter(
            Incidente.id_incidente == id_incidente
        ).first()

        if not incidente:
            raise HTTPException(status_code=404, detail="Incidente no encontrado")

        campos = ["antecedentes", "acciones_tomadas", "seguimiento", "estado", "id_responsable"]

        for campo in campos:
            nuevo_valor = getattr(dto, campo)
            valor_actual = getattr(incidente, campo)

            if nuevo_valor is not None and nuevo_valor != valor_actual:
                registro = ModificacionCreateDTO(
                    id_incidente=id_incidente,
                    id_usuario=dto.id_usuario_modifica,
                    campo_modificado=campo,
                    valor_anterior=str(valor_actual) if valor_actual else None,
                    valor_nuevo=str(nuevo_valor)
                )
                registrar_modificacion_service(self.db, registro)
                setattr(incidente, campo, nuevo_valor)

        return self.repo.update(self.db, incidente)
