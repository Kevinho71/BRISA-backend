# app/modules/administracion/repositories/administrativo_repository.py
"""Repositorio para acceso a datos de administrativos"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app.modules.administracion.models.administrativo_models import Administrativo
from typing import Optional, List


class AdministrativoRepository:

    @staticmethod
    def create(db: Session, persona_data: dict, administrativo_data: dict) -> Administrativo:
        """Crea un nuevo administrativo (persona + administrativo)"""
        try:
            # Filtrar campos None para evitar problemas en la inserción
            persona_data_clean = {k: v for k, v in persona_data.items() if v is not None}
            
            # Primero crear la persona usando SQL directo
            persona_cols = ', '.join(persona_data_clean.keys())
            persona_vals = ', '.join([f':{k}' for k in persona_data_clean.keys()])
            query_persona = text(f"""
                INSERT INTO personas ({persona_cols}) 
                VALUES ({persona_vals})
            """)
            result = db.execute(query_persona, persona_data_clean)
            db.flush()
            
            # Obtener el id_persona generado
            id_persona = result.lastrowid
            
            # Luego crear el registro administrativo
            administrativo_data['id_persona'] = id_persona
            # Filtrar campos None del administrativo_data también
            administrativo_data_clean = {k: v for k, v in administrativo_data.items() if v is not None}
            administrativo = Administrativo(**administrativo_data_clean)
            db.add(administrativo)
            # NO hacer commit aquí - se hará en el service después de validar el DTO
            db.flush()  # Solo flush para obtener el ID pero sin commit
            db.refresh(administrativo)
            return administrativo
        except Exception as e:
            # Si hay error, hacer rollback antes de relanzar
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session) -> List[dict]:
        """Obtiene todos los administrativos con sus datos completos"""
        # Usar vista o join para obtener datos completos
        query = text("""
            SELECT 
                a.id_administrativo,
                a.id_persona,
                a.id_cargo,
                c.nombre_cargo,
                p.ci,
                p.nombres,
                p.apellido_paterno,
                p.apellido_materno,
                CONCAT(p.nombres, ' ', p.apellido_paterno, ' ', COALESCE(p.apellido_materno, '')) as nombre_completo,
                p.direccion,
                p.telefono,
                p.correo,
                p.estado_laboral,
                p.años_experiencia,
                p.fecha_ingreso,
                TIME_FORMAT(a.horario_entrada, '%H:%i:%s') as horario_entrada,
                TIME_FORMAT(a.horario_salida, '%H:%i:%s') as horario_salida,
                a.area_trabajo,
                a.observaciones,
                TIMESTAMPDIFF(HOUR, a.horario_entrada, a.horario_salida) * 5 as horas_semana,
                r.nombre as rol_usuario
            FROM administrativos a
            INNER JOIN personas p ON a.id_persona = p.id_persona
            LEFT JOIN cargos c ON a.id_cargo = c.id_cargo
            LEFT JOIN usuarios u ON p.id_persona = u.id_persona AND u.is_active = true
            LEFT JOIN usuario_roles ur ON u.id_usuario = ur.id_usuario AND ur.estado = 'activo'
            LEFT JOIN roles r ON ur.id_rol = r.id_rol AND r.is_active = true
            WHERE p.tipo_persona = 'administrativo'
            ORDER BY p.apellido_paterno, p.apellido_materno, p.nombres
        """)
        result = db.execute(query)
        rows = result.fetchall()
        
        # Convertir a lista de diccionarios
        administrativos = []
        for row in rows:
            admin_dict = {
                'id_administrativo': row[0],
                'id_persona': row[1],
                'id_cargo': row[2],
                'nombre_cargo': row[3],
                'ci': row[4],
                'nombres': row[5],
                'apellido_paterno': row[6],
                'apellido_materno': row[7],
                'nombre_completo': row[8],
                'direccion': row[9],
                'telefono': row[10],
                'correo': row[11],
                'estado_laboral': row[12],
                'años_experiencia': row[13],
                'fecha_ingreso': str(row[14]) if row[14] else None,
                'horario_entrada': row[15],
                'horario_salida': row[16],
                'area_trabajo': row[17],
                'observaciones': row[18],
                'horas_semana': int(row[19]) if row[19] is not None else 40,
                'rol_usuario': row[20] if row[20] else None
            }
            administrativos.append(admin_dict)
        
        return administrativos

    @staticmethod
    def get_by_id(db: Session, id_persona: int) -> Optional[dict]:
        """Obtiene un administrativo por ID de persona"""
        query = text("""
            SELECT 
                a.id_administrativo,
                a.id_persona,
                a.id_cargo,
                c.nombre_cargo,
                p.ci,
                p.nombres,
                p.apellido_paterno,
                p.apellido_materno,
                CONCAT(p.nombres, ' ', p.apellido_paterno, ' ', COALESCE(p.apellido_materno, '')) as nombre_completo,
                p.direccion,
                p.telefono,
                p.correo,
                p.estado_laboral,
                p.años_experiencia,
                p.fecha_ingreso,
                TIME_FORMAT(a.horario_entrada, '%H:%i:%s') as horario_entrada,
                TIME_FORMAT(a.horario_salida, '%H:%i:%s') as horario_salida,
                a.area_trabajo,
                a.observaciones,
                TIMESTAMPDIFF(HOUR, a.horario_entrada, a.horario_salida) * 5 as horas_semana,
                r.nombre as rol_usuario
            FROM administrativos a
            INNER JOIN personas p ON a.id_persona = p.id_persona
            LEFT JOIN cargos c ON a.id_cargo = c.id_cargo
            LEFT JOIN usuarios u ON p.id_persona = u.id_persona AND u.is_active = true
            LEFT JOIN usuario_roles ur ON u.id_usuario = ur.id_usuario AND ur.estado = 'activo'
            LEFT JOIN roles r ON ur.id_rol = r.id_rol AND r.is_active = true
            WHERE p.id_persona = :id_persona AND p.tipo_persona = 'administrativo'
            LIMIT 1
        """)
        result = db.execute(query, {"id_persona": id_persona})
        row = result.fetchone()
        
        if not row:
            return None
        
        return {
            'id_administrativo': row[0],
            'id_persona': row[1],
            'id_cargo': row[2],
            'nombre_cargo': row[3],
            'ci': row[4],
            'nombres': row[5],
            'apellido_paterno': row[6],
            'apellido_materno': row[7],
            'nombre_completo': row[8],
            'direccion': row[9],
            'telefono': row[10],
            'correo': row[11],
            'estado_laboral': row[12],
            'años_experiencia': row[13],
            'fecha_ingreso': str(row[14]) if row[14] else None,  # Convertir date a string
            'horario_entrada': row[15],
            'horario_salida': row[16],
            'area_trabajo': row[17],
            'observaciones': row[18],
            'horas_semana': int(row[19]) if row[19] is not None else 40,
            'rol_usuario': row[20] if row[20] else None
        }

    @staticmethod
    def get_persona_by_id(db: Session, id_persona: int) -> Optional[dict]:
        """Obtiene una persona administrativa por ID"""
        query = text("""
            SELECT * FROM personas 
            WHERE id_persona = :id_persona AND tipo_persona = 'administrativo'
        """)
        result = db.execute(query, {"id_persona": id_persona})
        row = result.fetchone()
        if not row:
            return None
        return dict(row._mapping)

    @staticmethod
    def get_administrativo_by_persona_id(db: Session, id_persona: int) -> Optional[Administrativo]:
        """Obtiene el registro administrativo por ID de persona"""
        return (
            db.query(Administrativo)
            .filter(Administrativo.id_persona == id_persona)
            .first()
        )

    @staticmethod
    def update(db: Session, id_persona: int, persona_data: dict, administrativo_data: dict) -> Optional[dict]:
        """Actualiza un administrativo"""
        persona = AdministrativoRepository.get_persona_by_id(db, id_persona)
        if not persona:
            return None
        
        administrativo = AdministrativoRepository.get_administrativo_by_persona_id(db, id_persona)
        if not administrativo:
            return None
        
        # Actualizar persona usando SQL
        if persona_data:
            set_clauses = ', '.join([f"{k} = :{k}" for k in persona_data.keys()])
            query_persona = text(f"""
                UPDATE personas 
                SET {set_clauses}
                WHERE id_persona = :id_persona
            """)
            persona_data['id_persona'] = id_persona
            db.execute(query_persona, persona_data)
        
        # Actualizar administrativo
        for key, value in administrativo_data.items():
            if value is not None:
                setattr(administrativo, key, value)
        
        db.commit()
        db.refresh(administrativo)
        
        return AdministrativoRepository.get_by_id(db, id_persona)

    @staticmethod
    def delete(db: Session, id_persona: int) -> Optional[dict]:
        """Elimina un administrativo (elimina persona y administrativo en cascada)"""
        administrativo_data = AdministrativoRepository.get_by_id(db, id_persona)
        if not administrativo_data:
            return None
        
        # Eliminar persona (el administrativo se elimina en cascada)
        query = text("DELETE FROM personas WHERE id_persona = :id_persona")
        db.execute(query, {"id_persona": id_persona})
        db.commit()
        
        return administrativo_data

    @staticmethod
    def exists_by_ci(db: Session, ci: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una persona (de cualquier tipo) con el CI dado.
        Esto previene duplicados entre administrativos, profesores, etc.
        """
        query = text("""
            SELECT COUNT(*) as count FROM personas 
            WHERE ci = :ci
        """)
        params = {"ci": ci}
        if exclude_id:
            query = text("""
                SELECT COUNT(*) as count FROM personas 
                WHERE ci = :ci AND id_persona != :exclude_id
            """)
            params["exclude_id"] = exclude_id
        result = db.execute(query, params)
        row = result.fetchone()
        return row[0] > 0 if row else False

    @staticmethod
    def exists_by_correo(db: Session, correo: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una persona (de cualquier tipo) o usuario con el correo dado.
        Esto previene duplicados entre personas y usuarios.
        """
        # Verificar en personas
        query_persona = text("""
            SELECT COUNT(*) as count FROM personas 
            WHERE correo = :correo AND correo IS NOT NULL AND correo != ''
        """)
        params = {"correo": correo}
        if exclude_id:
            query_persona = text("""
                SELECT COUNT(*) as count FROM personas 
                WHERE correo = :correo AND correo IS NOT NULL AND correo != '' 
                AND id_persona != :exclude_id
            """)
            params["exclude_id"] = exclude_id
        result = db.execute(query_persona, params)
        count_persona = result.fetchone()[0]
        
        # Verificar en usuarios (el correo debe ser único en usuarios)
        query_usuario = text("""
            SELECT COUNT(*) as count FROM usuarios 
            WHERE correo = :correo
        """)
        result = db.execute(query_usuario, params)
        count_usuario = result.fetchone()[0]
        
        return (count_persona > 0) or (count_usuario > 0)

    @staticmethod
    def get_cargo_by_id(db: Session, id_cargo: int) -> Optional[dict]:
        """Obtiene un cargo por ID"""
        query = text("SELECT * FROM cargos WHERE id_cargo = :id_cargo")
        result = db.execute(query, {"id_cargo": id_cargo})
        row = result.fetchone()
        if not row:
            return None
        return dict(row._mapping)

    @staticmethod
    def verificar_dependencias(db: Session, id_persona: int) -> dict:
        """
        Verifica si la persona tiene dependencias que impidan su eliminación.
        Retorna un diccionario con información sobre las dependencias encontradas.
        """
        dependencias = {
            'tiene_usuario': False,
            'tiene_incidentes': False,
            'tiene_solicitudes_recepcionista': False,
            'tiene_solicitudes_regente': False,
            'tiene_derivaciones_deriva': False,
            'tiene_derivaciones_recibe': False,
            'tiene_adjuntos': False,
            'tiene_esquelas': False,
            'tiene_profesor_cursos': False,
            'mensajes': []
        }
        
        # Verificar si tiene usuario asociado
        query_usuario = text("SELECT COUNT(*) FROM usuarios WHERE id_persona = :id_persona")
        result = db.execute(query_usuario, {"id_persona": id_persona})
        count_usuario = result.fetchone()[0]
        if count_usuario > 0:
            dependencias['tiene_usuario'] = True
            dependencias['mensajes'].append("La persona tiene un usuario asociado. Debe eliminar o desasociar el usuario primero.")
        
        # Verificar si es responsable de incidentes
        query_incidentes = text("SELECT COUNT(*) FROM incidentes WHERE id_responsable = :id_persona")
        result = db.execute(query_incidentes, {"id_persona": id_persona})
        count_incidentes = result.fetchone()[0]
        if count_incidentes > 0:
            dependencias['tiene_incidentes'] = True
            dependencias['mensajes'].append(f"La persona es responsable de {count_incidentes} incidente(s). Debe reasignar los incidentes primero.")
        
        # Verificar si es recepcionista en solicitudes de retiro (vía usuario)
        if dependencias['tiene_usuario']:
            query_recepcionista = text("""
                SELECT COUNT(*) FROM solicitudes_retiro sr
                INNER JOIN usuarios u ON sr.id_recepcionista = u.id_usuario
                WHERE u.id_persona = :id_persona
            """)
            result = db.execute(query_recepcionista, {"id_persona": id_persona})
            count_recepcionista = result.fetchone()[0]
            if count_recepcionista > 0:
                dependencias['tiene_solicitudes_recepcionista'] = True
                dependencias['mensajes'].append(f"La persona es recepcionista en {count_recepcionista} solicitud(es) de retiro. Debe reasignar las solicitudes primero.")
            
            # Verificar si es regente en solicitudes de retiro
            query_regente = text("""
                SELECT COUNT(*) FROM solicitudes_retiro sr
                INNER JOIN usuarios u ON sr.id_regente = u.id_usuario
                WHERE u.id_persona = :id_persona
            """)
            result = db.execute(query_regente, {"id_persona": id_persona})
            count_regente = result.fetchone()[0]
            if count_regente > 0:
                dependencias['tiene_solicitudes_regente'] = True
                dependencias['mensajes'].append(f"La persona es regente en {count_regente} solicitud(es) de retiro. Debe reasignar las solicitudes primero.")
        
        # Verificar si tiene derivaciones (quien deriva) - SOLO INFORMATIVO, no bloquea
        query_deriva = text("SELECT COUNT(*) FROM derivaciones WHERE id_quien_deriva = :id_persona")
        result = db.execute(query_deriva, {"id_persona": id_persona})
        count_deriva = result.fetchone()[0]
        if count_deriva > 0:
            dependencias['tiene_derivaciones_deriva'] = True
            # No agregar a mensajes porque no bloquea la eliminación
        
        # Verificar si tiene derivaciones (quien recibe) - SOLO INFORMATIVO, no bloquea
        query_recibe = text("SELECT COUNT(*) FROM derivaciones WHERE id_quien_recibe = :id_persona")
        result = db.execute(query_recibe, {"id_persona": id_persona})
        count_recibe = result.fetchone()[0]
        if count_recibe > 0:
            dependencias['tiene_derivaciones_recibe'] = True
            # No agregar a mensajes porque no bloquea la eliminación
        
        # Verificar si subió adjuntos - SOLO INFORMATIVO, no bloquea
        # Nota: id_subido_por hace referencia a usuarios.id_usuario, no a personas.id_persona
        # Por lo tanto, esta verificación requiere una relación indirecta a través de usuarios
        # Como es solo informativo y puede causar errores si la estructura cambia, lo manejamos con try-except
        try:
            # Intentar verificar adjuntos a través de la relación usuario-persona
            # Si no hay relación directa, simplemente no marcamos esta dependencia
            query_adjuntos = text("""
                SELECT COUNT(*) FROM adjuntos a
                INNER JOIN usuarios u ON a.id_subido_por = u.id_usuario
                WHERE u.id_persona = :id_persona
            """)
            result = db.execute(query_adjuntos, {"id_persona": id_persona})
            count_adjuntos = result.fetchone()[0]
            if count_adjuntos > 0:
                dependencias['tiene_adjuntos'] = True
                # No agregar a mensajes porque no bloquea la eliminación
        except Exception as e:
            # Si hay algún error (columna no existe, estructura diferente, etc.), simplemente ignorar
            # ya que esta verificación es solo informativa
            # Log del error para debugging si es necesario
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"Error al verificar adjuntos para persona {id_persona}: {str(e)}")
            pass
        
        # Verificar si registró esquelas - SOLO INFORMATIVO, no bloquea
        query_esquelas = text("SELECT COUNT(*) FROM esquelas WHERE id_registrador = :id_persona")
        result = db.execute(query_esquelas, {"id_persona": id_persona})
        count_esquelas = result.fetchone()[0]
        if count_esquelas > 0:
            dependencias['tiene_esquelas'] = True
            # No agregar a mensajes porque no bloquea la eliminación
        
        # Verificar si está en profesores_cursos_materias (aunque es poco probable para administrativos)
        query_profesor = text("SELECT COUNT(*) FROM profesores_cursos_materias WHERE id_profesor = :id_persona")
        result = db.execute(query_profesor, {"id_persona": id_persona})
        count_profesor = result.fetchone()[0]
        if count_profesor > 0:
            dependencias['tiene_profesor_cursos'] = True
            dependencias['mensajes'].append(f"La persona está asignada a {count_profesor} curso(s) como profesor. Debe desasociar primero.")
        
        # Determinar si se puede eliminar
        # No se puede eliminar si tiene usuario, incidentes como responsable, o solicitudes como recepcionista/regente
        dependencias['puede_eliminar'] = not (
            dependencias['tiene_usuario'] or
            dependencias['tiene_incidentes'] or
            dependencias['tiene_solicitudes_recepcionista'] or
            dependencias['tiene_solicitudes_regente'] or
            dependencias['tiene_profesor_cursos']
        )
        
        return dependencias

