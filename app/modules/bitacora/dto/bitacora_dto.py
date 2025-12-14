"""
DTOs del Módulo de Bitácora
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class BitacoraResponseDTO(BaseModel):
    """DTO para respuesta de bitácora"""
    id: int
    id_usuario_admin: Optional[int] = None
    accion: str
    descripcion: Optional[str] = None
    created_at: datetime
    id_objetivo: Optional[int] = None
    tipo_objetivo: Optional[str] = None
    estado_anterior: Optional[Dict[str, Any]] = None
    estado_nuevo: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True

class FiltrosBitacoraDTO(BaseModel):
    """DTO para filtros de bitácora"""
    usuario_admin_id: Optional[int] = None
    accion: Optional[str] = None
    tipo_objetivo: Optional[str] = None
    id_objetivo: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    page: int = Field(1, ge=1)
    per_page: int = Field(50, ge=1, le=100)

class EstadisticasBitacoraDTO(BaseModel):
    """DTO para estadísticas de bitácora"""
    total_registros: int
    acciones_comunes: List[Dict[str, Any]] = []
    usuarios_activos: List[Dict[str, Any]] = []

class ResumenBitacoraDTO(BaseModel):
    """DTO para resumen de bitácora por fecha"""
    tipo: str
    resumen: List[Dict[str, Any]] = []

class PaginatedBitacoraDTO(BaseModel):
    """DTO para respuesta paginada de bitácora"""
    items: List[BitacoraResponseDTO] = []
    total: int
    page: int
    per_page: int
    pages: int
