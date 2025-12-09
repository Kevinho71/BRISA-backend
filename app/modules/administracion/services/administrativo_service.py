# app/modules/administracion/services/administrativo_service.py
"""Servicios para administrativos"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from fastapi import HTTPException
from typing import List, Optional
from datetime import time, datetime

from app.modules.administracion.dto.administrativo_dto import (
    AdministrativoCreateDTO, AdministrativoReadDTO, AdministrativoFullDTO, AdministrativoUpdateDTO, CargoReadDTO
)
from app.modules.administracion.repositories.administrativo_repository import (
    AdministrativoRepository
)


# ============ ADMINISTRATIVO SERVICE ============
class AdministrativoService:

    @staticmethod
    def _parse_time(time_str: Optional[str]) -> Optional[time]:
        """Convierte string HH:MM:SS a objeto time"""
        if not time_str:
            return None
        try:
            parts = time_str.split(':')
            return time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
        except:
            return None

    @staticmethod
    def _calculate_hours(horario_entrada: Optional[str], horario_salida: Optional[str]) -> int:
        """Calcula horas semanales a partir de horarios"""
        if not horario_entrada or not horario_salida:
            return 40  # Default
        
        try:
            entrada = AdministrativoService._parse_time(horario_entrada)
            salida = AdministrativoService._parse_time(horario_salida)
            
            if not entrada or not salida:
                return 40
            
            # Calcular diferencia en horas
            from datetime import datetime
            entrada_dt = datetime.combine(datetime.today(), entrada)
            salida_dt = datetime.combine(datetime.today(), salida)
            
            if salida_dt <= entrada_dt:
                return 40  # Default si salida <= entrada
            
            diff = salida_dt - entrada_dt
            horas_dia = diff.total_seconds() / 3600
            horas_semana = int(horas_dia * 5)  # 5 días laborables
            
            return horas_semana
        except:
            return 40  # Default en caso de error

    @staticmethod
    def crear_administrativo(db: Session, data: AdministrativoCreateDTO) -> AdministrativoReadDTO:
        """Crea un nuevo administrativo"""
        # Validar CI único (en todas las personas, no solo administrativos)
        if AdministrativoRepository.exists_by_ci(db, data.ci):
            raise HTTPException(
                status_code=400, 
                detail="Ya existe una persona (administrativo, profesor u otro) con este CI. El CI debe ser único."
            )
        
        # Validar correo único (si se proporciona) - verificar en personas y usuarios
        if data.correo and AdministrativoRepository.exists_by_correo(db, data.correo):
            raise HTTPException(
                status_code=400, 
                detail="Ya existe una persona o usuario con este correo electrónico. El correo debe ser único."
            )
        
        # Validar cargo
        cargo = AdministrativoRepository.get_cargo_by_id(db, data.id_cargo)
        if not cargo:
            raise HTTPException(status_code=404, detail="El cargo especificado no existe")
        
        try:
            # Separar datos de persona y administrativo
            # Solo incluir campos que no sean None para evitar problemas en la inserción
            persona_data = {
                'ci': data.ci,
                'nombres': data.nombres,
                'apellido_paterno': data.apellido_paterno,
                'tipo_persona': 'administrativo',
                'id_cargo': data.id_cargo,
                'estado_laboral': data.estado_laboral or 'activo',
                'años_experiencia': data.años_experiencia or 0,
            }
            
            # Agregar campos opcionales solo si tienen valor
            if data.apellido_materno:
                persona_data['apellido_materno'] = data.apellido_materno
            if data.direccion:
                persona_data['direccion'] = data.direccion
            if data.telefono:
                persona_data['telefono'] = data.telefono
            if data.correo:
                persona_data['correo'] = data.correo
            if data.fecha_ingreso:
                persona_data['fecha_ingreso'] = data.fecha_ingreso
            
            # Datos del administrativo
            administrativo_data = {
                'id_cargo': data.id_cargo,
            }
            
            # Agregar campos opcionales del administrativo
            if data.horario_entrada:
                parsed_entrada = AdministrativoService._parse_time(data.horario_entrada)
                if parsed_entrada:
                    administrativo_data['horario_entrada'] = parsed_entrada
            if data.horario_salida:
                parsed_salida = AdministrativoService._parse_time(data.horario_salida)
                if parsed_salida:
                    administrativo_data['horario_salida'] = parsed_salida
            if data.area_trabajo:
                administrativo_data['area_trabajo'] = data.area_trabajo
            if data.observaciones:
                administrativo_data['observaciones'] = data.observaciones
            
            # Crear administrativo en BD (hace flush pero NO commit todavía)
            administrativo = AdministrativoRepository.create(db, persona_data, administrativo_data)
            
            # Obtener cargo para el nombre_cargo (antes del commit)
            cargo = AdministrativoRepository.get_cargo_by_id(db, data.id_cargo)
            nombre_cargo = cargo.get('nombre_cargo') if cargo else None
            
            # Construir diccionario completo con datos ya disponibles ANTES del commit
            # Esto evita hacer otra query y permite validar el DTO antes del commit
            nombre_completo = f"{data.nombres} {data.apellido_paterno} {data.apellido_materno or ''}".strip()
            
            admin_dict = {
                'id_administrativo': administrativo.id_administrativo,
                'id_persona': administrativo.id_persona,
                'id_cargo': administrativo.id_cargo,
                'nombre_cargo': nombre_cargo,
                'ci': data.ci,
                'nombres': data.nombres,
                'apellido_paterno': data.apellido_paterno,
                'apellido_materno': data.apellido_materno,
                'nombre_completo': nombre_completo,
                'direccion': data.direccion,
                'telefono': data.telefono,
                'correo': data.correo,
                'estado_laboral': data.estado_laboral or 'activo',
                'años_experiencia': data.años_experiencia or 0,
                'fecha_ingreso': data.fecha_ingreso,  # Ya es string del DTO
                'horario_entrada': data.horario_entrada,  # Ya es string HH:MM:SS
                'horario_salida': data.horario_salida,  # Ya es string HH:MM:SS
                'area_trabajo': data.area_trabajo,
                'observaciones': data.observaciones,
                'horas_semana': AdministrativoService._calculate_hours(data.horario_entrada, data.horario_salida)
            }
            
            # Validar y convertir a DTO ANTES del commit
            # Si falla aquí, podemos hacer rollback y no guardar nada
            try:
                dto = AdministrativoReadDTO(**admin_dict)
            except Exception as e:
                # Si falla la conversión del DTO, hacer rollback
                db.rollback()
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error al convertir administrativo a DTO: {str(e)}", exc_info=True)
                logger.error(f"Datos del admin_dict que fallaron: {admin_dict}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error al validar datos del administrativo: {str(e)}"
                )
            
            # Si llegamos aquí, el DTO es válido - ahora hacer commit
            db.commit()
            
            # Retornar el DTO validado
            return dto
        except HTTPException:
            db.rollback()
            raise
        except IntegrityError as e:
            db.rollback()
            # Extraer información más útil del error
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            if "Duplicate entry" in error_msg or "UNIQUE constraint" in error_msg:
                if "ci" in error_msg.lower():
                    raise HTTPException(status_code=400, detail="Ya existe una persona con este CI")
                elif "correo" in error_msg.lower() or "email" in error_msg.lower():
                    raise HTTPException(status_code=400, detail="Ya existe una persona o usuario con este correo")
            raise HTTPException(status_code=400, detail=f"Error de integridad al crear el administrativo: {error_msg}")
        except Exception as e:
            db.rollback()
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error inesperado al crear administrativo: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error inesperado al crear el administrativo: {str(e)}")

    @staticmethod
    def listar_administrativos(db: Session) -> List[AdministrativoReadDTO]:
        """Lista todos los administrativos"""
        administrativos = AdministrativoRepository.get_all(db)
        return [AdministrativoReadDTO(**admin) for admin in administrativos]
    
    @staticmethod
    def listar_administrativos_completo(db: Session) -> List[AdministrativoFullDTO]:
        """Lista administrativos con información completa (incluye departamentos)"""
        administrativos = AdministrativoRepository.get_all(db)
        resultado = []
        for admin in administrativos:
            dto = AdministrativoFullDTO(**admin)
            # Para compatibilidad con frontend, usar area_trabajo como departamento
            if admin.get('area_trabajo'):
                dto.departamentos = [admin['area_trabajo']]
            else:
                dto.departamentos = []
            resultado.append(dto)
        return resultado

    @staticmethod
    def obtener_administrativo(db: Session, id_persona: int) -> Optional[AdministrativoReadDTO]:
        """Obtiene un administrativo por ID"""
        admin_dict = AdministrativoRepository.get_by_id(db, id_persona)
        if not admin_dict:
            return None
        return AdministrativoReadDTO(**admin_dict)

    @staticmethod
    def actualizar_administrativo(db: Session, id_persona: int, data: AdministrativoUpdateDTO) -> Optional[AdministrativoReadDTO]:
        """Actualiza un administrativo"""
        admin_dict = AdministrativoRepository.get_by_id(db, id_persona)
        if not admin_dict:
            raise HTTPException(status_code=404, detail="Administrativo no encontrado")
        
        # Validar CI único (si se está cambiando) - verificar en todas las personas
        if data.ci and data.ci != admin_dict['ci']:
            if AdministrativoRepository.exists_by_ci(db, data.ci, exclude_id=id_persona):
                raise HTTPException(
                    status_code=400, 
                    detail="Ya existe otra persona (administrativo, profesor u otro) con este CI. El CI debe ser único."
                )
        
        # Validar correo único (si se está cambiando) - verificar en personas y usuarios
        if data.correo and data.correo != admin_dict.get('correo'):
            if AdministrativoRepository.exists_by_correo(db, data.correo, exclude_id=id_persona):
                raise HTTPException(
                    status_code=400, 
                    detail="Ya existe otra persona o usuario con este correo electrónico. El correo debe ser único."
                )
        
        # Validar cargo si se proporciona
        if data.id_cargo:
            cargo = AdministrativoRepository.get_cargo_by_id(db, data.id_cargo)
            if not cargo:
                raise HTTPException(status_code=404, detail="El cargo especificado no existe")
        
        try:
            # Separar datos de persona y administrativo
            persona_data = {}
            administrativo_data = {}
            
            if data.ci is not None:
                persona_data['ci'] = data.ci
            if data.nombres is not None:
                persona_data['nombres'] = data.nombres
            if data.apellido_paterno is not None:
                persona_data['apellido_paterno'] = data.apellido_paterno
            if data.apellido_materno is not None:
                persona_data['apellido_materno'] = data.apellido_materno
            if data.direccion is not None:
                persona_data['direccion'] = data.direccion
            if data.telefono is not None:
                persona_data['telefono'] = data.telefono
            if data.correo is not None:
                persona_data['correo'] = data.correo
            if data.estado_laboral is not None:
                persona_data['estado_laboral'] = data.estado_laboral
            if data.años_experiencia is not None:
                persona_data['años_experiencia'] = data.años_experiencia
            if data.fecha_ingreso is not None:
                persona_data['fecha_ingreso'] = data.fecha_ingreso
            
            if data.id_cargo is not None:
                administrativo_data['id_cargo'] = data.id_cargo
                persona_data['id_cargo'] = data.id_cargo
            if data.horario_entrada is not None:
                administrativo_data['horario_entrada'] = AdministrativoService._parse_time(data.horario_entrada)
            if data.horario_salida is not None:
                administrativo_data['horario_salida'] = AdministrativoService._parse_time(data.horario_salida)
            if data.area_trabajo is not None:
                administrativo_data['area_trabajo'] = data.area_trabajo
            if data.observaciones is not None:
                administrativo_data['observaciones'] = data.observaciones
            
            admin_dict = AdministrativoRepository.update(db, id_persona, persona_data, administrativo_data)
            if not admin_dict:
                return None
            return AdministrativoReadDTO(**admin_dict)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error al actualizar el administrativo")

    @staticmethod
    def eliminar_administrativo(db: Session, id_persona: int) -> Optional[AdministrativoReadDTO]:
        """
        Elimina un administrativo después de verificar que no tenga dependencias críticas.
        
        No se puede eliminar si:
        - Tiene usuario asociado
        - Es responsable de incidentes
        - Es recepcionista o regente en solicitudes de retiro
        - Está asignado como profesor a cursos
        
        Se puede eliminar aunque tenga:
        - Derivaciones (historial)
        - Adjuntos subidos (historial)
        - Esquelas registradas (historial)
        """
        # Verificar que el administrativo existe
        admin_dict = AdministrativoRepository.get_by_id(db, id_persona)
        if not admin_dict:
            raise HTTPException(status_code=404, detail="Administrativo no encontrado")
        
        # Verificar dependencias antes de eliminar
        dependencias = AdministrativoRepository.verificar_dependencias(db, id_persona)
        
        if not dependencias['puede_eliminar']:
            # Construir mensaje de error más claro
            mensajes_bloqueantes = dependencias['mensajes']
            if mensajes_bloqueantes:
                mensaje_error = "No se puede eliminar el administrativo porque tiene las siguientes dependencias:\n\n"
                mensaje_error += "\n".join(f"• {msg}" for msg in mensajes_bloqueantes)
                mensaje_error += "\n\nPor favor, desasocie o elimine estas dependencias antes de intentar eliminar el administrativo."
            else:
                mensaje_error = "No se puede eliminar el administrativo debido a dependencias en otras tablas."
            raise HTTPException(status_code=400, detail=mensaje_error)
        
        # Proceder con la eliminación
        try:
            admin_eliminado = AdministrativoRepository.delete(db, id_persona)
            if not admin_eliminado:
                raise HTTPException(status_code=404, detail="No se pudo eliminar el administrativo")
            return AdministrativoReadDTO(**admin_eliminado)
        except HTTPException:
            # Re-lanzar HTTPException tal cual
            raise
        except IntegrityError as e:
            db.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            raise HTTPException(
                status_code=400, 
                detail=f"No se puede eliminar el administrativo debido a restricciones de integridad: {error_msg}"
            )
        except Exception as e:
            db.rollback()
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error inesperado al eliminar administrativo: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar el administrativo: {str(e)}"
            )


# ============ CARGO SERVICE ============
class CargoService:

    @staticmethod
    def listar_cargos(db: Session) -> List[CargoReadDTO]:
        """Lista todos los cargos disponibles"""
        # La tabla cargos tiene: id_cargo, nombre_cargo, descripcion, nivel_jerarquico, is_active
        query = text("SELECT id_cargo, nombre_cargo, descripcion, nivel_jerarquico, is_active FROM cargos WHERE is_active = true ORDER BY nombre_cargo")
        result = db.execute(query)
        rows = result.fetchall()
        
        cargos = []
        for row in rows:
            # Convertir is_active (boolean) a estado (string) para el DTO
            # row[0]=id_cargo, row[1]=nombre_cargo, row[2]=descripcion, row[3]=nivel_jerarquico, row[4]=is_active
            is_active = bool(row[4]) if len(row) > 4 else True
            estado_str = 'activo' if is_active else 'inactivo'
            cargo_dict = {
                'id_cargo': int(row[0]),
                'nombre_cargo': str(row[1]),
                'descripcion': str(row[2]) if len(row) > 2 and row[2] is not None else None,
                'estado': estado_str,
                'fecha_creacion': None  # La tabla no tiene fecha_creacion
            }
            cargos.append(CargoReadDTO(**cargo_dict))
        
        return cargos

    @staticmethod
    def obtener_cargo(db: Session, id_cargo: int) -> Optional[CargoReadDTO]:
        """Obtiene un cargo por ID"""
        query = text("SELECT id_cargo, nombre_cargo, descripcion, nivel_jerarquico, is_active FROM cargos WHERE id_cargo = :id_cargo")
        result = db.execute(query, {"id_cargo": id_cargo})
        row = result.fetchone()
        if not row:
            return None
        
        # Convertir is_active (boolean) a estado (string) para el DTO
        # row[0]=id_cargo, row[1]=nombre_cargo, row[2]=descripcion, row[3]=nivel_jerarquico, row[4]=is_active
        is_active = bool(row[4]) if len(row) > 4 else True
        estado_str = 'activo' if is_active else 'inactivo'
        cargo_dict = {
            'id_cargo': int(row[0]),
            'nombre_cargo': str(row[1]),
            'descripcion': str(row[2]) if len(row) > 2 and row[2] is not None else None,
            'estado': estado_str,
            'fecha_creacion': None  # La tabla no tiene fecha_creacion
        }
        return CargoReadDTO(**cargo_dict)

