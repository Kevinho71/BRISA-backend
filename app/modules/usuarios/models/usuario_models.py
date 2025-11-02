"""
Modelos del Módulo de Usuarios - RF-01, RF-02, RF-03, RF-04
Gestión de Personas, Usuarios, Roles, Permisos y Auditoría de cambios
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table, Text, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config import Base

# Tabla de asociación para Many-to-Many: usuario_roles
usuario_roles_table = Table(
    'usuario_roles',
    Base.metadata,
    Column('id_usuario', Integer, ForeignKey('usuarios.id'), ondelete='CASCADE', primary_key=True),
    Column('id_rol', Integer, ForeignKey('roles.id'), ondelete='CASCADE', primary_key=True),
    Column('fecha_asignacion', DateTime, default=datetime.utcnow)
)

# Tabla de asociación para Many-to-Many: rol_permisos
rol_permisos_table = Table(
    'rol_permisos',
    Base.metadata,
    Column('id_rol', Integer, ForeignKey('roles.id'), ondelete='CASCADE', primary_key=True),
    Column('id_permiso', Integer, ForeignKey('permisos.id'), ondelete='CASCADE', primary_key=True),
    Column('fecha_asignacion', DateTime, default=datetime.utcnow)
)

class Persona(Base):
    """Modelo de Persona - Información personal de profesores y administrativos (RF-01)"""
    __tablename__ = "personas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=True, index=True)
    telefono = Column(String(15), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(Text, nullable=True)
    tipo_persona = Column(Enum('profesor', 'administrativo'), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="persona", cascade="all, delete-orphan")
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    def __repr__(self):
        return f"<Persona {self.nombre_completo}>"

class Usuario(Base):
    """Modelo de Usuario - Cuenta de acceso al sistema (RF-01, RF-06)"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey('personas.id'), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    ultimo_acceso = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Relaciones
    persona = relationship("Persona", back_populates="usuarios")
    roles = relationship("Rol", secondary=usuario_roles_table, back_populates="usuarios")
    login_logs = relationship("LoginLog", back_populates="usuario", cascade="all, delete-orphan")
    historial_roles = relationship("RolHistorial", back_populates="usuario", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Usuario {self.correo}>"

class Rol(Base):
    """Modelo de Rol - Define perfiles de acceso (RF-02, RF-03)"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Relaciones
    usuarios = relationship("Usuario", secondary=usuario_roles_table, back_populates="roles")
    permisos = relationship("Permiso", secondary=rol_permisos_table, back_populates="roles")
    
    def __repr__(self):
        return f"<Rol {self.nombre}>"

class Permiso(Base):
    """Modelo de Permiso - Acciones permitidas en el sistema (RF-04)"""
    __tablename__ = "permisos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    modulo = Column(String(50), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Relaciones
    roles = relationship("Rol", secondary=rol_permisos_table, back_populates="permisos")
    
    def __repr__(self):
        return f"<Permiso {self.nombre}>"

class LoginLog(Base):
    """Modelo de LoginLog - Registro de inicios de sesión (RF-08)"""
    __tablename__ = "login_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    estado = Column(Enum('exitoso', 'fallido'), default='exitoso')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="login_logs")
    
    def __repr__(self):
        return f"<LoginLog usuario_id={self.id_usuario}>"

class RolHistorial(Base):
    """Modelo de RolHistorial - Historial de asignación de roles a usuarios (RF-02)"""
    __tablename__ = "rol_historial"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False, index=True)
    id_rol = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    accion = Column(Enum('asignado', 'revocado'), nullable=False)
    razon = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="historial_roles")
    
    def __repr__(self):
        return f"<RolHistorial usuario_id={self.id_usuario} accion={self.accion}>"
