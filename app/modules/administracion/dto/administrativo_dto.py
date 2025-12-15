# app/modules/administracion/dto/administrativo_dto.py
"""DTOs para administrativos"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ============ ADMINISTRATIVO DTOs ============
class AdministrativoCreateDTO(BaseModel):
    ci: str = Field(..., min_length=7, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=50)
    apellido_paterno: str = Field(..., min_length=2, max_length=50)
    apellido_materno: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    id_cargo: int = Field(..., gt=0)
    estado_laboral: Optional[str] = "activo"
    años_experiencia: Optional[int] = 0
    fecha_ingreso: Optional[str] = None
    horario_entrada: Optional[str] = "08:00:00"  # Time como string HH:MM:SS
    horario_salida: Optional[str] = "16:00:00"
    area_trabajo: Optional[str] = Field(None, max_length=100)
    observaciones: Optional[str] = None


class AdministrativoUpdateDTO(BaseModel):
    ci: Optional[str] = None
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    id_cargo: Optional[int] = None
    estado_laboral: Optional[str] = None
    años_experiencia: Optional[int] = None
    fecha_ingreso: Optional[str] = None
    horario_entrada: Optional[str] = None
    horario_salida: Optional[str] = None
    area_trabajo: Optional[str] = None
    observaciones: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class AdministrativoReadDTO(BaseModel):
    id_administrativo: int
    id_persona: int
    id_cargo: int
    nombre_cargo: Optional[str] = None
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    nombre_completo: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    estado_laboral: str
    años_experiencia: Optional[int] = 0
    fecha_ingreso: Optional[str] = None
    horario_entrada: Optional[str] = None
    horario_salida: Optional[str] = None
    area_trabajo: Optional[str] = None
    observaciones: Optional[str] = None
    horas_semana: Optional[int] = None  # Calculado

    model_config = ConfigDict(from_attributes=True)


class AdministrativoFullDTO(BaseModel):
    id_administrativo: int
    id_persona: int
    id_cargo: int
    nombre_cargo: Optional[str] = None
    ci: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    nombre_completo: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    estado_laboral: str
    años_experiencia: Optional[int] = 0
    fecha_ingreso: Optional[str] = None
    horario_entrada: Optional[str] = None
    horario_salida: Optional[str] = None
    area_trabajo: Optional[str] = None
    observaciones: Optional[str] = None
    horas_semana: Optional[int] = None
    departamentos: List[str] = []  # Para compatibilidad con frontend

    model_config = ConfigDict(from_attributes=True)


# ============ CARGO DTOs ============
class CargoReadDTO(BaseModel):
    id_cargo: int
    nombre_cargo: str
    descripcion: Optional[str] = None
    estado: str
    fecha_creacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

