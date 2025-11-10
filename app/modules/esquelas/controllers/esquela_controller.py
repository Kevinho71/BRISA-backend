"""Controlador (router) para el módulo de Esquelas."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Fuente correcta del dependency de BD
from app.core.database import get_db

from app.modules.esquelas.services.esquela_service import EsquelaService
from app.modules.esquelas.dto.esquela_dto import EsquelaBaseDTO, EsquelaResponseDTO


router = APIRouter(prefix="/esquelas", tags=["Esquelas"])


@router.get("/", response_model=List[EsquelaResponseDTO])
def listar_esquelas(db: Session = Depends(get_db)):
    return EsquelaService.listar_esquelas(db)


@router.get("/{id}", response_model=EsquelaResponseDTO)
def obtener_esquela(id: int, db: Session = Depends(get_db)):
    return EsquelaService.obtener_esquela(db, id)


@router.post("/", response_model=EsquelaResponseDTO)
def crear_esquela(esquela_data: EsquelaBaseDTO, db: Session = Depends(get_db)):
    return EsquelaService.crear_esquela(db, esquela_data)


@router.delete("/{id}")
def eliminar_esquela(id: int, db: Session = Depends(get_db)):
    return EsquelaService.eliminar_esquela(db, id)
