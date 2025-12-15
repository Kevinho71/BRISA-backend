"""
app/modules/usuarios/models/usuario_models.py
"""
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, ForeignKey, Table, Text, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# ================================
# Tablas Many-to-Many
# ================================

usuario_roles_table = Table(
    'usuario_roles',
    Base.metadata,
    Column('id_usuario', Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True),
    Column('id_rol', Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True),
    Column('fecha_inicio', DateTime, default=datetime.utcnow),
    Column('fecha_fin', DateTime, nullable=True),
    Column('estado', Enum('activo', 'inactivo', name='estado_usuario_rol'), default='activo'),
    extend_existing=True
)

rol_permisos_table = Table(
    'rol_permisos',
    Base.metadata,
    Column('id_rol', Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True),
    Column('id_permiso', Integer, ForeignKey('permisos.id_permiso', ondelete='CASCADE'), primary_key=True),
    # ELIMINADO: fecha_asignacion - no existe en tu BD
    extend_existing=True
)

# ================================
# Clases de modelos
# ================================

class Persona1(Base):
    """Persona - RF-01"""
    __tablename__ = "personas"
    __table_args__ = {'extend_existing': True}

    id_persona = Column(Integer, primary_key=True, autoincrement=True)
    ci = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    correo = Column(String(50), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    tipo_persona = Column(Enum('profesor', 'administrativo', 'apoderado', name='tipo_persona_enum'), nullable=False)
    is_active = Column(Boolean, default=True)
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

    def __repr__(self):
        return f"<Persona {self.nombre_completo}>"
    
    


class Usuario(Base):
    """Usuario - RF-01, RF-06"""
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona', ondelete='CASCADE'), nullable=False, index=True)
    usuario = Column(String(50), unique=True, nullable=False, index=True)
    correo = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    

    persona = relationship(
        "Persona1",
        foreign_keys=[id_persona],
        uselist=False,
        viewonly=True
    )
    
    roles = relationship("Rol", secondary=usuario_roles_table, back_populates="usuarios")
    login_logs = relationship("LoginLog", back_populates="usuario", cascade="all, delete-orphan")
    historial_roles = relationship("RolHistorial", back_populates="usuario", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Usuario {self.usuario}>"


class Rol(Base):
    """Rol - RF-02, RF-03"""
    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    usuarios = relationship("Usuario", secondary=usuario_roles_table, back_populates="roles")
    permisos = relationship("Permiso", secondary=rol_permisos_table, back_populates="roles")

    def __repr__(self):
        return f"<Rol {self.nombre}>"


class Permiso(Base):
    """Permiso - RF-04"""
    __tablename__ = "permisos"
    __table_args__ = {'extend_existing': True}

    id_permiso = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    modulo = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    roles = relationship("Rol", secondary=rol_permisos_table, back_populates="permisos")

    def __repr__(self):
        return f"<Permiso {self.nombre}>"


class LoginLog(Base):
    """LoginLog - RF-08"""
    __tablename__ = "login_logs"
    __table_args__ = {'extend_existing': True}

    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    estado = Column(Enum('exitoso', 'fallido', name='estado_login'), default='exitoso')

    usuario = relationship("Usuario", back_populates="login_logs")

    def __repr__(self):
        return f"<LoginLog usuario_id={self.id_usuario}>"


class RolHistorial(Base):
    """Historial de roles - RF-02"""
    __tablename__ = "rol_historial"
    __table_args__ = {'extend_existing': True}

    
    id_historial = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    id_rol = Column(Integer, ForeignKey('roles.id_rol', ondelete='CASCADE'), nullable=False)
    accion = Column(Enum('asignado', 'revocado', name='accion_rol'), nullable=False)
    razon = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)

    usuario = relationship("Usuario", back_populates="historial_roles")

    def __repr__(self):
        return f"<RolHistorial usuario_id={self.id_usuario} accion={self.accion}>"


class Bitacora(Base):
    """Bitacora - Auditoría"""
    __tablename__ = "bitacora"
    __table_args__ = {'extend_existing': True}

    id_bitacora = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario_admin = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    accion = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    id_objetivo = Column(Integer, nullable=True)
    tipo_objetivo = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Bitacora admin_id={self.id_usuario_admin} accion={self.accion}>"