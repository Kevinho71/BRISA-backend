"""
app/modules/auth/dto/auth_dto.py - Mejorado
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Literal
from datetime import datetime
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
    tipo_persona: str = "administrativo"
    id_rol: Optional[int] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """
        Validar complejidad de contraseña.
        Usa la función mejorada de security.py que maneja
        contraseñas largas automáticamente.
        """
        from app.shared.security import validate_password_strength
        
        # Usar la validación robusta
        es_valida, errores = validate_password_strength(v)
        
        if not es_valida:
            # Unir todos los errores en un mensaje
            raise ValueError("; ".join(errores))
        
        return v

    @field_validator('tipo_persona')
    @classmethod
    def validate_tipo_persona(cls, v: str):
        """✅ Valida tipo_persona - SOLO profesor o administrativo"""
        tipos_validos = ['profesor', 'administrativo']
        v_limpio = v.strip().lower()
        
        if v_limpio not in tipos_validos:
            raise ValueError(
                f"tipo_persona inválido: '{v}'. "
                f"Solo se permite 'profesor' o 'administrativo'"
            )
        
        return v_limpio
    
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

# ==========================
# DTO para cambiar contraseña
# ==========================
class CambiarPasswordDTO(BaseModel):
    """
    DTO para cambio de contraseña del usuario
    El usuario debe proporcionar su contraseña actual para seguridad
    """
    password_actual: str
    password_nueva: str
    confirmar_password_nueva: str
    
    @field_validator('password_nueva')
    @classmethod
    def validate_password_nueva(cls, v, info):
        """Validar que la nueva contraseña cumpla requisitos de seguridad"""
        from app.shared.security import validate_password_strength
        
        es_valida, errores = validate_password_strength(v)
        
        if not es_valida:
            raise ValueError("; ".join(errores))
        
        # Validar que no sea igual a la actual
        if 'password_actual' in info.data and v == info.data['password_actual']:
            raise ValueError("La nueva contraseña debe ser diferente a la actual")
        
        return v
    
    @field_validator('confirmar_password_nueva')
    @classmethod
    def validate_confirmacion(cls, v, info):
        """Validar que las contraseñas coincidan"""
        if 'password_nueva' in info.data and v != info.data['password_nueva']:
            raise ValueError("Las contraseñas no coinciden")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "password_actual": "Password123!",
                "password_nueva": "NuevaPassword456!",
                "confirmar_password_nueva": "NuevaPassword456!"
            }
        }
    }