from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.retiros_tempranos.repositories.registro_salida_repository import RegistroSalidaRepository
from app.modules.retiros_tempranos.repositories.solicitud_retiro_repository import SolicitudRetiroRepository
from app.modules.retiros_tempranos.repositories.solicitud_retiro_masivo_repository import SolicitudRetiroMasivoRepository
from app.modules.retiros_tempranos.repositories.detalle_solicitud_retiro_masivo_repository import DetalleSolicitudRetiroMasivoRepository

from app.modules.retiros_tempranos.models.RegistroSalida import RegistroSalida, TipoRegistroEnum
from app.modules.retiros_tempranos.models.SolicitudRetiro import EstadoSolicitudEnum
from app.modules.retiros_tempranos.models.SolicitudRetiroMasivo import EstadoSolicitudMasivaEnum

from app.modules.retiros_tempranos.dto.registro_salida_dto import (
    RegistroSalidaCreateDTO,
    RegistroSalidaMasivoCreateDTO,
    RegistroSalidaUpdateDTO,
    RegistroSalidaResponseDTO
)


class RegistroSalidaService:
    """Servicio para la gestión de registros de salida"""

    def __init__(self, db: Session):
        self.db = db
        self.registro_repo = RegistroSalidaRepository(db)
        self.solicitud_repo = SolicitudRetiroRepository(db)
        self.solicitud_masiva_repo = SolicitudRetiroMasivoRepository(db)
        self.detalle_repo = DetalleSolicitudRetiroMasivoRepository(db)

    def crear_registro_individual(
        self, 
        registro_dto: RegistroSalidaCreateDTO
    ) -> RegistroSalidaResponseDTO:
        """Crea un registro de salida individual a partir de solicitud aprobada"""
        
        solicitud = self.solicitud_repo.get_by_id(registro_dto.id_solicitud)
        if not solicitud:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud de retiro no encontrada"
            )

        if solicitud.estado != EstadoSolicitudEnum.aprobada.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden crear registros de solicitudes aprobadas"
            )

        # Verificar que no existe ya un registro
        registro_existente = self.db.query(RegistroSalida).filter(
            RegistroSalida.id_solicitud == registro_dto.id_solicitud
        ).first()
        
        if registro_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un registro para esta solicitud"
            )

        nuevo_registro = RegistroSalida(
            id_solicitud=registro_dto.id_solicitud,
            id_estudiante=solicitud.id_estudiante,
            tipo_registro=TipoRegistroEnum.individual.value,
            fecha_hora_salida_real=registro_dto.fecha_hora_salida_real or datetime.now()
        )

        registro_creado = self.registro_repo.create(nuevo_registro)
        
        # Cambiar estado de la solicitud a finalizado
        solicitud.estado = EstadoSolicitudEnum.finalizado.value
        self.db.commit()
        
        return self._convertir_a_dto(registro_creado)

    def crear_registros_masivos(
        self, 
        registro_dto: RegistroSalidaMasivoCreateDTO
    ) -> List[RegistroSalidaResponseDTO]:
        """Crea registros de salida para todos los estudiantes de una solicitud masiva aprobada"""
        
        solicitud_masiva = self.solicitud_masiva_repo.get_by_id(registro_dto.id_solicitud_masiva)
        if not solicitud_masiva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitud masiva no encontrada"
            )

        if solicitud_masiva.estado != EstadoSolicitudMasivaEnum.aprobada.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden crear registros de solicitudes masivas aprobadas"
            )

        # Obtener lista de estudiantes
        detalles = self.detalle_repo.get_by_solicitud(registro_dto.id_solicitud_masiva)
        if not detalles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La solicitud masiva no tiene estudiantes asociados"
            )

        # Crear un registro para cada estudiante
        registros_creados = []
        fecha_salida = registro_dto.fecha_hora_salida_real or datetime.now()

        for detalle in detalles:
            # Verificar que no existe ya registro
            registro_existente = self.db.query(RegistroSalida).filter(
                RegistroSalida.id_solicitud_masiva == registro_dto.id_solicitud_masiva,
                RegistroSalida.id_estudiante == detalle.id_estudiante
            ).first()
            
            if not registro_existente:
                nuevo_registro = RegistroSalida(
                    id_solicitud_masiva=registro_dto.id_solicitud_masiva,
                    id_estudiante=detalle.id_estudiante,
                    tipo_registro=TipoRegistroEnum.masivo.value,
                    fecha_hora_salida_real=fecha_salida
                )
                registro_creado = self.registro_repo.create(nuevo_registro)
                registros_creados.append(self._convertir_a_dto(registro_creado))

        if not registros_creados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existen registros para todos los estudiantes de esta solicitud"
            )

        # Cambiar estado de la solicitud masiva a finalizado
        solicitud_masiva.estado = EstadoSolicitudMasivaEnum.finalizado.value
        self.db.commit()

        return registros_creados

    def obtener_registro(self, id_registro: int) -> RegistroSalidaResponseDTO:
        """Obtiene un registro por ID"""
        registro = self.registro_repo.get_by_id(id_registro)
        if not registro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de salida no encontrado"
            )
        return self._convertir_a_dto(registro)

    def listar_registros(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RegistroSalidaResponseDTO]:
        """Lista todos los registros"""
        registros = self.registro_repo.get_all(skip, limit)
        return [self._convertir_a_dto(reg) for reg in registros]

    def listar_por_estudiante(
        self, 
        id_estudiante: int
    ) -> List[RegistroSalidaResponseDTO]:
        """Lista registros de un estudiante"""
        registros = self.registro_repo.get_by_estudiante(id_estudiante)
        return [self._convertir_a_dto(reg) for reg in registros]

    def _convertir_a_dto(self, registro: RegistroSalida) -> RegistroSalidaResponseDTO:
        """Convierte modelo a DTO"""
        estudiante_nombre = None
        estudiante_ci = None

        if registro.estudiante:
            estudiante_nombre = f"{registro.estudiante.nombres} {registro.estudiante.apellido_paterno} {registro.estudiante.apellido_materno or ''}"
            estudiante_ci = registro.estudiante.ci

        return RegistroSalidaResponseDTO(
            id_registro=registro.id_registro,
            id_solicitud=registro.id_solicitud,
            id_solicitud_masiva=registro.id_solicitud_masiva,
            id_estudiante=registro.id_estudiante,
            tipo_registro=registro.tipo_registro,
            fecha_hora_salida_real=registro.fecha_hora_salida_real,
            fecha_hora_retorno_real=registro.fecha_hora_retorno_real,
            estudiante_nombre=estudiante_nombre,
            estudiante_ci=estudiante_ci
        )