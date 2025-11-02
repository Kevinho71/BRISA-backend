from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.usuarios.models.usuario_models import Usuario, Rol, Permiso

class UsuarioRepository:
    """Repositorio para operaciones de usuario"""
    
    @staticmethod
    def obtener_por_id(db: Session, id_usuario: int) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    @staticmethod
    def obtener_por_usuario(db: Session, usuario: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.usuario == usuario).first()
    
    @staticmethod
    def listar_todos(db: Session, skip: int = 0, limit: int = 50) -> List[Usuario]:
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_usuarios(db: Session) -> int:
        return db.query(Usuario).count()

class RolRepository:
    """Repositorio para operaciones de rol"""
    
    @staticmethod
    def obtener_por_id(db: Session, id_rol: int) -> Optional[Rol]:
        return db.query(Rol).filter(Rol.id_rol == id_rol).first()
    
    @staticmethod
    def obtener_por_nombre(db: Session, nombre: str) -> Optional[Rol]:
        return db.query(Rol).filter(Rol.nombre == nombre).first()
    
    @staticmethod
    def listar_todos(db: Session, skip: int = 0, limit: int = 50) -> List[Rol]:
        return db.query(Rol).offset(skip).limit(limit).all()

class PermisoRepository:
    """Repositorio para operaciones de permisos"""
    
    @staticmethod
    def obtener_por_id(db: Session, id_permiso: int) -> Optional[Permiso]:
        return db.query(Permiso).filter(Permiso.id_permiso == id_permiso).first()
    
    @staticmethod
    def obtener_por_nombre(db: Session, nombre: str) -> Optional[Permiso]:
        return db.query(Permiso).filter(Permiso.nombre == nombre).first()
    
    @staticmethod
    def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Permiso]:
        return db.query(Permiso).offset(skip).limit(limit).all()
