"""
app/modules/usuarios/dto/usuario_dto.py - COMPLETO Y CORREGIDO
DTOs del Módulo de Usuarios - Validación de datos de entrada/salida
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, date


# ==================== PERSONA DTOs ====================

class PersonaCreateDTO(BaseModel):
    """DTO para crear persona (RF-01)"""
    ci: str = Field(..., min_length=7, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=50)
    apellido_paterno: str = Field(..., min_length=2, max_length=50)
    apellido_materno: str = Field(..., min_length=2, max_length=50)
    direccion: Optional[str] = None
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    tipo_persona: str = Field(..., pattern="^(profesor|administrativo)$")


class PersonaUpdateDTO(BaseModel):
    """DTO para actualizar persona (RF-01)"""
    ci: Optional[str] = Field(None, min_length=7, max_length=20)
    nombres: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido_paterno: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido_materno: Optional[str] = Field(None, min_length=2, max_length=50)
    direccion: Optional[str] = None
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    tipo_persona: Optional[str] = Field(None, pattern="^(profesor|administrativo)$")


class PersonaResponseDTO(BaseModel):
    """DTO para respuesta de persona"""
    id_persona: int
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    direccion: Optional[str]
    telefono: Optional[str]
    correo: Optional[str]
    tipo_persona: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ==================== USUARIO DTOs ====================

class UsuarioCreateDTO(BaseModel):
    """
    DTO para crear usuario (RF-01)
    Se usa en endpoints internos que requieren id_persona
    """
    id_persona: int
    usuario: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validación completa de contraseña"""
        if len(v) < 8:
            raise ValueError('Contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Contraseña debe contener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Contraseña debe contener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Contraseña debe contener al menos un número')
        return v


class UsuarioUpdateDTO(BaseModel):
    """DTO para actualizar usuario (RF-06)"""
    usuario: Optional[str] = Field(None, min_length=3, max_length=50)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validación de contraseña si se proporciona"""
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Contraseña debe contener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Contraseña debe contener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Contraseña debe contener al menos un número')
        return v


class UsuarioResponseDTO(BaseModel):
    """
    DTO para respuesta de usuario
    ⚠️ CRÍTICO: NUNCA exponer password
    """
    id_usuario: int
    id_persona: int
    usuario: str
    correo: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


# ==================== ROL DTOs ====================

class RolCreateDTO(BaseModel):
    """DTO para crear rol (RF-03)"""
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class RolUpdateDTO(BaseModel):
    """DTO para actualizar rol (RF-03)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class PermisoResponseDTO(BaseModel):
    """DTO para respuesta de permiso"""
    id_permiso: int
    nombre: str
    descripcion: Optional[str] = None
    modulo: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class RolResponseDTO(BaseModel):
    """DTO para respuesta de rol"""
    id_rol: int
    nombre: str
    descripcion: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    permisos: List[PermisoResponseDTO] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# ==================== PERMISO DTOs ====================

class PermisoCreateDTO(BaseModel):
    """DTO para crear permiso (RF-04)"""
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)
    modulo: str = Field(..., min_length=2, max_length=50)


# ==================== OTROS DTOs ====================

class AsignarRolDTO(BaseModel):
    """DTO para asignar rol a usuario (RF-02)"""
    id_rol: int
    razon: Optional[str] = Field(None, max_length=255)
    estado: str = Field(default="activo", pattern="^(activo|inactivo)$")


class LoginDTO(BaseModel):
    """DTO para login"""
    usuario: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class TokenResponseDTO(BaseModel):
    """DTO para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hora por defecto


class PaginatedResponseDTO(BaseModel):
    """DTO para respuestas paginadas"""
    items: List = []
    total: int = 0
    page: int = 1
    per_page: int = 50
    pages: int = 1

    @classmethod
    def create(cls, items: List, total: int, page: int, per_page: int):
        """Helper para crear respuesta paginada"""
        import math
        pages = math.ceil(total / per_page) if per_page > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages
        )


# Resolver referencias circulares
RolResponseDTO.model_rebuild()
PermisoResponseDTO.model_rebuild()
