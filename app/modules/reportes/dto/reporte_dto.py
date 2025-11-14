# app/modules/reportes/dto/reporte_dto.py
from pydantic import BaseModel
from typing import List, Optional


class RankingItemDTO(BaseModel):
    """DTO para un item del ranking"""
    id: int
    nombre: str
    total: int
    reconocimiento: int = 0
    orientacion: int = 0
    posicion: int


class RankingResponseDTO(BaseModel):
    """DTO para respuesta de ranking"""
    metric: str  # 'student' o 'course'
    type: Optional[str] = None  # 'reconocimiento', 'orientacion' o None (todos)
    limit: int
    data: List[RankingItemDTO]
