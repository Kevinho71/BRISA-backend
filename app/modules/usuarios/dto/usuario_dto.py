"""
app/modules/usuarios/dto/usuario_dto.py
✅ DTOs completos para CRUD de Personas - SINTAXIS CORREGIDA
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
import re


# ==================== PERSONA DTOs ====================

class PersonaCreateDTO(BaseModel):
    """
    DTO para crear persona
    ✅ Genera automáticamente usuario y contraseña
    """
    ci: str = Field(..., min_length=5, max_length=20, description="Cédula de identidad")
    nombres: str = Field(..., min_length=2, max_length=50, description="Nombres de la persona")
    apellido_paterno: str = Field(..., min_length=2, max_length=50, description="Apellido paterno")
    apellido_materno: str = Field(..., min_length=2, max_length=50, description="Apellido materno (REQUERIDO)")
    correo: str = Field(..., max_length=50, description="Correo electrónico")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección física")
    tipo_persona: str = Field(
        ..., 
        description="Tipo de persona en el sistema"
    )
    tiene_acceso: Optional[bool] = None
    # ✅ Opcional: permite asignar rol específico al crear
    id_rol: Optional[int] = Field(None, description="ID del rol a asignar (opcional)")
    
    @field_validator('tipo_persona')
    @classmethod
    def validar_tipo_persona(cls, v: str) -> str:
        """Validar tipo de persona - solo profesor o administrativo"""
        tipos_validos = ['profesor', 'administrativo']
        if v.lower() not in tipos_validos:
            raise ValueError(f"tipo_persona debe ser 'profesor' o 'administrativo'")
        return v.lower()
    
    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v: str) -> str:
        """Validar formato de correo electrónico"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, v):
            raise ValueError('Formato de correo electrónico inválido')
        return v.lower()
    
    @field_validator('nombres', 'apellido_paterno', 'apellido_materno')
    @classmethod
    def validar_nombres(cls, v: Optional[str]) -> Optional[str]:
        """
        ✅ CORREGIDO: Validar y limpiar nombres
        Permite: letras (con acentos), espacios, guiones, apóstrofes
        NO permite: números, caracteres especiales raros
        """
        if v is None:
            return v
        
        # Eliminar espacios múltiples y trimear
        v = re.sub(r'\s+', ' ', v.strip())
        
        # ✅ PATRÓN CORREGIDO: Incluye acentos españoles
        patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'\-]+$"
        
        if not re.match(patron, v):
            raise ValueError('Solo se permiten letras, espacios, guiones y apóstrofes')
        
        return v
    
    @field_validator('ci')
    @classmethod
    def validar_ci(cls, v: str) -> str:
        """
        ✅ CORREGIDO: Validar y limpiar CI
        Permite alfanuméricos y algunos caracteres especiales
        """
        # Eliminar espacios extras
        v = v.strip()
        
        # Validar longitud después de limpiar
        if len(v) > 20:
            raise ValueError('CI no puede exceder 20 caracteres')
        
        # ✅ Permitir letras, números y guiones
        if not re.match(r'^[A-Za-z0-9\-]+$', v):
            raise ValueError('CI solo puede contener letras, números y guiones')
        
        return v.upper()

class PersonaUpdateDTO(BaseModel):
    """DTO para actualizar persona"""
    nombres: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido_paterno: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido_materno: Optional[str] = Field(None, min_length=2, max_length=50)
    correo: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=100)
    tipo_persona: Optional[str] = None
    
    @field_validator('tipo_persona')
    @classmethod
    def validar_tipo_persona(cls, v: Optional[str]) -> Optional[str]:
        """Validar tipo de persona"""
        if v is None:
            return v
        tipos_validos = ['profesor', 'administrativo']
        if v.lower() not in tipos_validos:
            raise ValueError(f"tipo_persona debe ser 'profesor' o 'administrativo'")
        return v.lower()
    
    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v: Optional[str]) -> Optional[str]:
        if v:
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron, v):
                raise ValueError('Formato de correo electrónico inválido')
            return v.lower()
        return v
    
    @field_validator('nombres', 'apellido_paterno', 'apellido_materno')
    @classmethod
    def validar_nombres(cls, v: Optional[str]) -> Optional[str]:
        """✅ CORREGIDO: Misma validación que en Create"""
        if v is None:
            return v
        
        v = re.sub(r'\s+', ' ', v.strip())
        
        # ✅ Incluye acentos y caracteres especiales válidos
        patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'\-]+$"
        
        if not re.match(patron, v):
            raise ValueError('Solo se permiten letras, espacios, guiones y apóstrofes')
        
        return v


# En usuario_dto.py

class PersonaResponseDTO(BaseModel):
    """
    DTO de respuesta de persona
    ✅ Incluye información del usuario generado
    """
    id_persona: int
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    tipo_persona: str
    is_active: bool
    
    # ✅ Información adicional del usuario generado
    usuario: Optional[str] = None
    id_usuario: Optional[int] = None
    tiene_acceso: bool = False
    
    model_config = ConfigDict(from_attributes=True)
    
    @property
    def nombre_completo(self) -> str:
        """Nombre completo de la persona"""
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"


class PersonaFiltrosDTO(BaseModel):
    """DTO para filtros de búsqueda de personas"""
    tipo_persona: Optional[str] = None
    is_active: Optional[bool] = None
    busqueda: Optional[str] = None
    skip: int = 0
    limit: int = 50


class PersonasStatsDTO(BaseModel):
    """DTO para estadísticas de personas"""
    total_personas: int
    total_profesores: int
    total_administrativos: int
    personas_activas: int
    personas_inactivas: int
    personas_con_usuario: int
    personas_sin_usuario: int

class PersonaConCredencialesDTO(BaseModel):
    """
    DTO que incluye las credenciales generadas
    ✅ Se usa al crear persona para informar al admin
    """
    persona: PersonaResponseDTO
    credenciales: dict = Field(
        ...,
        description="Credenciales de acceso generadas",
        example={
            "usuario": "pjuan",
            "password_temporal": "Temporal123*",
            "mensaje": "Credenciales generadas automáticamente"
        }
    )


# ==================== ROL DTOs ====================

class RolCreateDTO(BaseModel):
    """DTO para crear rol"""
    nombre: str = Field(..., min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class RolUpdateDTO(BaseModel):
    """DTO para actualizar rol"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class RolResponseDTO(BaseModel):
    """DTO de respuesta de rol"""
    id_rol: int
    nombre: str
    descripcion: Optional[str] = None
    is_active: bool
    permisosCount: int = 0
    usuariosCount: int = 0
    permisos: List[dict] = []

    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm(cls, rol):
        return cls(
            id_rol=rol.id_rol,
            nombre=rol.nombre,
            descripcion=rol.descripcion,
            is_active=rol.is_active,
            permisosCount=0,
            usuariosCount=0,
            permisos=[]
        )


# ==================== PERMISO DTOs ====================

class PermisoResponseDTO(BaseModel):
    """DTO de respuesta de permiso"""
    id_permiso: int
    nombre: str
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    modulo: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class PermisoCreateDTO(BaseModel):
    """DTO para crear permiso"""
    nombre: str = Field(..., min_length=3, max_length=100)
    codigo: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)
    modulo: str = Field(..., max_length=50)
    is_active: bool = True


# ==================== USUARIO DTOs ====================

class UsuarioCreateDTO(BaseModel):
    """DTO para crear usuario"""
    id_persona: int
    usuario: str = Field(..., min_length=3, max_length=50)
    correo: str
    password: str = Field(..., min_length=8)
    is_active: bool = True
    
    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v: str) -> str:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, v):
            raise ValueError('Formato de correo electrónico inválido')
        return v.lower()


class UsuarioUpdateDTO(BaseModel):
    """DTO para actualizar usuario"""
    usuario: Optional[str] = Field(None, min_length=3, max_length=50)
    correo: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    
    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v: Optional[str]) -> Optional[str]:
        if v:
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron, v):
                raise ValueError('Formato de correo electrónico inválido')
            return v.lower()
        return v


class UsuarioResponseDTO(BaseModel):
    """DTO de respuesta de usuario"""
    id_usuario: int
    id_persona: int
    usuario: str
    correo: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class AsignarRolDTO(BaseModel):
    """DTO para asignar rol a usuario"""
    id_usuario: int
    id_rol: int
    razon: Optional[str] = Field(None, max_length=255)