# app/modules/incidentes/services/services_derivaciones.py

from sqlalchemy.orm import Session

from app.modules.incidentes.models.models_incidentes import Incidente
from app.modules.incidentes.dto.dto_derivaciones import DerivacionCreate
from app.modules.incidentes.repositories.repositories_derivaciones import DerivacionRepository

from app.modules.incidentes.dto.dto_modificaciones import ModificacionCreateDTO
from app.modules.incidentes.services.services_modificaciones import registrar_modificacion_service


class DerivacionService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = DerivacionRepository(db)

    def derivar(self, id_incidente: int, data: DerivacionCreate):

        # 1. Validación
        incidente = self.db.query(Incidente).filter(
            Incidente.id_incidente == id_incidente
        ).first()

        if not incidente:
            raise ValueError("Incidente no encontrado")

        # Guardar valores previos
        estado_anterior = incidente.estado
        responsable_anterior = incidente.id_responsable

        # 2. Crear derivación
        derivacion = self.repo.crear(
            id_incidente=id_incidente,
            data=data.dict()
        )

        # 3. Actualizar incidente
        incidente.estado = "derivado"
        incidente.id_responsable = data.id_quien_recibe
        self.db.commit()
        self.db.refresh(incidente)

        # 4. Registrar historial usando servicios_modificaciones.py
        registro = ModificacionCreateDTO(
            id_incidente=id_incidente,
            id_usuario=data.id_quien_deriva,
            campo_modificado="derivación",
            valor_anterior=f"estado={estado_anterior}, id_responsable={responsable_anterior}",
            valor_nuevo=f"estado=derivado, id_responsable={data.id_quien_recibe}"
        )

        registrar_modificacion_service(self.db, registro)

        return derivacion
