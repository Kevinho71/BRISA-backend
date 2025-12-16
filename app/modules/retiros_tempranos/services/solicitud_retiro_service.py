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
from app.modules.retiros_tempranos.models.EstudianteApoderado import EstudianteApoderado

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
        relacion = self.db.query(
            self.db.query(EstudianteApoderado).filter(
                EstudianteApoderado.id_estudiante == solicitud_dto.id_estudiante,
                EstudianteApoderado.id_apoderado == id_apoderado
            ).exists()
        ).scalar()
        
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
            fecha_creacion=datetime.now(),
            estado=EstadoSolicitudEnum.recibida.value
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
        """Lista solicitudes recién creadas (recibidas)"""
        solicitudes = self.solicitud_repo.get_by_estado(EstadoSolicitudEnum.recibida.value, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def listar_derivadas(self, skip: int = 0, limit: int = 100) -> List[SolicitudRetiroResponseDTO]:
        """Lista todas las solicitudes derivadas al regente"""
        solicitudes = self.solicitud_repo.get_by_estado(EstadoSolicitudEnum.derivada.value, skip, limit)
        return [self._convertir_a_dto(sol) for sol in solicitudes]

    def derivar_solicitud(
        self, 
        id_solicitud: int, 
        derivar_dto: DerivarSolicitudDTO
    ) -> SolicitudRetiroResponseDTO:
        """Recepcionista deriva solicitud al regente (único)"""
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

        # Cambiar estado a derivada (el regente se asignará cuando tome acción)
        solicitud_actualizada = self.solicitud_repo.update(
            id_solicitud,
            {
                "estado": EstadoSolicitudEnum.derivada.value,
                "fecha_derivacion": datetime.now()
            }
        )
        return self._convertir_a_dto(solicitud_actualizada)

    def aprobar_rechazar_solicitud(
        self, 
        id_solicitud: int, 
        decision_dto: AprobarRechazarSolicitudDTO,
        id_usuario_aprobador: int
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

        # Crear autorización (sin id_solicitud, se vincula desde solicitud)
        nueva_autorizacion = AutorizacionRetiro(
            id_usuario_aprobador=id_usuario_aprobador,
            decision=decision_dto.decision,
            motivo_decision=decision_dto.motivo_rechazo,
            fecha_decision=datetime.now()
        )
        autorizacion_creada = self.autorizacion_repo.create(nueva_autorizacion)

        # Actualizar solicitud: cambiar estado y vincular autorización
        solicitud_actualizada = self.solicitud_repo.update(
            id_solicitud,
            {
                "estado": decision_dto.decision,
                "id_autorizacion": autorizacion_creada.id_autorizacion
            }
        )

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

        solicitud_actualizada = self.solicitud_repo.update(
            id_solicitud, 
            {
                "estado": EstadoSolicitudEnum.cancelada.value,
                "observacion": solicitud.observacion
            }
        )
        return self._convertir_a_dto(solicitud_actualizada)

    def eliminar_solicitud(self, id_solicitud: int, id_apoderado: int) -> bool:
        """Elimina una solicitud (solo si está en estado recibida)"""
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

        if solicitud.estado != EstadoSolicitudEnum.recibida.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar solicitudes en estado recibida"
            )

        return self.solicitud_repo.delete(id_solicitud)

    def _convertir_a_dto(self, solicitud: SolicitudRetiro) -> SolicitudRetiroResponseDTO:
        """Convierte modelo a DTO"""
        estudiante_nombre = None
        apoderado_nombre = None
        motivo_nombre = None
        curso_nombre = None

        if solicitud.estudiante:
            estudiante_nombre = f"{solicitud.estudiante.nombres} {solicitud.estudiante.apellido_paterno} {solicitud.estudiante.apellido_materno or ''}"
            # Estudiante puede tener múltiples cursos, tomamos el primero si existe
            if solicitud.estudiante.cursos and len(solicitud.estudiante.cursos) > 0:
                curso_nombre = solicitud.estudiante.cursos[0].nombre_curso

        if solicitud.apoderado:
            apoderado_nombre = f"{solicitud.apoderado.nombres} {solicitud.apoderado.apellidos}"

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
            fecha_creacion=solicitud.fecha_creacion,
            estado=solicitud.estado,
            fecha_derivacion=solicitud.fecha_derivacion,
            estudiante_nombre=estudiante_nombre,
            apoderado_nombre=apoderado_nombre,
            motivo_nombre=motivo_nombre,
            curso_nombre=curso_nombre
        )
