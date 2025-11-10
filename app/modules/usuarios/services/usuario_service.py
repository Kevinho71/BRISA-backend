"""
app/modules/usuarios/services/usuario_service.py - CORREGIDO
Servicios del Módulo de Usuarios - FINAL
"""
from sqlalchemy.orm import Session
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
    PermisoCreateDTO, PermisoResponseDTO,
    AsignarRolDTO
)
from app.shared.services.base_services import BaseService
from app.shared.exceptions.custom_exceptions import NotFound, Conflict, ValidationException, DatabaseException
from app.shared.security import hash_password, verify_password
from app.shared.permission_mapper import puede_modificar_usuario

from app.shared.decorators.auth_decorators import (
    verificar_permiso, 
    validar_puede_modificar_usuario
)

logger = logging.getLogger(__name__)


class PersonaService(BaseService):
    """Servicio de gestión de personas (RF-01)"""
    model_class = Persona1
    
    @classmethod
    def crear_persona(cls, db: Session, persona_dto: PersonaCreateDTO, user_id: Optional[int] = None) -> PersonaResponseDTO:
        """Crear nueva persona"""
        persona_existente = db.query(Persona1).filter(Persona1.ci == persona_dto.ci).first()
        if persona_existente:
            raise Conflict(f"CI {persona_dto.ci} ya registrado")
        
        try:
            data = persona_dto.dict(exclude_unset=True)
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
        persona = db.query(Persona1).filter(
            Persona1.id_persona == persona_id, 
            Persona1.is_active == True
        ).first()
        if not persona:
            raise NotFound("Persona", persona_id)
        return PersonaResponseDTO.from_orm(persona)


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
    """Servicio de gestión de roles (RF-02, RF-03, RF-04) - CORREGIDO"""
    
    model_class = Rol
    
    @classmethod
    def crear_rol(cls, db: Session, rol_dto: RolCreateDTO, current_user: Usuario = None) -> RolResponseDTO:
        """✅ CORREGIDO: Crear nuevo rol con validación de permisos"""
        if current_user:
            from app.shared.permissions import check_permission
            if not check_permission(current_user, 'crear_rol'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para crear roles"
                )
        
        # ✅ Verificar duplicado ANTES del try
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
        rol = db.query(Rol).filter(
            Rol.id_rol == rol_id, 
            Rol.is_active == True
        ).first()
        if not rol:
            raise NotFound("Rol", rol_id)
        return RolResponseDTO.from_orm(rol)
    
    @classmethod
    def listar_roles(cls, db: Session, skip: int = 0, limit: int = 50):
        """Listar roles con paginación"""
        roles = db.query(Rol).filter(Rol.is_active == True).offset(skip).limit(limit).all()
        return [RolResponseDTO.from_orm(r) for r in roles]
    
    @classmethod
    def actualizar_rol(cls, db: Session, rol_id: int, rol_dto: RolUpdateDTO, current_user: Usuario = None) -> RolResponseDTO:
        """✅ CORREGIDO: Actualizar rol"""
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
            data = rol_dto.dict(exclude_unset=True)
            for key, value in data.items():
                if value is not None:
                    setattr(rol, key, value)
            
            if current_user:
                rol.updated_by = current_user.id_usuario
            
            db.commit()
            db.refresh(rol)
            logger.info(f"Rol actualizado: {rol.nombre}")
            return RolResponseDTO.from_orm(rol)
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar rol: {str(e)}")
            raise DatabaseException(f"Error al actualizar rol: {str(e)}")
    
    @classmethod
    def eliminar_rol(cls, db: Session, rol_id: int, current_user: Usuario = None) -> dict:
        """✅ CORREGIDO: Eliminar rol (borrado lógico)"""
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
        
        try:
            rol.is_active = False
            if current_user:
                rol.updated_by = current_user.id_usuario
            
            db.commit()
            logger.info(f"Rol eliminado: ID {rol_id}")
            return {"mensaje": "Rol eliminado exitosamente"}
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
        """✅ CORREGIDO: Asignar permisos a rol (RF-04)"""
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
            permisos = db.query(Permiso).filter(
                Permiso.id_permiso.in_(permisos_ids), 
                Permiso.is_active == True
            ).all()
            
            if len(permisos) != len(permisos_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Algunos permisos no existen o están inactivos"
                )
            
            rol.permisos = permisos
            
            if current_user:
                rol.updated_by = current_user.id_usuario
            
            db.commit()
            db.refresh(rol)
            
            logger.info(f"Permisos asignados al rol {rol_id}")
            return RolResponseDTO.from_orm(rol)
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
        """✅ CORREGIDO: Asignar rol a usuario"""
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
        """✅ CORREGIDO: Remover rol de un usuario"""
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