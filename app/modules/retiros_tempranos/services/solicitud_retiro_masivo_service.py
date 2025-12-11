from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.retiros_tempranos.repositories.solicitud_retiro_masivo_repository import SolicitudRetiroMasivoRepository
from app.modules.retiros_tempranos.repositories.detalle_solicitud_retiro_masivo_repository import DetalleSolicitudRetiroMasivoRepository
from app.modules.retiros_tempranos.repositories.motivo_retiro_repository import MotivoRetiroRepository
from app.modules.retiros_tempranos.repositories.autorizacion_retiro_repository import AutorizacionRetiroRepository
from app.modules.retiros_tempranos.repositories.estudiante_repository import EstudianteRepository

from app.modules.retiros_tempranos.models.SolicitudRetiroMasivo import SolicitudRetiroMasivo, EstadoSolicitudMasivaEnum
from app.modules.retiros_tempranos.models.DetalleSolicitudRetiroMasivo import DetalleSolicitudRetiroMasivo
from app.modules.retiros_tempranos.models.AutorizacionesRetiro import AutorizacionRetiro, DecisionEnum

from app.modules.retiros_tempranos.dto.solicitud_retiro_masivo_dto import (
    SolicitudRetiroMasivoCreateDTO,
    SolicitudRetiroMasivoUpdateDTO,
    SolicitudRetiroMasivoResponseDTO,
    SolicitudRetiroMasivoDetalladaResponseDTO,
    DetalleSolicitudMasivoResponseDTO,
    RecibirSolicitudMasivaDTO,
    DerivarSolicitudMasivaDTO,
    AprobarRechazarSolicitudMasivaDTO,
    CancelarSolicitudMasivaDTO
)

from app.modules.usuarios.models import Usuario


class SolicitudRetiroMasivoService:
    """Servicio para la gestión de solicitudes de retiro masivo"""

    def __init__(self, db: Session):
        self.db = db
        self.solicitud_repo = SolicitudRetiroMasivoRepository(db)
        self.detalle_repo = DetalleSolicitudRetiroMasivoRepository(db)
        self.motivo_repo = MotivoRetiroRepository(db)
        self.autorizacion_repo = AutorizacionRetiroRepository(db)
        self.estudiante_repo = EstudianteRepository(db)

    def crear_solicitud(
        self, 
        solicitud_dto: SolicitudRetiroMasivoCreateDTO, 
        id_solicitante: int
    ) -> SolicitudRetiroMasivoDetalladaResponseDTO:
        """Crea una solicitud de retiro masivo con lista de estudiantes"""
        
        # Validar motivo
        motivo = self.motivo_repo.get_by_id(solicitud_dto.id_motivo)
        if not motivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Motivo de retiro no encontrado"
            )

        # Validar que haya al menos un estudiante
        if not solicitud_dto.estudiantes or len(solicitud_dto.estudiantes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe incluir al menos un estudiante en la solicitud"
            )

        # Validar que todos los estudiantes existen
        for detalle_dto in solicitud_dto.estudiantes:
            estudiante = self.estudiante_repo.get_by_id(detalle_dto.id_estudiante)
            if not estudiante:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Estudiante con ID {detalle_dto.id_estudiante} no encontrado"
                )

        # Crear solicitud masiva
        nueva_solicitud = SolicitudRetiroMasivo(
            id_solicitante=id_solicitante,
            id_motivo=solicitud_dto.id_motivo,
            fecha_hora_salida=solicitud_dto.fecha_hora_salida,
            fecha_hora_retorno=solicitud_dto.fecha_hora_retorno,
            foto_evidencia=solicitud_dto.foto_evidencia,
            observacion=solicitud_dto.observacion,
            estado=EstadoSolicitudMasivaEnum.pendiente.value
        )

        solicitud_creada = self.solicitud_repo.create(nueva_solicitud)

        # Crear detalles (lista de estudiantes)
        detalles = []
        for detalle_dto in solicitud_dto.estudiantes:
            detalle = DetalleSolicitudRetiroMasivo(
                id_solicitud_masiva=solicitud_creada.id_solicitud_masiva,
                id_estudiante=detalle_dto.id_estudiante,
                observacion_individual=detalle_dto.observacion_individual
            )
            detalles.append(detalle)

        detalles_creados = self.detalle_repo.create_multiple(detalles)

        return self._convertir_a_dto_detallado(solicitud_creada, detalles_creados)

    def obtener_solicitud(self, id_solicitud: int) -> SolicitudRetiroMasivoDetalladaResponseDTO:
        """Obtiene una solicitud masiva con sus detalles"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud de retiro masivo no encontrada"
            )

        detalles = self.detalle_repo.get_by_solicitud(id_solicitud)
        return self._convertir_a_dto_detallado(solicitud, detalles)

    def listar_solicitudes(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroMasivoResponseDTO]:
        """Lista todas las solicitudes masivas"""
        solicitudes = self.solicitud_repo.get_all(skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_por_solicitante(
        self, 
        id_solicitante: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroMasivoResponseDTO]:
        """Lista solicitudes de un solicitante específico"""
        solicitudes = self.solicitud_repo.get_by_solicitante(id_solicitante, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_pendientes(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroMasivoResponseDTO]:
        """Lista solicitudes pendientes de recepción"""
        solicitudes = self.solicitud_repo.get_pendientes(skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_recibidas(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroMasivoResponseDTO]:
        """Lista solicitudes recibidas (pendientes de derivar)"""
        solicitudes = self.solicitud_repo.get_recibidas(skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_derivadas_a_regente(
        self, 
        id_regente: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SolicitudRetiroMasivoResponseDTO]:
        """Lista solicitudes derivadas a un regente"""
        solicitudes = self.solicitud_repo.get_derivadas(id_regente, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def recibir_solicitud(
        self, 
        id_solicitud: int, 
        recibir_dto: RecibirSolicitudMasivaDTO, 
        id_recepcionista: int
    ) -> SolicitudRetiroMasivoResponseDTO:
        """Recepcionista marca solicitud como recibida"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.estado != EstadoSolicitudMasivaEnum.pendiente.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden recibir solicitudes en estado pendiente"
            )

        solicitud.estado = EstadoSolicitudMasivaEnum.recibida.value
        solicitud.id_recepcionista = id_recepcionista
        solicitud.fecha_recepcion = recibir_dto.fecha_hora_recepcion or datetime.now()

        solicitud_actualizada = self.solicitud_repo.update(solicitud)
        return self._convertir_a_dto(solicitud_actualizada)

    def derivar_solicitud(
        self, 
        id_solicitud: int, 
        derivar_dto: DerivarSolicitudMasivaDTO
    ) -> SolicitudRetiroMasivoResponseDTO:
        """Recepcionista deriva solicitud al regente"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.estado != EstadoSolicitudMasivaEnum.recibida.value:
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

        solicitud.estado = EstadoSolicitudMasivaEnum.derivada.value
        solicitud.id_regente = derivar_dto.id_regente
        solicitud.fecha_derivacion = datetime.now()

        solicitud_actualizada = self.solicitud_repo.update(solicitud)
        return self._convertir_a_dto(solicitud_actualizada)

    def aprobar_rechazar_solicitud(
        self, 
        id_solicitud: int, 
        decision_dto: AprobarRechazarSolicitudMasivaDTO,
        id_regente: int
    ) -> SolicitudRetiroMasivoResponseDTO:
        """Regente aprueba o rechaza una solicitud masiva"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.estado != EstadoSolicitudMasivaEnum.derivada.value:
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
            id_solicitud_masiva=id_solicitud,
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
        cancelar_dto: CancelarSolicitudMasivaDTO,
        id_solicitante: int
    ) -> SolicitudRetiroMasivoResponseDTO:
        """Solicitante cancela su propia solicitud"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.id_solicitante != id_solicitante:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el solicitante puede cancelar su solicitud"
            )

        if solicitud.estado in [EstadoSolicitudMasivaEnum.aprobada.value, EstadoSolicitudMasivaEnum.rechazada.value]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cancelar una solicitud ya aprobada o rechazada"
            )

        solicitud.estado = EstadoSolicitudMasivaEnum.cancelada.value
        solicitud.observacion = f"{solicitud.observacion or ''}\n[CANCELADA: {cancelar_dto.motivo_cancelacion}]"

        solicitud_actualizada = self.solicitud_repo.update(solicitud)
        return self._convertir_a_dto(solicitud_actualizada)

    def eliminar_solicitud(self, id_solicitud: int, id_solicitante: int) -> bool:
        """Elimina una solicitud masiva (solo si está en pendiente)"""
        solicitud = self.solicitud_repo.get_by_id(id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud no encontrada"
            )

        if solicitud.id_solicitante != id_solicitante:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el solicitante puede eliminar su solicitud"
            )

        if solicitud.estado != EstadoSolicitudMasivaEnum.pendiente.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar solicitudes pendientes"
            )

        return self.solicitud_repo.delete(id_solicitud)

    def _convertir_a_dto(self, solicitud: SolicitudRetiroMasivo) -> SolicitudRetiroMasivoResponseDTO:
        """Convierte modelo a DTO (sin detalles)"""
        solicitante_nombre = None
        if solicitud.solicitante:
            solicitante_nombre = f"{solicitud.solicitante.nombre} {solicitud.solicitante.apellido_paterno}"

        motivo_nombre = solicitud.motivo.nombre if solicitud.motivo else None
        
        # Contar estudiantes
        cantidad_estudiantes = len(self.detalle_repo.get_by_solicitud(solicitud.id_solicitud_masiva))

        return SolicitudRetiroMasivoResponseDTO(
            id_solicitud=solicitud.id_solicitud_masiva,
            id_solicitante=solicitud.id_solicitante,
            id_motivo=solicitud.id_motivo,
            id_autorizacion=solicitud.id_autorizacion,
            fecha_hora_salida=solicitud.fecha_hora_salida,
            fecha_hora_retorno=solicitud.fecha_hora_retorno,
            foto_evidencia=solicitud.foto_evidencia,
            observacion=solicitud.observacion,
            fecha_hora_solicitud=solicitud.fecha_hora_solicitud,
            estado=solicitud.estado,
            id_recepcionista=solicitud.id_recepcionista,
            fecha_recepcion=solicitud.fecha_recepcion,
            id_regente=solicitud.id_regente,
            fecha_derivacion=solicitud.fecha_derivacion,
            solicitante_nombre=solicitante_nombre,
            motivo_nombre=motivo_nombre,
            cantidad_estudiantes=cantidad_estudiantes
        )

    def _convertir_a_dto_detallado(
        self, 
        solicitud: SolicitudRetiroMasivo, 
        detalles: List[DetalleSolicitudRetiroMasivo]
    ) -> SolicitudRetiroMasivoDetalladaResponseDTO:
        """Convierte modelo a DTO detallado (con lista de estudiantes)"""
        dto_base = self._convertir_a_dto(solicitud)
        
        detalles_dto = []
        for detalle in detalles:
            estudiante_nombre = None
            estudiante_ci = None
            curso_nombre = None
            
            if detalle.estudiante:
                estudiante_nombre = f"{detalle.estudiante.nombre} {detalle.estudiante.apellido_paterno} {detalle.estudiante.apellido_materno or ''}"
                estudiante_ci = detalle.estudiante.ci
                if detalle.estudiante.curso:
                    curso_nombre = detalle.estudiante.curso.nombre

            detalles_dto.append(DetalleSolicitudMasivoResponseDTO(
                id_detalle=detalle.id_detalle,
                id_solicitud_masiva=detalle.id_solicitud_masiva,
                id_estudiante=detalle.id_estudiante,
                observacion_individual=detalle.observacion_individual,
                estudiante_nombre=estudiante_nombre,
                estudiante_ci=estudiante_ci,
                curso_nombre=curso_nombre
            ))

        return SolicitudRetiroMasivoDetalladaResponseDTO(
            **dto_base.model_dump(),
            detalles=detalles_dto
        )
