from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.modules.usuarios.models.usuario_models import Bitacora

class BitacoraRepository:
    """Repositorio para operaciones de bitácora"""
    
    @staticmethod
    def registrar_accion(
        db: Session,
        id_usuario_admin: int,
        accion: str,
        descripcion: str,
        id_objetivo: Optional[int] = None,
        tipo_objetivo: Optional[str] = None,
        estado_anterior: Optional[dict] = None,
        estado_nuevo: Optional[dict] = None,
        ip_address: Optional[str] = None
    ) -> Bitacora:
        """Registrar una acción en la bitácora"""
        bitacora = Bitacora(
            id_usuario_admin=id_usuario_admin,
            accion=accion,
            descripcion=descripcion,
            id_objetivo=id_objetivo,
            tipo_objetivo=tipo_objetivo,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            ip_address=ip_address,
            fecha_hora=datetime.utcnow()
        )
        db.add(bitacora)
        db.commit()
        return bitacora
    
    @staticmethod
    def obtener_por_id(db: Session, id_bitacora: int) -> Optional[Bitacora]:
        return db.query(Bitacora).filter(Bitacora.id_bitacora == id_bitacora).first()
    
    @staticmethod
    def listar_por_usuario(db: Session, id_usuario: int, skip: int = 0, limit: int = 50) -> List[Bitacora]:
        return db.query(Bitacora).filter(
            Bitacora.id_usuario_admin == id_usuario
        ).order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def listar_por_accion(db: Session, accion: str, skip: int = 0, limit: int = 50) -> List[Bitacora]:
        return db.query(Bitacora).filter(
            Bitacora.accion == accion
        ).order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_registros(db: Session) -> int:
        return db.query(Bitacora).count()
