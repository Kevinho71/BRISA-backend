from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.retiros_tempranos.repositories.solicitud_retiro_repository import SolicitudRetiroRepository
from app.modules.retiros_tempranos.repositories.estudiante_apoderado_repository import EstudianteApoderadoRepository
from app.modules.retiros_tempranos.repositories.motivo_retiro_repository import MotivoRetiroRepository
from app.modules.retiros_tempranos.repositories.autorizacion_retiro_repository import AutorizacionRetiroRepository
from app.modules.retiros_tempranos.repositories.estudiante_repository import EstudianteRepository

from app.modules.retiros_tempranos.models.SolicitudRetiro import SolicitudRetiro, EstadoSolicitudEnum, TipoSolicitudEnum
from app.modules.retiros_tempranos.models.AutorizacionesRetiro import AutorizacionRetiro, DecisionEnum

from app.modules.retiros_tempranos.dto.solicitud_retiro_dto import (
    SolicitudRetiroCreateDTO,
    SolicitudRetiroUpdateDTO,
    SolicitudRetiroResponseDTO,
    RecibirSolicitudDTO,
    DerivarSolicitudDTO,
    AprobarRechazarSolicitudDTO,
    CancelarSolicitudDTO
)

from app.modules.usuarios.models import Usuario


class SolicitudRetiroService:
    """Servicio para la gestión de solicitudes de retiro individual"""

    def __init__(self, db: Session):
        self.db = db
        self.solicitud_repo = SolicitudRetiroRepository(db)
        self.estudiante_apoderado_repo = EstudianteApoderadoRepository(db)
        self.motivo_repo = MotivoRetiroRepository(db)
        self.autorizacion_repo = AutorizacionRetiroRepository(db)
        self.estudiante_repo = EstudianteRepository(db)

    def crear_solicitud(
        self, 
        solicitud_dto: SolicitudRetiroCreateDTO, 
        id_apoderado: int
    ) -> SolicitudRetiroResponseDTO:
        """Apoderado crea una solicitud de retiro para su estudiante"""
        
        # Validar que el estudiante existe
        estudiante = self.estudiante_repo.get_by_id(solicitud_dto.id_estudiante)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado"
            )

        # Validar que el apoderado está relacionado con el estudiante
        relacion = self.db.query(self.db.query(
            self.estudiante_apoderado_repo.__class__.__table__
        ).filter_by(
            id_estudiante=solicitud_dto.id_estudiante,
            id_apoderado=id_apoderado
        ).exists()).scalar()
        
        if not relacion:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene autorización para crear solicitudes para este estudiante"
            )

        # Validar motivo
        motivo = self.motivo_repo.get_by_id(solicitud_dto.id_motivo)
        if not motivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Motivo de retiro no encontrado"
            )

        # Crear solicitud
        nueva_solicitud = SolicitudRetiro(
            id_estudiante=solicitud_dto.id_estudiante,
            id_apoderado=id_apoderado,
            id_motivo=solicitud_dto.id_motivo,
            tipo_solicitud=TipoSolicitudEnum.individual.value,
            foto_evidencia=solicitud_dto.foto_evidencia,
            id_solicitante=id_apoderado,
            fecha_hora_salida=solicitud_dto.fecha_hora_salida,
            fecha_hora_retorno_previsto=solicitud_dto.fecha_hora_retorno_previsto,
            observacion=solicitud_dto.observacion,
            estado=EstadoSolicitudEnum.pendiente.value
        )

        solicitud_creada = self.solicitud_repo.create(nueva_solicitud)
        return self._convertir_a_dto(solicitud_creada)

    def obtener_solicitud(self, id_solicitud: int) -> SolicitudRetiroResponseDTO:
        """Obtiene una solicitud por ID"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud de retiro no encontrada"
            )
        return self._convertir_a_dto(solicitud)

    def listar_solicitudes(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroResponseDTO]:
        """Lista todas las solicitudes"""
        solicitudes = self.solicitud_repo.get_all(skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_por_estudiante(
        self, 
        id_estudiante: int
    ) -> List[SolicitudRetiroResponseDTO]:
        """Lista solicitudes de un estudiante"""
        solicitudes = self.solicitud_repo.get_by_estudiante(id_estudiante)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_por_apoderado(
        self, 
        id_apoderado: int
    ) -> List[SolicitudRetiroResponseDTO]:
        """Lista solicitudes de un apoderado"""
        solicitudes = self.solicitud_repo.get_by_apoderado(id_apoderado)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_pendientes(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroResponseDTO]:
        """Lista solicitudes pendientes de recepción"""
        solicitudes = self.solicitud_repo.get_by_estado(EstadoSolicitudEnum.pendiente.value, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_recibidas(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroResponseDTO]:
        """Lista solicitudes recibidas (pendientes de derivar)"""
        solicitudes = self.solicitud_repo.get_by_estado(EstadoSolicitudEnum.recibida.value, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_derivadas_a_regente(
        self, 
        id_regente: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroResponseDTO]:
        """Lista solicitudes derivadas a un regente"""
        solicitudes = self.solicitud_repo.get_by_regente(id_regente, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def recibir_solicitud(
        self, 
        id_solicitud: int, 
        recibir_dto: RecibirSolicitudDTO, 
        id_recepcionista: int
    ) -> SolicitudRetiroResponseDTO:
        """Recepcionista marca solicitud como recibida"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.estado != EstadoSolicitudEnum.pendiente.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden recibir solicitudes en estado pendiente"
            )

        solicitud.estado = EstadoSolicitudEnum.recibida.value
        solicitud.id_recepcionista = id_recepcionista
        solicitud.fecha_recepcion = recibir_dto.fecha_hora_recepcion or datetime.now()

        solicitud_actualizada = self.solicitud_repo.update(solicitud)
        return self._convertir_a_dto(solicitud_actualizada)

    def derivar_solicitud(
        self, 
        id_solicitud: int, 
        derivar_dto: DerivarSolicitudDTO
    ) -> SolicitudRetiroResponseDTO:
        """Recepcionista deriva solicitud al regente"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.estado != EstadoSolicitudEnum.recibida.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden derivar solicitudes en estado recibida"
            )

        # Validar que el regente existe
        regente = self.db.query(Usuario).filter(Usuario.id_usuario == derivar_dto.id_regente).first()
        if not regente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Regente no encontrado"
            )

        solicitud.estado = EstadoSolicitudEnum.derivada.value
        solicitud.id_regente = derivar_dto.id_regente
        solicitud.fecha_derivacion = datetime.now()

        solicitud_actualizada = self.solicitud_repo.update(solicitud)
        return self._convertir_a_dto(solicitud_actualizada)

    def aprobar_rechazar_solicitud(
        self, 
        id_solicitud: int, 
        decision_dto: AprobarRechazarSolicitudDTO,
        id_regente: int
    ) -> SolicitudRetiroResponseDTO:
        """Regente aprueba o rechaza una solicitud"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.estado != EstadoSolicitudEnum.derivada.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden aprobar/rechazar solicitudes derivadas"
            )

        if solicitud.id_regente != id_regente:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el regente asignado puede aprobar/rechazar esta solicitud"
            )

        # Validar decisión
        if decision_dto.decision not in ["aprobada", "rechazada"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La decisión debe ser 'aprobada' o 'rechazada'"
            )

        if decision_dto.decision == "rechazada" and not decision_dto.motivo_rechazo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El motivo de rechazo es obligatorio"
            )

        # Actualizar estado
        solicitud.estado = decision_dto.decision

        # Crear autorización
        nueva_autorizacion = AutorizacionRetiro(
            id_solicitud=id_solicitud,
            id_regente=id_regente,
            decision=DecisionEnum.aprobada.value if decision_dto.decision == "aprobada" else DecisionEnum.rechazada.value,
            motivo_rechazo=decision_dto.motivo_rechazo,
            fecha_autorizacion=datetime.now()
        )
        autorizacion_creada = self.autorizacion_repo.create(nueva_autorizacion)

        solicitud.id_autorizacion = autorizacion_creada.id_autorizacion
        solicitud_actualizada = self.solicitud_repo.update(solicitud)

        return self._convertir_a_dto(solicitud_actualizada)

    def cancelar_solicitud(
        self, 
        id_solicitud: int, 
        cancelar_dto: CancelarSolicitudDTO,
        id_apoderado: int
    ) -> SolicitudRetiroResponseDTO:
        """Apoderado cancela su propia solicitud"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.id_apoderado != id_apoderado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el apoderado puede cancelar su solicitud"
            )

        if solicitud.estado in [EstadoSolicitudEnum.aprobada.value, EstadoSolicitudEnum.rechazada.value]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cancelar una solicitud ya aprobada o rechazada"
            )

        solicitud.estado = EstadoSolicitudEnum.cancelada.value
        solicitud.observacion = f"{solicitud.observacion or ''}\n[CANCELADA: {cancelar_dto.motivo_cancelacion}]"

        solicitud_actualizada = self.solicitud_repo.update(solicitud)
        return self._convertir_a_dto(solicitud_actualizada)

    def eliminar_solicitud(self, id_solicitud: int, id_apoderado: int) -> bool:
        """Elimina una solicitud (solo si está en pendiente)"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.id_apoderado != id_apoderado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el apoderado puede eliminar su solicitud"
            )

        if solicitud.estado != EstadoSolicitudEnum.pendiente.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar solicitudes pendientes"
            )

        return self.solicitud_repo.delete(id_solicitud)

    def _convertir_a_dto(self, solicitud: SolicitudRetiro) -> SolicitudRetiroResponseDTO:
        """Convierte modelo a DTO"""
        estudiante_nombre = None
        apoderado_nombre = None
        motivo_nombre = None
        curso_nombre = None

        if solicitud.estudiante:
            estudiante_nombre = f"{solicitud.estudiante.nombre} {solicitud.estudiante.apellido_paterno} {solicitud.estudiante.apellido_materno or ''}"
            if solicitud.estudiante.curso:
                curso_nombre = solicitud.estudiante.curso.nombre

        if solicitud.apoderado:
            apoderado_nombre = f"{solicitud.apoderado.nombre} {solicitud.apoderado.apellido_paterno}"

        if solicitud.motivo:
            motivo_nombre = solicitud.motivo.nombre

        return SolicitudRetiroResponseDTO(
            id_solicitud=solicitud.id_solicitud,
            id_estudiante=solicitud.id_estudiante,
            id_apoderado=solicitud.id_apoderado,
            id_motivo=solicitud.id_motivo,
            id_autorizacion=solicitud.id_autorizacion,
            tipo_solicitud=solicitud.tipo_solicitud,
            foto_evidencia=solicitud.foto_evidencia,
            id_solicitante=solicitud.id_solicitante,
            fecha_hora_salida=solicitud.fecha_hora_salida,
            fecha_hora_retorno_previsto=solicitud.fecha_hora_retorno_previsto,
            observacion=solicitud.observacion,
            fecha_hora_solicitud=solicitud.fecha_hora_solicitud,
            estado=solicitud.estado,
            id_recepcionista=solicitud.id_recepcionista,
            fecha_recepcion=solicitud.fecha_recepcion,
            id_regente=solicitud.id_regente,
            fecha_derivacion=solicitud.fecha_derivacion,
            estudiante_nombre=estudiante_nombre,
            apoderado_nombre=apoderado_nombre,
            motivo_nombre=motivo_nombre,
            curso_nombre=curso_nombre
        )
