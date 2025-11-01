# app/modules/esquelas/controllers/codigo_esquela_controller.py
"""Controlador (router) para códigos de esquela."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.extensions import get_db
from app.modules.esquelas.services.codigo_esquela_service import CodigoEsquelaService
from app.modules.esquelas.dto.codigo_esquela_dto import (
    CodigoEsquelaCreateDTO,
    CodigoEsquelaUpdateDTO,
    CodigoEsquelaResponseDTO
)


router = APIRouter(prefix="/codigos-esquelas", tags=["Códigos de Esquela"])


@router.get("/", response_model=List[CodigoEsquelaResponseDTO])
def listar_codigos(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'reconocimiento' u 'orientacion'"),
    db: Session = Depends(get_db)
):
    """Listar todos los códigos de esquela o filtrar por tipo"""
    if tipo:
        return CodigoEsquelaService.listar_por_tipo(db, tipo)
    return CodigoEsquelaService.listar_codigos(db)


@router.get("/{id_codigo}", response_model=CodigoEsquelaResponseDTO)
def obtener_codigo(id_codigo: int, db: Session = Depends(get_db)):
    """Obtener un código de esquela por ID"""
    return CodigoEsquelaService.obtener_codigo(db, id_codigo)


@router.post("/", response_model=CodigoEsquelaResponseDTO, status_code=201)
def crear_codigo(codigo_data: CodigoEsquelaCreateDTO, db: Session = Depends(get_db)):
    """Crear un nuevo código de esquela"""
    return CodigoEsquelaService.crear_codigo(db, codigo_data)


@router.put("/{id_codigo}", response_model=CodigoEsquelaResponseDTO)
def actualizar_codigo(
    id_codigo: int,
    codigo_data: CodigoEsquelaUpdateDTO,
    db: Session = Depends(get_db)
):
    """Actualizar un código de esquela"""
    return CodigoEsquelaService.actualizar_codigo(db, id_codigo, codigo_data)


@router.delete("/{id_codigo}")
def eliminar_codigo(id_codigo: int, db: Session = Depends(get_db)):
    """Eliminar un código de esquela"""
    codigo = CodigoEsquelaService.eliminar_codigo(db, id_codigo)
    return {"message": "Código eliminado exitosamente", "codigo": codigo.codigo}
