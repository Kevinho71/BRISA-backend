"""
DTOs del Módulo de Usuarios - Validación de datos de entrada/salida
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime, date

class PersonaCreateDTO(BaseModel):
    """DTO para crear persona (RF-01)"""
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    cedula: str = Field(..., min_length=7, max_length=20)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=15)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    tipo_persona: str = Field(..., pattern="^(profesor|administrativo)$")

class PersonaUpdateDTO(BaseModel):
    """DTO para actualizar persona (RF-01)"""
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=15)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None

class PersonaResponseDTO(BaseModel):
    """DTO para respuesta de persona"""
    id: int
    nombres: str
    apellidos: str
    cedula: str
    email: Optional[str]
    telefono: Optional[str]
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]
    tipo_persona: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class UsuarioCreateDTO(BaseModel):
    """DTO para crear usuario (RF-01)"""
    id_persona: int
    correo: EmailStr
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Contraseña debe contener al menos una mayúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Contraseña debe contener al menos un número')
        return v

class UsuarioUpdateDTO(BaseModel):
    """DTO para actualizar usuario (RF-06)"""
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class UsuarioResponseDTO(BaseModel):
    """DTO para respuesta de usuario"""
    id: int
    id_persona: int
    correo: str
    ultimo_acceso: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    roles: List['RolResponseDTO'] = []
    
    class Config:
        from_attributes = True

class RolCreateDTO(BaseModel):
    """DTO para crear rol (RF-03)"""
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)

class RolUpdateDTO(BaseModel):
    """DTO para actualizar rol (RF-03)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)

class RolResponseDTO(BaseModel):
    """DTO para respuesta de rol"""
    id: int
    nombre: str
    descripcion: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    permisos: List['PermisoResponseDTO'] = []
    
    class Config:
        from_attributes = True

class PermisoCreateDTO(BaseModel):
    """DTO para crear permiso (RF-04)"""
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    modulo: str = Field(..., min_length=2, max_length=50)

class PermisoResponseDTO(BaseModel):
    """DTO para respuesta de permiso"""
    id: int
    nombre: str
    descripcion: Optional[str]
    modulo: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AsignarRolDTO(BaseModel):
    """DTO para asignar rol a usuario (RF-02)"""
    id_rol: int
    razon: Optional[str] = None

class LoginDTO(BaseModel):
    """DTO para login"""
    correo: EmailStr
    password: str

class TokenResponseDTO(BaseModel):
    """DTO para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponseDTO

class PaginatedResponseDTO(BaseModel):
    """DTO para respuestas paginadas"""
    items: List = []
    total: int
    page: int
    per_page: int
    pages: int
