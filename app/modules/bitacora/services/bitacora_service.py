"""
app/modules/bitacora/services/bitacora_service.py
✅ FIX: Importar Bitacora desde usuario_models
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
import logging

# ✅ IMPORTAR DESDE USUARIO_MODELS
from app.modules.usuarios.models.usuario_models import Bitacora, Usuario

logger = logging.getLogger(__name__)

class BitacoraService:
    """Servicio para consultas de bitácora (RF-08)"""
    
    @staticmethod
    def obtener_registros_bitacora(
        db: Session,
        usuario_admin: Optional[int] = None,
        accion: Optional[str] = None,
        tipo_objetivo: Optional[str] = None,
        id_objetivo: Optional[int] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Bitacora], int]:
        """
        Obtener registros de bitácora con filtros (RF-08)
        Retorna tupla (registros, total)
        """
        query = db.query(Bitacora)
        
        # Aplicar filtros
        if usuario_admin:
            query = query.filter(Bitacora.id_usuario_admin == usuario_admin)
        
        if accion:
            query = query.filter(Bitacora.accion.ilike(f"%{accion}%"))
        
        if tipo_objetivo:
            query = query.filter(Bitacora.tipo_objetivo == tipo_objetivo)
        
        if id_objetivo:
            query = query.filter(Bitacora.id_objetivo == id_objetivo)
        
        if fecha_inicio and fecha_fin:
            query = query.filter(
                and_(
                    Bitacora.fecha_hora >= fecha_inicio,
                    Bitacora.fecha_hora <= fecha_fin
                )
            )
        elif fecha_inicio:
            query = query.filter(Bitacora.fecha_hora >= fecha_inicio)
        elif fecha_fin:
            query = query.filter(Bitacora.fecha_hora <= fecha_fin)
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación y ordenar por fecha descendente
        registros = query.order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()
        
        return registros, total
    
    @staticmethod
    def obtener_bitacora_usuario(
        db: Session,
        id_usuario: int,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Bitacora], int]:
        """Obtener bitácora de un usuario específico"""
        query = db.query(Bitacora).filter(Bitacora.id_usuario_admin == id_usuario)
        
        total = query.count()
        registros = query.order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()
        
        return registros, total
    
    @staticmethod
    def obtener_bitacora_por_tipo(
        db: Session,
        tipo_objetivo: str,
        id_objetivo: int,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Bitacora], int]:
        """Obtener bitácora de un objeto específico (usuario, rol, etc)"""
        query = db.query(Bitacora).filter(
            and_(
                Bitacora.tipo_objetivo == tipo_objetivo,
                Bitacora.id_objetivo == id_objetivo
            )
        )
        
        total = query.count()
        registros = query.order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()
        
        return registros, total
    
    @staticmethod
    def obtener_estadisticas_bitacora(db: Session, fecha_inicio: Optional[datetime] = None) -> dict:
        """Obtener estadísticas de bitácora"""
        query = db.query(Bitacora)
        
        if fecha_inicio:
            query = query.filter(Bitacora.fecha_hora >= fecha_inicio)
        
        total_registros = query.count()
        
        # Acciones más comunes
        acciones_comunes = db.query(
            Bitacora.accion,
            db.func.count(Bitacora.id_bitacora).label('cantidad')
        ).filter(Bitacora.fecha_hora >= fecha_inicio if fecha_inicio else True).group_by(
            Bitacora.accion
        ).order_by(db.func.count(Bitacora.id_bitacora).desc()).limit(10).all()
        
        # Usuarios más activos
        usuarios_activos = db.query(
            Usuario.usuario,
            db.func.count(Bitacora.id_bitacora).label('cantidad')
        ).join(Bitacora, Bitacora.id_usuario_admin == Usuario.id_usuario).filter(
            Bitacora.fecha_hora >= fecha_inicio if fecha_inicio else True
        ).group_by(Usuario.usuario).order_by(db.func.count(Bitacora.id_bitacora).desc()).limit(10).all()
        
        return {
            "total_registros": total_registros,
            "acciones_comunes": [{"accion": a[0], "cantidad": a[1]} for a in acciones_comunes],
            "usuarios_activos": [{"usuario": u[0], "cantidad": u[1]} for u in usuarios_activos]
        }
    
    @staticmethod
    def obtener_resumen_por_fecha(db: Session, tipo: str = 'dia') -> dict:
        """
        Obtener resumen de actividades por fecha
        tipo: 'dia', 'semana', 'mes'
        """
        from datetime import timedelta, date
        
        if tipo == 'dia':
            fecha_limite = datetime.utcnow() - timedelta(days=1)
        elif tipo == 'semana':
            fecha_limite = datetime.utcnow() - timedelta(weeks=1)
        else:  # mes
            fecha_limite = datetime.utcnow() - timedelta(days=30)
        
        registros = db.query(
            db.func.date(Bitacora.fecha_hora).label('fecha'),
            db.func.count(Bitacora.id_bitacora).label('cantidad')
        ).filter(
            Bitacora.fecha_hora >= fecha_limite
        ).group_by(
            db.func.date(Bitacora.fecha_hora)
        ).order_by(
            db.func.date(Bitacora.fecha_hora).desc()
        ).all()
        
        return {
            "tipo": tipo,
            "resumen": [{"fecha": str(r[0]), "cantidad": r[1]} for r in registros]
        }