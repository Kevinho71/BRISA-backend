# app/modules/administracion/controllers/administrativo_controller.py
"""Controladores (routers) para administrativos"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.modules.administracion.dto.administrativo_dto import (
    AdministrativoCreateDTO, AdministrativoReadDTO, AdministrativoFullDTO, AdministrativoUpdateDTO, CargoReadDTO
)
from app.modules.administracion.services.administrativo_service import (
    AdministrativoService, CargoService
)

router = APIRouter(prefix="/api/administrativos", tags=["Administrativos"])


# ============ ENDPOINTS ESTÁTICOS (PRIMERO) ============

# ---- ADMINISTRATIVOS ----
@router.post("/", response_model=AdministrativoReadDTO, status_code=status.HTTP_201_CREATED)
def crear_administrativo(administrativo: dict, db: Session = Depends(get_db)):
    """
    Crea un nuevo administrativo
   
    - **ci**: Cédula de identidad (único)
    - **nombres**: Nombres del administrativo
    - **apellido_paterno**: Apellido paterno
    - **correo**: Correo electrónico (único, opcional)
    - **id_cargo**: ID del cargo (requerido)
    - **estado_laboral**: activo, retirado, suspendido, etc.
    """
    try:
        validated_data = AdministrativoCreateDTO(**administrativo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Datos inválidos: {str(e)}"
        )
    
    try:
        return AdministrativoService.crear_administrativo(db, validated_data)
    except HTTPException:
        # Re-lanzar HTTPException tal cual
        raise
    except Exception as e:
        # Manejar otros errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el administrativo: {str(e)}"
        )

@router.get("/", response_model=List[AdministrativoFullDTO])
def listar_administrativos(
    completo: bool = Query(True, description="Si es True, incluye información completa"),
    db: Session = Depends(get_db)
):
    """
    Lista todos los administrativos
   
    - Si **completo=True**: Incluye información completa con departamentos
    - Si **completo=False**: Solo datos básicos
    """
    if completo:
        return AdministrativoService.listar_administrativos_completo(db)
    else:
        return AdministrativoService.listar_administrativos(db)


# ---- CARGOS ----
@router.get("/cargos", response_model=List[CargoReadDTO], tags=["Cargos"])
def listar_cargos(db: Session = Depends(get_db)):
    """
    Lista todos los cargos disponibles para administrativos
    """
    return CargoService.listar_cargos(db)


# ============ ENDPOINTS DINÁMICOS (DESPUÉS) ============

# ---- ADMINISTRATIVOS ----
@router.get("/{id_persona}", response_model=AdministrativoReadDTO)
def obtener_administrativo(id_persona: int, db: Session = Depends(get_db)):
    """
    Obtiene un administrativo específico por su ID de persona
    """
    administrativo = AdministrativoService.obtener_administrativo(db, id_persona)
    if not administrativo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Administrativo con ID {id_persona} no encontrado"
        )
    return administrativo

@router.put("/{id_persona}", response_model=AdministrativoReadDTO)
def actualizar_administrativo(
    id_persona: int,
    data: dict, # Aceptar dict para más flexibilidad
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un administrativo
   
    - Solo se actualizan los campos proporcionados
    - CI y correo deben ser únicos
    """
    try:
        validated_data = AdministrativoUpdateDTO(**data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Datos inválidos: {str(e)}"
        )
   
    administrativo_actualizado = AdministrativoService.actualizar_administrativo(db, id_persona, validated_data)
    if not administrativo_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Administrativo con ID {id_persona} no encontrado"
        )
    return administrativo_actualizado

@router.delete("/{id_persona}", response_model=AdministrativoReadDTO)
def eliminar_administrativo(id_persona: int, db: Session = Depends(get_db)):
    """
    Elimina un administrativo
   
    - Se elimina la persona y el registro administrativo en cascada
    """
    administrativo_eliminado = AdministrativoService.eliminar_administrativo(db, id_persona)
    if not administrativo_eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Administrativo con ID {id_persona} no encontrado"
        )
    return administrativo_eliminado


# ---- CARGOS (DINÁMICA) ----
@router.get("/cargos/{id_cargo}", response_model=CargoReadDTO, tags=["Cargos"])
def obtener_cargo(id_cargo: int, db: Session = Depends(get_db)):
    """
    Obtiene un cargo específico por su ID
    """
    cargo = CargoService.obtener_cargo(db, id_cargo)
    if not cargo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cargo con ID {id_cargo} no encontrado"
        )
    return cargo

