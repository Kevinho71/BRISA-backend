from sqlalchemy.orm import Session
from app.modules.usuarios.models.usuario_models import Usuario, Persona1, LoginLog
from typing import Optional

class AuthRepository:
    """Repositorio para operaciones de autenticación"""
    
    @staticmethod
    def buscar_usuario_por_nombre(db: Session, usuario: str) -> Optional[Usuario]:
        """Buscar usuario por nombre de usuario"""
        return db.query(Usuario).filter(Usuario.usuario == usuario).first()
    
    @staticmethod
    def buscar_usuario_por_correo(db: Session, correo: str) -> Optional[Usuario]:
        """Buscar usuario por correo"""
        return db.query(Usuario).filter(Usuario.correo == correo).first()
    
    @staticmethod
    def buscar_persona_por_ci(db: Session, ci: str) -> Optional[Persona1]:
        """Buscar persona por CI"""
        return db.query(Persona1).filter(Persona1.ci == ci).first()
    
    @staticmethod
    def registrar_login(db: Session, id_usuario: int, ip_address: str = None, estado: str = 'exitoso'):
        """Registrar intento de login"""
        login_log = LoginLog(
            id_usuario=id_usuario,
            ip_address=ip_address,
            estado_login=estado
        )
        db.add(login_log)
        db.commit()
        return login_log
