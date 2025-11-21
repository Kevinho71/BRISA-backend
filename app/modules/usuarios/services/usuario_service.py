"""
app/modules/usuarios/services/usuario_service
Servicios del Módulo de Usuarios - FINAL
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
from fastapi import HTTPException, status
from app.core.database import SessionLocal
from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona1, Rol, Permiso, LoginLog, RolHistorial, usuario_roles_table
)
from app.modules.auth.services.auth_service import AuthService
from app.modules.usuarios.dto.usuario_dto import (
    PersonaCreateDTO, PersonaUpdateDTO, PersonaResponseDTO,
    UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO,
    RolCreateDTO, RolUpdateDTO, RolResponseDTO, 
    PermisoCreateDTO, PermisoResponseDTO,PersonasStatsDTO,
    AsignarRolDTO
)
from app.modules.usuarios.models.usuario_models import Bitacora
from app.shared.services.base_services import BaseService
from app.shared.exceptions.custom_exceptions import NotFound, Conflict, ValidationException, DatabaseException
from app.shared.security import hash_password, verify_password
from app.shared.permission_mapper import puede_modificar_usuario
import unicodedata

from app.shared.decorators.auth_decorators import (
    verificar_permiso, 
    validar_puede_modificar_usuario
)
import random
import string
import re


logger = logging.getLogger(__name__)

def limpiar_texto(texto: str) -> str:
        """Normaliza texto, elimina tildes y caracteres especiales."""
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")
        texto = re.sub(r'[^a-zA-Z0-9]', '', texto)
        return texto.lower()

class PersonaService(BaseService):
    """Servicio de gestión de personas con generación automática de credenciales"""
    model_class = Persona1
    
    @staticmethod
    def limpiar_texto(texto: str) -> str:
        """Limpiar texto para generar username"""
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
            'ñ': 'n', 'Ñ': 'n', 'ü': 'u', 'Ü': 'u'
        }
        for old, new in replacements.items():
            texto = texto.replace(old, new)
        texto = texto.replace(' ', '').lower()
        texto = re.sub(r'[^a-z]', '', texto)
        return texto
    
    @staticmethod
    def generar_username_base(nombres: str, apellido_paterno: str) -> str:
        """Generar username: primera_letra_apellido + nombre"""
        nombres_limpio = PersonaService.limpiar_texto(nombres)
        apellido_limpio = PersonaService.limpiar_texto(apellido_paterno)
        
        if not nombres_limpio or not apellido_limpio:
            raise ValueError("Nombres y apellidos deben contener al menos una letra válida")
        
        return apellido_limpio[0] + nombres_limpio
    
    @staticmethod
    def validar_username_disponible(db: Session, username: str) -> str:
        """Validar username disponible, agregar número si existe"""
        username_final = username
        contador = 1
        
        while db.query(Usuario).filter(Usuario.usuario == username_final).first():
            username_final = f"{username}{contador}"
            contador += 1
            if contador > 100:
                raise DatabaseException("No se pudo generar username único")
        
        return username_final
    
    @staticmethod
    def generar_password_temporal() -> str:
        """Generar contraseña temporal: Temporal{año}*{números}"""
        año_actual = datetime.now().year
        numeros = ''.join(random.choices(string.digits, k=3))
        simbolo = random.choice('*#@!')
        return f"Temporal{año_actual}{simbolo}{numeros}"
    

    @classmethod
    def crear_persona_con_usuario(cls, db: Session, persona_dto: PersonaCreateDTO, user_id: Optional[int] = None) -> dict:
        """Crear persona con generación automática de credenciales"""
        try:
            # ✅ Validar CI único
            if db.query(Persona1).filter(Persona1.ci == persona_dto.ci).first():
                raise Conflict(f"CI {persona_dto.ci} ya está registrado")
            
            # ✅ Validar correo único
            if persona_dto.correo:
                if db.query(Persona1).filter(Persona1.correo == persona_dto.correo).first():
                    raise Conflict(f"Correo {persona_dto.correo} ya está registrado")
            
            # Crear persona
            persona_data = persona_dto.dict(exclude={'tiene_acceso', 'id_rol'})
            persona = Persona1(**persona_data)
            db.add(persona)
            db.flush()
            
            credenciales = None
            usuario_creado = None
            
            # ¿Generar credenciales?
            if persona_dto.tiene_acceso:
                username_base = cls.generar_username_base(persona.nombres, persona.apellido_paterno)
                username_final = cls.validar_username_disponible(db, username_base)
                password_temporal = cls.generar_password_temporal()
                
                usuario_creado = Usuario(
                    id_persona=persona.id_persona,
                    usuario=username_final,
                    correo=persona.correo,
                    password=hash_password(password_temporal),
                    is_active=True
                )
                db.add(usuario_creado)
                db.flush()
                
                # Asignar rol
                if persona_dto.id_rol:
                    rol = db.query(Rol).filter(Rol.id_rol == persona_dto.id_rol, Rol.is_active == True).first()
                    if rol:
                        usuario_creado.roles.append(rol)
                
                credenciales = {
                    "usuario": username_final,
                    "password_temporal": password_temporal,
                    "mensaje": "⚠ Guarde estas credenciales"
                }
            
            # Bitácora
            if user_id:
                bitacora = Bitacora(
                    id_usuario_admin=user_id,
                    accion="CREAR_PERSONA",
                    tipo_objetivo="Persona",
                    id_objetivo=persona.id_persona,
                    descripcion=f"Persona creada: {persona.nombre_completo}"
                )
                db.add(bitacora)
            
            db.commit()
            db.refresh(persona)
            
            persona_response = PersonaResponseDTO.from_orm(persona)
            if usuario_creado:
                persona_response.usuario = credenciales['usuario']
                persona_response.id_usuario = usuario_creado.id_usuario
                persona_response.tiene_acceso = True
            
            return {"persona": persona_response.dict(), "credenciales": credenciales}
        
        # ✅ CRÍTICO: NO convertir Conflict en DatabaseException
        except Conflict:
            db.rollback()
            raise  # ← Re-lanzar sin modificar
        
        except ValidationException:
            db.rollback()
            raise  # ← Re-lanzar sin modificar
        
        # ✅ Solo capturar errores de SQLAlchemy
        except IntegrityError as e:
            db.rollback()
            error_msg = str(e.orig)
            
            # Detectar tipo de conflicto
            if "Duplicate entry" in error_msg and "ci" in error_msg.lower():
                raise Conflict(f"CI {persona_dto.ci} ya está registrado")
            elif "Duplicate entry" in error_msg and "correo" in error_msg.lower():
                raise Conflict(f"Correo {persona_dto.correo} ya está registrado")
            else:
                raise Conflict("Valor duplicado en la base de datos")
        
        except SQLAlchemyError as e:
            db.rollback()
            raise DatabaseException(f"Error de base de datos: {str(e)}")
        
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error inesperado: {str(e)}")
    
    @classmethod
    def listar_personas(
        cls, 
        db: Session, 
        skip: int = 0, 
        limit: int = 10000,  # ✅ AUMENTADO: Cargar todos por defecto
        tipo_persona: Optional[str] = None,
        busqueda: Optional[str] = None,  # ✅ NUEVO: Búsqueda general
        estado: Optional[str] = None  # ✅ NUEVO: Filtro activo/inactivo
    ) -> List[dict]:
        """
        Listar personas con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Registros a saltar (paginación)
            limit: Límite de registros (por defecto 10000 = todos)
            tipo_persona: 'profesor' o 'administrativo'
            busqueda: Texto para buscar en nombres, CI, correo
            estado: 'activo' o 'inactivo'
        """
        query = db.query(Persona1)
        
        # Filtro por tipo
        if tipo_persona:
            query = query.filter(Persona1.tipo_persona == tipo_persona)
        
        # Filtro por estado
        if estado:
            if estado == 'activo':
                query = query.filter(Persona1.is_active == True)
            elif estado == 'inactivo':
                query = query.filter(Persona1.is_active == False)
        else:
            # Por defecto, mostrar activos e inactivos
            pass
        
        # Búsqueda general
        if busqueda:
            busqueda_lower = f"%{busqueda.lower()}%"
            query = query.filter(
                db.or_(
                    Persona1.nombres.ilike(busqueda_lower),
                    Persona1.apellido_paterno.ilike(busqueda_lower),
                    Persona1.apellido_materno.ilike(busqueda_lower),
                    Persona1.ci.ilike(busqueda_lower),
                    Persona1.correo.ilike(busqueda_lower)
                )
            )
        
        # Ordenar por nombre
        query = query.order_by(Persona1.apellido_paterno, Persona1.nombres)
        
        # Aplicar paginación
        personas = query.offset(skip).limit(limit).all()
        
        # Construir respuesta
        resultado = []
        for persona in personas:
            usuario = db.query(Usuario).filter(
                Usuario.id_persona == persona.id_persona
            ).first()
            
            persona_dict = PersonaResponseDTO.from_orm(persona).dict()
            persona_dict['tiene_acceso'] = usuario is not None
            if usuario:
                persona_dict['usuario'] = usuario.usuario
                persona_dict['id_usuario'] = usuario.id_usuario
            
            resultado.append(persona_dict)
        
        return resultado
    
    @classmethod
    def actualizar_persona(cls, db: Session, persona_id: int, persona_dto: PersonaUpdateDTO, user_id: Optional[int] = None) -> dict:
        """Actualizar persona"""
        persona = db.query(Persona1).filter(Persona1.id_persona == persona_id, Persona1.is_active == True).first()
        if not persona:
            raise NotFound("Persona", persona_id)
        
        try:
            data = persona_dto.dict(exclude_unset=True)
            for key, value in data.items():
                if value is not None:
                    setattr(persona, key, value)
            
            if user_id:
                bitacora = Bitacora(
                    id_usuario_admin=user_id,
                    accion="EDITAR_PERSONA",
                    tipo_objetivo="Persona",
                    id_objetivo=persona_id,
                    descripcion=f"Persona editada: {persona.nombre_completo}"
                )
                db.add(bitacora)
            
            db.commit()
            db.refresh(persona)
            return PersonaResponseDTO.from_orm(persona).dict()
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error: {str(e)}")
    
    @classmethod
    def eliminar_persona(cls, db: Session, persona_id: int, user_id: Optional[int] = None) -> dict:
        """
        Eliminar persona (borrado lógico)
        ✅ CORREGIDO: Evita el error de UnmappedColumnError
        """
        # 1. Verificar que existe
        persona = db.query(Persona1).filter(Persona1.id_persona == persona_id).first()
        if not persona:
            raise NotFound("Persona", persona_id)
        
        # 2. Guardar nombre antes de modificar
        nombre_completo = persona.nombre_completo
        
        try:
            # 3. Desactivar usuario asociado PRIMERO (query directa sin relación)
            db.query(Usuario).filter(
                Usuario.id_persona == persona_id
            ).update(
                {"is_active": False},
                synchronize_session=False  # ✅ CRÍTICO: Evita sync de relaciones
            )
            
            # 4. Desactivar persona
            persona.is_active = False
            
            # 5. Registrar en bitácora
            if user_id:
                bitacora = Bitacora(
                    id_usuario_admin=user_id,
                    accion="ELIMINAR_PERSONA",
                    tipo_objetivo="Persona",
                    id_objetivo=persona_id,
                    descripcion=f"Persona eliminada: {nombre_completo}"
                )
                db.add(bitacora)
            
            # 6. Commit
            db.commit()
            
            return {
                "mensaje": "Persona eliminada exitosamente",
                "id_persona": persona_id,
                "nombre_completo": nombre_completo
            }
            
        except Exception as e:
            db.rollback()
            import traceback
            print(f"❌ ERROR en eliminar_persona:")
            print(traceback.format_exc())
            raise DatabaseException(f"Error al eliminar persona: {str(e)}")
        
    @classmethod
    def obtener_estadisticas(cls, db: Session) -> PersonasStatsDTO:
        """
        Obtener estadísticas de personas
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            PersonasStatsDTO: Estadísticas generales
        """
        total_personas = db.query(Persona1).count()
        total_profesores = db.query(Persona1).filter(
            Persona1.tipo_persona == 'profesor'
        ).count()
        total_administrativos = db.query(Persona1).filter(
            Persona1.tipo_persona == 'administrativo'
        ).count()
        personas_activas = db.query(Persona1).filter(
            Persona1.is_active == True
        ).count()
        personas_inactivas = db.query(Persona1).filter(
            Persona1.is_active == False
        ).count()
        
        # Contar personas con usuario
        personas_con_usuario = db.query(Persona1).join(
            Usuario, Persona1.id_persona == Usuario.id_persona
        ).count()
        
        personas_sin_usuario = total_personas - personas_con_usuario
        
        return PersonasStatsDTO(
            total_personas=total_personas,
            total_profesores=total_profesores,
            total_administrativos=total_administrativos,
            personas_activas=personas_activas,
            personas_inactivas=personas_inactivas,
            personas_con_usuario=personas_con_usuario,
            personas_sin_usuario=personas_sin_usuario
        )
    
    @staticmethod
    def _build_persona_response(db: Session, persona: Persona1) -> PersonaResponseDTO:
        """
        Construir respuesta de persona con información adicional
        
        Args:
            db: Sesión de base de datos
            persona: Objeto Persona1
            
        Returns:
            PersonaResponseDTO con información completa
        """
        # Verificar si tiene usuario asociado
        usuario = db.query(Usuario).filter(
            Usuario.id_persona == persona.id_persona
        ).first()
        
        usuario_info = None
        tiene_usuario = False
        
        if usuario:
            tiene_usuario = True
            usuario_info = {
                "id_usuario": usuario.id_usuario,
                "usuario": usuario.usuario,
                "correo": usuario.correo,
                "is_active": usuario.is_active
            }
        
        return PersonaResponseDTO(
            id_persona=persona.id_persona,
            ci=persona.ci,
            nombres=persona.nombres,
            apellido_paterno=persona.apellido_paterno,
            apellido_materno=persona.apellido_materno,
            nombre_completo=persona.nombre_completo,
            direccion=persona.direccion,
            telefono=persona.telefono,
            correo=persona.correo,
            tipo_persona=persona.tipo_persona,
            is_active=persona.is_active,
            tiene_usuario=tiene_usuario,
            usuario_info=usuario_info
        )

    def generar_username_base(nombres: str, apellido_paterno: str) -> str:
        nombres_limpio = limpiar_texto(nombres.split()[0])
        apellido_limpio = limpiar_texto(apellido_paterno)
        return f"{nombres_limpio}.{apellido_limpio}"

    def validar_username_disponible(db, username_base: str) -> str:
        username = username_base
        counter = 1
        from app.modules.usuarios.models.usuario_models import Usuario

        while db.query(Usuario).filter(Usuario.username == username).first():
            username = f"{username_base}{counter}"
            counter += 1

        return username

    def generar_password_temporal() -> str:
        year = datetime.now().year
        simbolo = random.choice(["@", "#", "$"])
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"Temporal{year}{simbolo}{numeros}"

class UsuarioService(BaseService):
    """Servicio de gestión de usuarios (RF-01, RF-06, RF-08)"""
    model_class = Usuario
    
    @classmethod
    def crear_usuario(cls, db: Session, usuario_dto: UsuarioCreateDTO, user_id: Optional[int] = None) -> UsuarioResponseDTO:
        """Crear nuevo usuario vinculado a persona"""
        persona = db.query(Persona1).filter(
            Persona1.id_persona == usuario_dto.id_persona, 
            Persona1.is_active == True
        ).first()
        if not persona:
            raise NotFound("Persona", usuario_dto.id_persona)
        
        usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario_dto.correo).first()
        if usuario_existente:
            raise Conflict(f"Correo {usuario_dto.correo} ya registrado")
        
        try:
            data = usuario_dto.dict(exclude_unset=True)
            data['password'] = hash_password(data.pop('password'))
            
            usuario = Usuario(**data)
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            logger.info(f"Usuario creado: {usuario.correo}")
            return UsuarioResponseDTO.from_orm(usuario)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al crear usuario: {str(e)}")
            raise DatabaseException(f"Error al crear usuario: {str(e)}")
    
    @classmethod
    def obtener_usuario(cls, db: Session, usuario_id: int) -> UsuarioResponseDTO:
        """Obtener usuario por ID"""
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id, 
            Usuario.is_active == True
        ).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        usuario_dict = {
            'id_usuario': usuario.id_usuario,
            'id_persona': usuario.id_persona,
            'usuario': usuario.usuario,
            'correo': usuario.correo,
            'is_active': usuario.is_active
        }
        return UsuarioResponseDTO(**usuario_dict)
        
    @classmethod
    def obtener_usuario_por_correo(cls, db: Session, correo: str) -> Usuario:
        """Obtener usuario por correo para autenticación"""
        usuario = db.query(Usuario).filter(
            Usuario.correo == correo, 
            Usuario.is_active == True
        ).first()
        if not usuario:
            raise NotFound("Usuario", correo)
        return usuario
    
    @classmethod
    def listar_usuarios(cls, db: Session, skip: int = 0, limit: int = 50, estado: str | None = None):
        """Listar usuarios con paginación"""
        usuarios = db.query(Usuario).offset(skip).limit(limit).all()
        return [UsuarioResponseDTO.model_validate(u) for u in usuarios]

    @classmethod
    def actualizar_usuario(
        cls, 
        db: Session, 
        usuario_id: int, 
        usuario_dto: UsuarioUpdateDTO, 
        current_user: Usuario
    ) -> UsuarioResponseDTO:
        """Actualizar usuario con validación de permisos"""
        if not puede_modificar_usuario(current_user, usuario_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para modificar este usuario"
            )
        
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id, 
            Usuario.is_active == True
        ).first()
        
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        try:
            data = usuario_dto.dict(exclude_unset=True)
            
            if 'password' in data:
                data['password'] = AuthService.hash_password(data['password'])
            
            if 'correo' in data:
                otro_usuario = db.query(Usuario).filter(
                    Usuario.correo == data['correo'],
                    Usuario.id_usuario != usuario_id
                ).first()
                if otro_usuario:
                    raise Conflict(f"Correo {data['correo']} ya registrado")
            
            for key, value in data.items():
                if value is not None:
                    setattr(usuario, key, value)
            
            usuario.updated_by = current_user.id_usuario
            
            db.commit()
            db.refresh(usuario)
            
            logger.info(f"Usuario actualizado: {usuario.correo} por usuario {current_user.id_usuario}")
            
            usuario_dict = {
                'id_usuario': usuario.id_usuario,
                'id_persona': usuario.id_persona,
                'usuario': usuario.usuario,
                'correo': usuario.correo,
                'is_active': usuario.is_active
            }
            return UsuarioResponseDTO(**usuario_dict)
            
        except Conflict:
            raise
        except NotFound:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar usuario: {str(e)}")
            raise DatabaseException(f"Error al actualizar usuario: {str(e)}")

    @classmethod
    def eliminar_usuario(
        cls, 
        db: Session, 
        usuario_id: int, 
        current_user: Usuario
    ) -> dict:
        """Eliminar usuario (borrado lógico) con validación de permisos"""
        from app.shared.decorators.auth_decorators import verificar_permiso
        
        verificar_permiso(current_user, 'eliminar_usuario')
        
        if current_user.id_usuario == usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puede eliminar su propio usuario"
            )
        
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id, 
            Usuario.is_active == True
        ).first()
        
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        try:
            usuario.is_active = False
            usuario.updated_by = current_user.id_usuario
            
            db.commit()
            
            logger.info(f"Usuario eliminado: ID {usuario_id} por usuario {current_user.id_usuario}")
            
            return {
                "mensaje": "Usuario eliminado exitosamente",
                "id_usuario": usuario_id,
                "usuario": usuario.usuario
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar usuario: {str(e)}")
            raise DatabaseException(f"Error al eliminar usuario: {str(e)}")            
    
    @classmethod
    def asignar_rol(cls, db: Session, usuario_id: int, rol_id: int, razon: Optional[str] = None, user_id: Optional[int] = None) -> dict:
        """Asignar rol a usuario (RF-02) con historial"""
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id, 
            Usuario.is_active == True
        ).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id, 
            Rol.is_active == True
        ).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        if rol in usuario.roles:
            raise Conflict("Usuario ya tiene este rol")
        
        try:
            usuario.roles.append(rol)
            
            historial = RolHistorial(
                id_usuario=usuario_id,
                id_rol=rol_id,
                accion='asignado',
                razon=razon
            )
            db.add(historial)
            db.commit()
            
            logger.info(f"Rol {rol.nombre} asignado a usuario {usuario_id}")
            return {"mensaje": f"Rol {rol.nombre} asignado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al asignar rol: {str(e)}")
            raise DatabaseException(f"Error al asignar rol: {str(e)}")
    
    @classmethod
    def revocar_rol(cls, db: Session, usuario_id: int, rol_id: int, razon: Optional[str] = None, user_id: Optional[int] = None) -> dict:
        """Revocar rol de usuario (RF-02)"""
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id, 
            Usuario.is_active == True
        ).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            if rol in usuario.roles:
                usuario.roles.remove(rol)
                
                historial = RolHistorial(
                    id_usuario=usuario_id,
                    id_rol=rol_id,
                    accion='revocado',
                    razon=razon
                )
                db.add(historial)
                db.commit()
            
            logger.info(f"Rol {rol.nombre} revocado de usuario {usuario_id}")
            return {"mensaje": f"Rol {rol.nombre} revocado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al revocar rol: {str(e)}")
            raise DatabaseException(f"Error al revocar rol: {str(e)}")


class RolService:
    """Servicio de gestión de roles (RF-02, RF-03, RF-04)"""
    
    model_class = Rol
    
    @classmethod
    def crear_rol(cls, db: Session, rol_dto: RolCreateDTO, current_user: Usuario = None) -> RolResponseDTO:
        """Crear nuevo rol con validación de permisos"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'crear_rol'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para crear roles"
                )
        
        # Verificar duplicado ANTES del try
        rol_existente = db.query(Rol).filter(Rol.nombre == rol_dto.nombre).first()
        if rol_existente:
            logger.warning(f"Intento de crear rol duplicado: {rol_dto.nombre}")
            raise Conflict(f"Rol con nombre {rol_dto.nombre} ya existe")
        
        try:
            data = rol_dto.dict(exclude_unset=True)
            rol = Rol(**data)
            
            if current_user:
                rol.created_by = current_user.id_usuario
            
            db.add(rol)
            db.flush()
            
            # ✅ Registrar en bitácora
            from app.modules.auth.services.auth_service import AuthService
            if current_user:
                AuthService.registrar_bitacora(
                    db,
                    usuario_id=current_user.id_usuario,
                    accion='CREAR_ROL',
                    tipo_objetivo='Rol',
                    id_objetivo=rol.id_rol,
                    descripcion=f"Rol '{rol.nombre}' creado"
                )
            
            db.commit()
            db.refresh(rol)
            logger.info(f"Rol creado: {rol.nombre}")
            return RolResponseDTO.from_orm(rol)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al crear rol: {str(e)}")
            raise DatabaseException(f"Error al crear rol: {str(e)}")
    
    @classmethod
    def obtener_rol(cls, db: Session, rol_id: int) -> RolResponseDTO:
        """Obtener rol por ID con contador de permisos y lista de permisos"""
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id, 
            Rol.is_active == True
        ).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        # ✅ Construir respuesta con permisos incluidos
        rol_dto = RolResponseDTO.from_orm(rol)
        
        # ✅ Contar permisos activos
        rol_dto.permisosCount = len([p for p in rol.permisos if p.is_active])
        
        # ✅ Contar usuarios activos
        rol_dto.usuariosCount = len([u for u in rol.usuarios if u.is_active])
        
        # ✅ AGREGAR LISTA DE PERMISOS (esto faltaba)
        rol_dto.permisos = [
            {
                "id_permiso": p.id_permiso,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "modulo": p.modulo
            }
            for p in rol.permisos if p.is_active
        ]
        
        return rol_dto
    
    @classmethod
    def listar_roles(cls, db: Session, skip: int = 0, limit: int = 50):
        """Listar roles con contadores de permisos y usuarios"""
        roles = db.query(Rol).filter(Rol.is_active == True).offset(skip).limit(limit).all()
        
        roles_dto = []
        for rol in roles:
            rol_dto = RolResponseDTO.from_orm(rol)
            # ✅ Agregar contadores
            rol_dto.permisosCount = len([p for p in rol.permisos if p.is_active])
            rol_dto.usuariosCount = len([u for u in rol.usuarios if u.is_active])
            roles_dto.append(rol_dto)
        
        return roles_dto
    
    @classmethod
    def actualizar_rol(
        cls, 
        db: Session, 
        rol_id: int, 
        rol_dto: RolUpdateDTO, 
        current_user: Usuario = None
    ) -> RolResponseDTO:
        """✅ Actualizar rol con registro en bitácora"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'editar_rol'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para editar roles"
                )
        
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id, 
            Rol.is_active == True
        ).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            # Guardar estado anterior
            estado_anterior = {
                'nombre': rol.nombre,
                'descripcion': rol.descripcion
            }
            
            # Aplicar cambios
            data = rol_dto.dict(exclude_unset=True)
            for key, value in data.items():
                if value is not None:
                    setattr(rol, key, value)
            
            if current_user:
                rol.updated_by = current_user.id_usuario
            
            db.flush()
            
            # ✅ Registrar en bitácora
            from app.modules.auth.services.auth_service import AuthService
            if current_user:
                cambios = []
                for key in data.keys():
                    if estado_anterior.get(key) != data.get(key):
                        cambios.append(f"{key}: '{estado_anterior.get(key)}' → '{data.get(key)}'")
                
                AuthService.registrar_bitacora(
                    db,
                    usuario_id=current_user.id_usuario,
                    accion='EDITAR_ROL',
                    tipo_objetivo='Rol',
                    id_objetivo=rol.id_rol,
                    descripcion=f"Rol '{rol.nombre}' actualizado. Cambios: {', '.join(cambios)}"
                )
            
            db.commit()
            db.refresh(rol)
            logger.info(f"Rol actualizado: {rol.nombre}")
            
            # Retornar con contadores
            rol_response = RolResponseDTO.from_orm(rol)
            rol_response.permisosCount = len([p for p in rol.permisos if p.is_active])
            rol_response.usuariosCount = len([u for u in rol.usuarios if u.is_active])
            
            return rol_response
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar rol: {str(e)}")
            raise DatabaseException(f"Error al actualizar rol: {str(e)}")
    
    @classmethod
    def eliminar_rol(
        cls, 
        db: Session, 
        rol_id: int, 
        current_user: Usuario = None
    ) -> dict:
        """✅ Eliminar rol (borrado lógico) con registro en bitácora"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'eliminar_rol'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para eliminar roles"
                )
        
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id, 
            Rol.is_active == True
        ).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        # ✅ Verificar si tiene usuarios asignados
        usuarios_activos = [u for u in rol.usuarios if u.is_active]
        if usuarios_activos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el rol '{rol.nombre}' porque tiene {len(usuarios_activos)} usuarios asignados"
            )
        
        try:
            nombre_rol = rol.nombre  # Guardar antes de eliminar
            
            rol.is_active = False
            if current_user:
                rol.updated_by = current_user.id_usuario
            
            db.flush()
            
            # ✅ Registrar en bitácora
            from app.modules.auth.services.auth_service import AuthService
            if current_user:
                AuthService.registrar_bitacora(
                    db,
                    usuario_id=current_user.id_usuario,
                    accion='ELIMINAR_ROL',
                    tipo_objetivo='Rol',
                    id_objetivo=rol_id,
                    descripcion=f"Rol '{nombre_rol}' eliminado (borrado lógico)"
                )
            
            db.commit()
            logger.info(f"Rol eliminado: ID {rol_id}")
            
            return {
                "mensaje": "Rol eliminado exitosamente",
                "id_rol": rol_id,
                "nombre": nombre_rol
            }
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar rol: {str(e)}")
            raise DatabaseException(f"Error al eliminar rol: {str(e)}")
    
    @classmethod
    def asignar_permisos_rol(
        cls, 
        db: Session, 
        rol_id: int, 
        permisos_ids: List[int], 
        current_user: Usuario = None
    ) -> RolResponseDTO:
        """✅ Asignar permisos a rol (RF-04) con bitácora"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'asignar_permisos'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para asignar permisos"
                )
        
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id, 
            Rol.is_active == True
        ).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            # Obtener permisos anteriores
            permisos_anteriores = {p.id_permiso: p.nombre for p in rol.permisos if p.is_active}
            
            # Obtener nuevos permisos
            permisos = db.query(Permiso).filter(
                Permiso.id_permiso.in_(permisos_ids), 
                Permiso.is_active == True
            ).all()
            
            if len(permisos) != len(permisos_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Algunos permisos no existen o están inactivos"
                )
            
            # Actualizar permisos
            rol.permisos = permisos
            
            if current_user:
                rol.updated_by = current_user.id_usuario
            
            db.flush()
            
            # ✅ Registrar en bitácora
            from app.modules.auth.services.auth_service import AuthService
            if current_user:
                permisos_nuevos = {p.id_permiso: p.nombre for p in permisos}
                
                agregados = [nombre for id, nombre in permisos_nuevos.items() if id not in permisos_anteriores]
                removidos = [nombre for id, nombre in permisos_anteriores.items() if id not in permisos_nuevos]
                
                cambios = []
                if agregados:
                    cambios.append(f"Agregados: {', '.join(agregados)}")
                if removidos:
                    cambios.append(f"Removidos: {', '.join(removidos)}")
                
                descripcion = f"Permisos del rol '{rol.nombre}' actualizados. {' | '.join(cambios)}" if cambios else f"Permisos del rol '{rol.nombre}' actualizados"
                
                AuthService.registrar_bitacora(
                    db,
                    usuario_id=current_user.id_usuario,
                    accion='ASIGNAR_PERMISOS',
                    tipo_objetivo='Rol',
                    id_objetivo=rol.id_rol,
                    descripcion=descripcion
                )
            
            db.commit()
            db.refresh(rol)
            
            logger.info(f"Permisos asignados al rol {rol_id}")
            
            # Retornar con contadores
            rol_response = RolResponseDTO.from_orm(rol)
            rol_response.permisosCount = len([p for p in rol.permisos if p.is_active])
            rol_response.usuariosCount = len([u for u in rol.usuarios if u.is_active])
            
            return rol_response
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al asignar permisos: {str(e)}")
            raise DatabaseException(f"Error al asignar permisos: {str(e)}")
    
    @classmethod
    def asignar_rol_usuario(
        cls, 
        db: Session, 
        id_usuario: int, 
        id_rol: int, 
        current_user: Usuario = None
    ) -> dict:
        """Asignar rol a usuario"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'asignar_permisos'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para asignar roles"
                )
        
        return UsuarioService.asignar_rol(
            db, 
            id_usuario, 
            id_rol, 
            user_id=current_user.id_usuario if current_user else None
        )
    
    @classmethod
    def remover_rol_usuario(
        cls,
        db: Session,
        usuario_id: int,
        rol_id: int,
        current_user: Usuario = None
    ) -> dict:
        """Remover rol de un usuario"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'asignar_permisos'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para remover roles"
                )
        
        usuario = db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id,
            Usuario.is_active == True
        ).first()
        
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id,
            Rol.is_active == True
        ).first()
        
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            if rol not in usuario.roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El usuario no tiene asignado el rol {rol.nombre}"
                )
            
            usuario.roles.remove(rol)
            if current_user:
                usuario.updated_by = current_user.id_usuario
            
            db.commit()
            
            logger.info(f"Rol {rol_id} removido de usuario {usuario_id}")
            
            return {
                "mensaje": "Rol removido exitosamente",
                "usuario_id": usuario_id,
                "rol_id": rol_id
            }
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al remover rol: {str(e)}")
            raise DatabaseException(f"Error al remover rol: {str(e)}")

class PermisoService(BaseService):
    """Servicio de gestión de permisos (RF-04)"""
    model_class = Permiso
    
    @classmethod
    def crear_permiso(cls, db: Session, permiso_dto: PermisoCreateDTO, user_id: Optional[int] = None) -> PermisoResponseDTO:
        """Crear nuevo permiso"""
        permiso_existente = db.query(Permiso).filter(Permiso.nombre == permiso_dto.nombre).first()
        if permiso_existente:
            raise Conflict(f"Permiso con nombre {permiso_dto.nombre} ya existe")
        
        try:
            data = permiso_dto.dict(exclude_unset=True)
            permiso = Permiso(**data)
            db.add(permiso)
            db.commit()
            db.refresh(permiso)
            logger.info(f"Permiso creado: {permiso.nombre}")
            return PermisoResponseDTO.from_orm(permiso)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al crear permiso: {str(e)}")
            raise DatabaseException(f"Error al crear permiso: {str(e)}")
    
    @classmethod
    def obtener_permiso(cls, db: Session, permiso_id: int) -> PermisoResponseDTO:
        """Obtener permiso por ID"""
        permiso = db.query(Permiso).filter(
            Permiso.id_permiso == permiso_id, 
            Permiso.is_active == True
        ).first()
        if not permiso:
            raise NotFound("Permiso", permiso_id)
        return PermisoResponseDTO.from_orm(permiso)
    
    @classmethod
    def listar_permisos(cls, db: Session, skip: int = 0, limit: int = 100, modulo: Optional[str] = None):
        """Listar permisos con filtros"""
        query = db.query(Permiso).filter(Permiso.is_active == True)
        
        if modulo:
            query = query.filter(Permiso.modulo == modulo)
        
        permisos = query.offset(skip).limit(limit).all()
        return [PermisoResponseDTO.from_orm(p) for p in permisos]
    
    @classmethod
    def obtener_roles_con_permiso(cls, db: Session, permiso_id: int) -> List[dict]:
        """Obtener roles que tienen un permiso específico con contador de usuarios"""
        permiso = db.query(Permiso).filter(
            Permiso.id_permiso == permiso_id,
            Permiso.is_active == True
        ).first()
        
        if not permiso:
            raise NotFound("Permiso", permiso_id)
        
        roles_data = []
        for rol in permiso.roles:
            if rol.is_active:
                # Contar usuarios activos con este rol
                usuarios_count = db.query(Usuario).join(
                    usuario_roles_table,
                    Usuario.id_usuario == usuario_roles_table.c.id_usuario
                ).filter(
                    usuario_roles_table.c.id_rol == rol.id_rol,
                    Usuario.is_active == True
                ).count()
                
                roles_data.append({
                    "id_rol": rol.id_rol,
                    "nombre": rol.nombre,
                    "descripcion": rol.descripcion,
                    "usuariosCount": usuarios_count
                })
        
        return roles_data