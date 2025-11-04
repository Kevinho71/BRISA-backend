"""
Modelos del Módulo de Usuarios - RF-01, RF-02, RF-03, RF-04
Gestión de Personas, Usuarios, Roles, Permisos y Bitácora de cambios
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# ================================
# Tablas de asociación Many-to-Many
# ================================

usuario_roles_table = Table(
    'usuario_roles',
    Base.metadata,
    Column('id_usuario', Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True),
    Column('id_rol', Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True),
    Column('fecha_inicio', DateTime, default=datetime.utcnow),
    Column('fecha_fin', DateTime, nullable=True),
    Column('estado', Enum('activo', 'inactivo'), default='activo'),
    extend_existing=True
)

rol_permisos_table = Table(
    'rol_permisos',
    Base.metadata,
    Column('id_rol', Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True),
    Column('id_permiso', Integer, ForeignKey('permisos.id_permiso', ondelete='CASCADE'), primary_key=True),
    Column('fecha_asignacion', DateTime, default=datetime.utcnow),
    extend_existing=True
)

# ================================
# Clases de modelos
# ================================

class Persona1(Base):
    """Modelo de Persona - Información personal de profesores y administrativos (RF-01)"""
    __tablename__ = "personas"
    __table_args__ = {"extend_existing": True}

    id_persona = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    correo = Column(String(50), unique=True, nullable=True, index=True)
    telefono = Column(String(20), nullable=True)
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
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

    def __repr__(self):
        return f"<Persona {self.nombre_completo}>"

class Usuario(Base):
    """Modelo de Usuario - Cuenta de acceso al sistema (RF-01, RF-06)"""
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona', ondelete='CASCADE'), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)


    # Relaciones
    persona = relationship("Persona1", back_populates="usuarios")
    roles = relationship("Rol", secondary=usuario_roles_table, back_populates="usuarios")
    login_logs = relationship("LoginLog", back_populates="usuario", cascade="all, delete-orphan")
    historial_roles = relationship("RolHistorial", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.usuario}>"

class Rol(Base):
    """Modelo de Rol - Define perfiles de acceso (RF-02, RF-03)"""
    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id_rol = Column(Integer, primary_key=True, index=True)
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
    __table_args__ = {"extend_existing": True}

    id_permiso = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
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
    __table_args__ = {"extend_existing": True}

    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False, index=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    estado = Column(Enum('exitoso', 'fallido'), default='exitoso')

    # Relaciones
    usuario = relationship("Usuario", back_populates="login_logs")

    def __repr__(self):
        return f"<LoginLog usuario_id={self.id_usuario}>"

class RolHistorial(Base):
    """Modelo de RolHistorial - Historial de asignación de roles a usuarios (RF-02)"""
    __tablename__ = "rol_historial"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False, index=True)
    id_rol = Column(Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), nullable=False, index=True)
    accion = Column(Enum('asignado', 'revocado'), nullable=False)
    razon = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="historial_roles")

    def __repr__(self):
        return f"<RolHistorial usuario_id={self.id_usuario} accion={self.accion}>"

class Bitacora(Base):
    """Modelo de Bitacora - Registro de acciones administrativas"""
    __tablename__ = "bitacora"
    __table_args__ = {"extend_existing": True}

    id_bitacora = Column(Integer, primary_key=True, index=True)
    id_usuario_admin = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    accion = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    id_objetivo = Column(Integer, nullable=True)
    tipo_objetivo = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Bitacora admin_id={self.id_usuario_admin} accion={self.accion}>"
