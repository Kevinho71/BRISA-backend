from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class RegistroDTO(BaseModel):
    """DTO para registro de nuevo usuario"""
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    usuario: str
    correo: EmailStr
    password: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    tipo_persona: str = "administrativo"  # profesor o administrativo
    id_rol: Optional[int] = None  # ID del rol a asignar
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validar complejidad de contraseña"""
        if len(v) < 8:
            raise ValueError('Contraseña debe tener mínimo 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Contraseña debe contener mayúsculas')
        if not any(c.islower() for c in v):
            raise ValueError('Contraseña debe contener minúsculas')
        if not any(c.isdigit() for c in v):
            raise ValueError('Contraseña debe contener números')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "ci": "1234567890",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "apellido_materno": "García",
                "usuario": "jperez",
                "correo": "jperez@example.com",
                "password": "Password123!",
                "telefono": "+34-555-123456",
                "tipo_persona": "profesor",
                "id_rol": 1
            }
        }

class LoginDTO(BaseModel):
    """DTO para inicio de sesión"""
    usuario: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "usuario": "jperez",
                "password": "Password123!"
            }
        }

class TokenDTO(BaseModel):
    """DTO para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    usuario: str
    nombres: str
    rol: str
    permisos: list[str]
    expires_in: int
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "usuario_id": 1,
                "usuario": "jperez",
                "nombres": "Juan Pérez",
                "rol": "Profesor",
                "permisos": ["ver_usuario", "generar_reportes"],
                "expires_in": 1800
            }
        }

class UsuarioActualDTO(BaseModel):
    """DTO para información del usuario actual"""
    id_usuario: int
    usuario: str
    correo: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    ci: str
    roles: list[dict]
    permisos: list[str]
    estado: str
    
    class Config:
        schema_extra = {
            "example": {
                "id_usuario": 1,
                "usuario": "jperez",
                "correo": "jperez@example.com",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "apellido_materno": "García",
                "ci": "1234567890",
                "roles": [{"id_rol": 1, "nombre": "Profesor"}],
                "permisos": ["ver_usuario", "generar_reportes"],
                "estado": "activo"
            }
        }
