from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.usuarios.models.usuario_models import Usuario, Rol, Permiso, Persona1
from sqlalchemy import or_

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

class PersonaRepository:
    """Repositorio para operaciones de personas"""
    
    @staticmethod
    def obtener_por_id(db: Session, persona_id: int) -> Optional[Persona1]:
        """Obtener persona por ID"""
        return db.query(Persona1).filter(
            Persona1.id_persona == persona_id
        ).first()
    
    @staticmethod
    def obtener_por_ci(db: Session, ci: str) -> Optional[Persona1]:
        """Obtener persona por CI"""
        return db.query(Persona1).filter(
            Persona1.ci == ci
        ).first()
    
    @staticmethod
    def obtener_por_correo(db: Session, correo: str) -> Optional[Persona1]:
        """Obtener persona por correo"""
        return db.query(Persona1).filter(
            Persona1.correo == correo
        ).first()
    
    @staticmethod
    def listar_todas(
        db: Session,
        skip: int = 0,
        limit: int = 10000
    ) -> List[Persona1]:
        """
        Listar todas las personas ordenadas
        
        Args:
            db: Sesión de base de datos
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            Lista de personas ordenadas por apellido y nombre
        """
        return db.query(Persona1).order_by(
            Persona1.apellido_paterno,
            Persona1.nombres
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def listar_con_filtros(
        db: Session,
        skip: int = 0,
        limit: int = 10000,
        tipo_persona: Optional[str] = None,
        busqueda: Optional[str] = None,
        estado: Optional[str] = None
    ) -> List[Persona1]:
        """
        Listar personas con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Registros a saltar
            limit: Límite de registros
            tipo_persona: 'profesor' o 'administrativo'
            busqueda: Búsqueda en nombres, CI, correo, teléfono
            estado: 'activo' o 'inactivo'
            
        Returns:
            Lista de personas filtradas
        """
        query = db.query(Persona1)
        
        # Filtro por tipo de persona
        if tipo_persona:
            query = query.filter(Persona1.tipo_persona == tipo_persona.lower())
        
        # Filtro por estado
        if estado:
            if estado.lower() == 'activo':
                query = query.filter(Persona1.is_active == True)
            elif estado.lower() == 'inactivo':
                query = query.filter(Persona1.is_active == False)
        
        # Filtro por búsqueda (múltiples campos)
        if busqueda:
            busqueda_lower = f"%{busqueda.lower()}%"
            query = query.filter(
                or_(
                    Persona1.nombres.ilike(busqueda_lower),
                    Persona1.apellido_paterno.ilike(busqueda_lower),
                    Persona1.apellido_materno.ilike(busqueda_lower),
                    Persona1.ci.ilike(busqueda_lower),
                    Persona1.correo.ilike(busqueda_lower),
                    Persona1.telefono.ilike(busqueda_lower)
                )
            )
        
        # Ordenar por apellido y nombre
        query = query.order_by(
            Persona1.apellido_paterno,
            Persona1.nombres
        )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def contar_total(db: Session) -> int:
        """Contar total de personas"""
        return db.query(Persona1).count()
    
    @staticmethod
    def contar_con_filtros(
        db: Session,
        tipo_persona: Optional[str] = None,
        busqueda: Optional[str] = None,
        estado: Optional[str] = None
    ) -> int:
        """Contar personas con filtros"""
        query = db.query(Persona1)
        
        if tipo_persona:
            query = query.filter(Persona1.tipo_persona == tipo_persona.lower())
        
        if estado:
            if estado.lower() == 'activo':
                query = query.filter(Persona1.is_active == True)
            elif estado.lower() == 'inactivo':
                query = query.filter(Persona1.is_active == False)
        
        if busqueda:
            busqueda_lower = f"%{busqueda.lower()}%"
            query = query.filter(
                or_(
                    Persona1.nombres.ilike(busqueda_lower),
                    Persona1.apellido_paterno.ilike(busqueda_lower),
                    Persona1.apellido_materno.ilike(busqueda_lower),
                    Persona1.ci.ilike(busqueda_lower),
                    Persona1.correo.ilike(busqueda_lower),
                    Persona1.telefono.ilike(busqueda_lower)
                )
            )
        
        return query.count()
    
    @staticmethod
    def listar_por_tipo(
        db: Session,
        tipo_persona: str,
        skip: int = 0,
        limit: int = 10000
    ) -> List[Persona1]:
        """Listar personas por tipo específico"""
        return db.query(Persona1).filter(
            Persona1.tipo_persona == tipo_persona.lower()
        ).order_by(
            Persona1.apellido_paterno,
            Persona1.nombres
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def listar_activas(db: Session) -> List[Persona1]:
        """Listar solo personas activas"""
        return db.query(Persona1).filter(
            Persona1.is_active == True
        ).order_by(
            Persona1.apellido_paterno,
            Persona1.nombres
        ).all()
    
    @staticmethod
    def listar_inactivas(db: Session) -> List[Persona1]:
        """Listar solo personas inactivas"""
        return db.query(Persona1).filter(
            Persona1.is_active == False
        ).order_by(
            Persona1.apellido_paterno,
            Persona1.nombres
        ).all()