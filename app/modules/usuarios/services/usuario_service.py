"""
Servicios del Módulo de Usuarios - RF-01, RF-02, RF-03, RF-04, RF-06, RF-08
Implementa la lógica de negocio para usuarios, roles y permisos
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from app.core.database import SessionLocal
from app.modules.usuarios.models.usuario_models import (
    Usuario, Persona1, Rol, Permiso, LoginLog, RolHistorial,usuario_roles_table
)

from app.modules.usuarios.dto.usuario_dto import (
    PersonaCreateDTO, PersonaUpdateDTO, PersonaResponseDTO,
    UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO,
    RolCreateDTO, RolUpdateDTO, RolResponseDTO, 
    PermisoCreateDTO, PermisoResponseDTO,
    AsignarRolDTO
)
from app.shared.services.base_services import BaseService
from app.shared.exceptions.custom_exceptions import NotFound, Conflict, ValidationException, DatabaseException
from app.shared.security import hash_password, verify_password

logger = logging.getLogger(__name__)

class PersonaService(BaseService):
    """Servicio de gestión de personas (RF-01)"""
    model_class = Persona1
    
    @classmethod
    def crear_persona(cls, db: Session, persona_dto: PersonaCreateDTO, user_id: Optional[int] = None) -> PersonaResponseDTO:
        """Crear nueva persona"""
        persona_existente = db.query(Persona1).filter(Persona1.cedula == persona_dto.cedula).first()
        if persona_existente:
            raise Conflict(f"Cédula {persona_dto.cedula} ya registrada")
        
        try:
            data = persona_dto.dict(exclude_unset=True)
            data['created_by'] = user_id
            persona = Persona1(**data)
            db.add(persona)
            db.commit()
            db.refresh(persona)
            logger.info(f"Persona creada: {persona.nombre_completo}")
            return PersonaResponseDTO.from_orm(persona)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al crear persona: {str(e)}")
            raise DatabaseException(f"Error al crear persona: {str(e)}")
    
    @classmethod
    def obtener_persona(cls, db: Session, persona_id: int) -> PersonaResponseDTO:
        """Obtener persona por ID"""
        persona = db.query(Persona1).filter(Persona1.id == persona_id, Persona1.is_active == True).first()
        if not persona:
            raise NotFound("Persona", persona_id)
        return PersonaResponseDTO.from_orm(persona)
    
    @classmethod
    def listar_usuarios(cls, db: Session, skip: int = 0, limit: int = 50, estado: Optional[str] = "activo") -> List[UsuarioResponseDTO]:
        """
        Listar usuarios filtrando por el estado de sus roles.
        """
        # Join con la tabla de asociación usuario_roles
        query = db.query(Usuario).join(usuario_roles_table, Usuario.id_usuario == usuario_roles_table.c.id_usuario)

        if estado:
            query = query.filter(usuario_roles_table.c.estado == estado)

        # Evitar duplicados si un usuario tiene varios roles
        query = query.distinct()

        total = query.count()
        usuarios = query.offset(skip).limit(limit).all()

        return [UsuarioResponseDTO.from_orm(u) for u in usuarios]
    

    @classmethod
    def actualizar_persona(cls, db: Session, persona_id: int, persona_dto: PersonaUpdateDTO, user_id: Optional[int] = None) -> PersonaResponseDTO:
        """Actualizar persona"""
        persona = db.query(Persona1).filter(Persona1.id == persona_id, Persona1.is_active == True).first()
        if not persona:
            raise NotFound("Persona", persona_id)
        
        try:
            data = persona_dto.dict(exclude_unset=True)
            for key, value in data.items():
                setattr(persona, key, value)
            persona.updated_by = user_id
            db.commit()
            db.refresh(persona)
            logger.info(f"Persona actualizada: {persona.nombre_completo}")
            return PersonaResponseDTO.from_orm(persona)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar persona: {str(e)}")
            raise DatabaseException(f"Error al actualizar persona: {str(e)}")
    
    @classmethod
    def eliminar_persona(cls, db: Session, persona_id: int, user_id: Optional[int] = None) -> dict:
        """Eliminar persona (borrado lógico)"""
        persona = db.query(Persona1).filter(Persona1.id == persona_id, Persona1.is_active == True).first()
        if not persona:
            raise NotFound("Persona", persona_id)
        
        try:
            persona.is_active = False
            persona.updated_by = user_id
            db.commit()
            logger.info(f"Persona eliminada: ID {persona_id}")
            return {"mensaje": "Persona eliminada exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar persona: {str(e)}")
            raise DatabaseException(f"Error al eliminar persona: {str(e)}")

class UsuarioService(BaseService):
    """Servicio de gestión de usuarios (RF-01, RF-06, RF-08)"""
    model_class = Usuario
    
    @classmethod
    def crear_usuario(cls, db: Session, usuario_dto: UsuarioCreateDTO, user_id: Optional[int] = None) -> UsuarioResponseDTO:
        """Crear nuevo usuario vinculado a persona"""
        # Validar que la persona existe
        persona = db.query(Persona1).filter(Persona1.id == usuario_dto.id_persona, Persona1.is_active == True).first()
        if not persona:
            raise NotFound("Persona", usuario_dto.id_persona)
        
        # Validar correo duplicado
        usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario_dto.correo).first()
        if usuario_existente:
            raise Conflict(f"Correo {usuario_dto.correo} ya registrado")
        
        try:
            data = usuario_dto.dict(exclude_unset=True)
            data['password'] = hash_password(data.pop('password'))
            data['created_by'] = user_id
            
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
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        return UsuarioResponseDTO.from_orm(usuario)
    
    @classmethod
    def obtener_usuario_por_correo(cls, db: Session, correo: str) -> Usuario:
        """Obtener usuario por correo para autenticación"""
        usuario = db.query(Usuario).filter(Usuario.correo == correo, Usuario.is_active == True).first()
        if not usuario:
            raise NotFound("Usuario", correo)
        return usuario
    
    @classmethod
    def listar_usuarios(cls, db: Session, skip: int = 0, limit: int = 50, estado: str | None = None):
        """Listar usuarios con paginación"""
        usuarios = db.query(Usuario).offset(skip).limit(limit).all()
        # Usar model_validate en lugar de from_orm
        return [UsuarioResponseDTO.model_validate(u) for u in usuarios]

    @classmethod
    def actualizar_usuario(cls, db: Session, usuario_id: int, usuario_dto: UsuarioUpdateDTO, user_id: Optional[int] = None) -> UsuarioResponseDTO:
        """Actualizar usuario"""
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        try:
            data = usuario_dto.dict(exclude_unset=True)
            
            # Si hay nueva contraseña, hashearla
            if 'password' in data:
                data['password'] = hash_password(data.pop('password'))
            
            if 'correo' in data:
                # Validar que correo no esté duplicado
                otro_usuario = db.query(Usuario).filter(
                    Usuario.correo == data['correo'],
                    Usuario.id != usuario_id
                ).first()
                if otro_usuario:
                    raise Conflict(f"Correo {data['correo']} ya registrado")
            
            for key, value in data.items():
                if value is not None:
                    setattr(usuario, key, value)
            
            usuario.updated_by = user_id
            db.commit()
            db.refresh(usuario)
            logger.info(f"Usuario actualizado: {usuario.correo}")
            return UsuarioResponseDTO.from_orm(usuario)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar usuario: {str(e)}")
            raise DatabaseException(f"Error al actualizar usuario: {str(e)}")
    
    @classmethod
    def eliminar_usuario(cls, db: Session, usuario_id: int, user_id: Optional[int] = None) -> dict:
        """Eliminar usuario (borrado lógico)"""
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        try:
            usuario.is_active = False
            usuario.updated_by = user_id
            db.commit()
            logger.info(f"Usuario eliminado: ID {usuario_id}")
            return {"mensaje": "Usuario eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar usuario: {str(e)}")
            raise DatabaseException(f"Error al eliminar usuario: {str(e)}")
    
    @classmethod
    def asignar_rol(cls, db: Session, usuario_id: int, rol_id: int, razon: Optional[str] = None, user_id: Optional[int] = None) -> dict:
        """Asignar rol a usuario (RF-02) con historial"""
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        rol = db.query(Rol).filter(Rol.id == rol_id, Rol.is_active == True).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        # Verificar si ya tiene el rol
        if rol in usuario.roles:
            raise Conflict("Usuario ya tiene este rol")
        
        try:
            usuario.roles.append(rol)
            
            historial = RolHistorial(
                id_usuario=usuario_id,
                id_rol=rol_id,
                accion='asignado',
                razon=razon,
                created_by=user_id
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
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            if rol in usuario.roles:
                usuario.roles.remove(rol)
                
                historial = RolHistorial(
                    id_usuario=usuario_id,
                    id_rol=rol_id,
                    accion='revocado',
                    razon=razon,
                    created_by=user_id
                )
                db.add(historial)
                db.commit()
            
            logger.info(f"Rol {rol.nombre} revocado de usuario {usuario_id}")
            return {"mensaje": f"Rol {rol.nombre} revocado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al revocar rol: {str(e)}")
            raise DatabaseException(f"Error al revocar rol: {str(e)}")
    
    @classmethod
    def obtener_historial_roles(cls, db: Session, usuario_id: int) -> List[dict]:
        """Obtener historial de asignación de roles del usuario"""
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise NotFound("Usuario", usuario_id)
        
        historial = db.query(RolHistorial).filter(RolHistorial.id_usuario == usuario_id).order_by(RolHistorial.created_at.desc()).all()
        
        return [{
            "id": h.id,
            "rol_id": h.id_rol,
            "accion": h.accion,
            "fecha": h.created_at.isoformat(),
            "razon": h.razon
        } for h in historial]
    
    @classmethod
    def registrar_login(cls, db: Session, usuario_id: int, ip_address: Optional[str] = None, 
                       user_agent: Optional[str] = None) -> dict:
        """Registrar login de usuario (RF-08)"""
        try:
            login_log = LoginLog(
                id_usuario=usuario_id,
                ip_address=ip_address,
                user_agent=user_agent,
                estado='exitoso',
                created_by=usuario_id
            )
            db.add(login_log)
            db.commit()
            logger.info(f"Login registrado para usuario {usuario_id}")
            return {"mensaje": "Login registrado"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al registrar login: {str(e)}")
            raise DatabaseException(f"Error al registrar login: {str(e)}")
    
    @classmethod
    def obtener_logins_usuario(cls, db: Session, usuario_id: int, limit: int = 50) -> List[dict]:
        """Obtener logins de un usuario"""
        logins = db.query(LoginLog).filter(LoginLog.id_usuario == usuario_id).order_by(LoginLog.created_at.desc()).limit(limit).all()
        
        return [{
            "id": l.id,
            "fecha": l.created_at.isoformat(),
            "ip_address": l.ip_address,
            "estado": l.estado
        } for l in logins]

class RolService(BaseService):
    """Servicio de gestión de roles (RF-02, RF-03, RF-04)"""
    model_class = Rol
    
    @classmethod
    def crear_rol(cls, db: Session, rol_dto: RolCreateDTO, user_id: Optional[int] = None) -> RolResponseDTO:
        """Crear nuevo rol (RF-03)"""
        # Validar nombre duplicado
        rol_existente = db.query(Rol).filter(Rol.nombre == rol_dto.nombre).first()
        if rol_existente:
            raise Conflict(f"Rol con nombre {rol_dto.nombre} ya existe")
        
        try:
            data = rol_dto.dict(exclude_unset=True)
            data['created_by'] = user_id
            rol = Rol(**data)
            db.add(rol)
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
        """Obtener rol por ID"""
        rol = db.query(Rol).filter(Rol.id == rol_id, Rol.is_active == True).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        return RolResponseDTO.from_orm(rol)
    
    @classmethod
    def listar_roles(cls, db: Session, page: int = 1, per_page: int = 10):
        """Listar roles con paginación"""
        query = db.query(Rol).filter(Rol.is_active == True)
        total = query.count()
        roles = query.offset((page-1)*per_page).limit(per_page).all()
        
        return {
            'items': [RolResponseDTO.from_orm(r) for r in roles],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @classmethod
    def actualizar_rol(cls, db: Session, rol_id: int, rol_dto: RolUpdateDTO, user_id: Optional[int] = None) -> RolResponseDTO:
        """Actualizar rol"""
        rol = db.query(Rol).filter(Rol.id == rol_id, Rol.is_active == True).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            data = rol_dto.dict(exclude_unset=True)
            for key, value in data.items():
                if value is not None:
                    setattr(rol, key, value)
            rol.updated_by = user_id
            db.commit()
            db.refresh(rol)
            logger.info(f"Rol actualizado: {rol.nombre}")
            return RolResponseDTO.from_orm(rol)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar rol: {str(e)}")
            raise DatabaseException(f"Error al actualizar rol: {str(e)}")
    
    @classmethod
    def eliminar_rol(cls, db: Session, rol_id: int, user_id: Optional[int] = None) -> dict:
        """Eliminar rol (borrado lógico)"""
        rol = db.query(Rol).filter(Rol.id == rol_id, Rol.is_active == True).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            rol.is_active = False
            rol.updated_by = user_id
            db.commit()
            logger.info(f"Rol eliminado: ID {rol_id}")
            return {"mensaje": "Rol eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar rol: {str(e)}")
            raise DatabaseException(f"Error al eliminar rol: {str(e)}")
    
    @classmethod
    def asignar_permisos(cls, db: Session, rol_id: int, permisos_ids: List[int], user_id: Optional[int] = None) -> RolResponseDTO:
        """Asignar permisos a rol (RF-04)"""
        rol = db.query(Rol).filter(Rol.id == rol_id, Rol.is_active == True).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        
        try:
            permisos = db.query(Permiso).filter(Permiso.id.in_(permisos_ids), Permiso.is_active == True).all()
            rol.permisos = permisos
            rol.updated_by = user_id
            db.commit()
            db.refresh(rol)
            
            logger.info(f"Permisos asignados al rol {rol_id}")
            return RolResponseDTO.from_orm(rol)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al asignar permisos: {str(e)}")
            raise DatabaseException(f"Error al asignar permisos: {str(e)}")
    
    @classmethod
    def asignar_rol_usuario(cls, db: Session, usuario_id: int, rol_id: int, user_id: Optional[int] = None) -> dict:
        """Método adaptador que llama a asignar_rol para mantener compatibilidad con el controlador"""
        return cls.asignar_rol(db, usuario_id, rol_id, user_id=user_id)
    
    @classmethod
    def asignar_permisos_rol(cls, db: Session, rol_id: int, permisos_ids: List[int], user_id: Optional[int] = None) -> RolResponseDTO:
        """Método adaptador que llama a asignar_permisos para mantener compatibilidad con el controlador"""
        return cls.asignar_permisos(db, rol_id, permisos_ids, user_id=user_id)

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
            data['created_by'] = user_id
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
        permiso = db.query(Permiso).filter(Permiso.id == permiso_id, Permiso.is_active == True).first()
        if not permiso:
            raise NotFound("Permiso", permiso_id)
        return PermisoResponseDTO.from_orm(permiso)
    
    @classmethod
    def listar_permisos(cls, db: Session, page: int = 1, per_page: int = 100, modulo: Optional[str] = None):
        """Listar permisos con filtros"""
        query = db.query(Permiso).filter(Permiso.is_active == True)
        
        if modulo:
            query = query.filter(Permiso.modulo == modulo)
        
        total = query.count()
        permisos = query.offset((page-1)*per_page).limit(per_page).all()
        
        return {
            'items': [PermisoResponseDTO.from_orm(p) for p in permisos],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @classmethod
    def actualizar_permiso(cls, db: Session, permiso_id: int, permiso_dto: PermisoCreateDTO, user_id: Optional[int] = None) -> PermisoResponseDTO:
        """Actualizar permiso"""
        permiso = db.query(Permiso).filter(Permiso.id == permiso_id, Permiso.is_active == True).first()
        if not permiso:
            raise NotFound("Permiso", permiso_id)
        
        try:
            data = permiso_dto.dict(exclude_unset=True)
            for key, value in data.items():
                setattr(permiso, key, value)
            permiso.updated_by = user_id
            db.commit()
            db.refresh(permiso)
            logger.info(f"Permiso actualizado: {permiso.nombre}")
            return PermisoResponseDTO.from_orm(permiso)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar permiso: {str(e)}")
            raise DatabaseException(f"Error al actualizar permiso: {str(e)}")
