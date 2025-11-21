"app/module/auth/dto/auth_dto"

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from app.core.database import Base
from typing import TYPE_CHECKING

# ==========================
# DTO para Roles
# ==========================
class RolDTO(BaseModel):
    id_rol: int
    nombre: str

# ==========================
# DTO para Registro de Usuario
# ==========================
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
    tipo_persona: Literal["profesor", "administrativo"] = "administrativo"
    id_rol: Optional[int] = None  # ID del rol a asignar al usuario
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validar complejidad de contraseña"""
        if len(v) < 8:
            raise ValueError('Contraseña debe tener mínimo 8 caracteres')
        if len(v) > 72:
            raise ValueError('Contraseña no puede exceder 72 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Contraseña debe contener mayúsculas')
        if not any(c.islower() for c in v):
            raise ValueError('Contraseña debe contener minúsculas')
        if not any(c.isdigit() for c in v):
            raise ValueError('Contraseña debe contener números')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "ci": "1234567890",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "apellido_materno": "García",
                "usuario": "jperez",
                "correo": "jperez@example.com",
                "password": "Password123!",
                "telefono": "+34-555-123456",
                "direccion": "Calle Falsa 123",
                "tipo_persona": "profesor",
                "id_rol": 1
            }
        }
    }

# ==========================
# DTO para Login
# ==========================
class LoginDTO(BaseModel):
    """DTO para inicio de sesión"""
    usuario: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "usuario": "jperez",
                "password": "Password123!"
            }
        }
    }

# ==========================
# DTO para Token JWT
# ==========================
class TokenDTO(BaseModel):
    """DTO para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    usuario: str
    nombres: str
    rol: str
    permisos: List[str]
    expires_in: int
    
    model_config = {
        "json_schema_extra": {
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
    }

# ==========================
# DTO para Usuario Actual
# ==========================
class UsuarioActualDTO(BaseModel):
    """DTO para información del usuario actual"""
    id_usuario: int
    id_persona: int
    usuario: str
    correo: EmailStr
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    ci: str
    roles: List[RolDTO]
    permisos: List[str]
    estado: Literal["activo", "inactivo"]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_usuario": 1,
                "id_persona": 10,
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
    }


if TYPE_CHECKING:
    from app.modules.usuarios.dto.usuario_dto import UsuarioResponseDTO


class TokenResponseDTO(BaseModel):
    """DTO para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    usuario: "UsuarioResponseDTO"
