from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.config import get_db
from app.shared.response import ResponseModel
from app.shared.security import verify_token
from app.modules.bitacora.dto.bitacora_dto import BitacoraResponseDTO, FiltrosAuditoriaDTO
from app.modules.bitacora.services.bitacora_service import AuditoriaService

router = APIRouter()

@router.get("", response_model=dict)
async def obtener_bitacora(
    usuario_admin: Optional[int] = Query(None, description="Filtrar por usuario administrador"),
    accion: Optional[str] = Query(None, description="Filtrar por acción"),
    tipo_objetivo: Optional[str] = Query(None, description="Filtrar por tipo de objetivo"),
    id_objetivo: Optional[int] = Query(None, description="Filtrar por ID de objetivo"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    Obtener registros de auditoría (RF-08)
    
    Parámetros de filtro:
    - usuario_admin: ID del usuario que realizó la acción
    - accion: Tipo de acción (crear_usuario, editar_usuario, etc.)
    - tipo_objetivo: Tipo de objeto afectado (Usuario, Rol, etc.)
    - id_objetivo: ID del objeto afectado
    - fecha_inicio: Fecha inicio (formato: YYYY-MM-DD)
    - fecha_fin: Fecha fin (formato: YYYY-MM-DD)
    """
    try:
        # Convertir fechas si existen
        fecha_inicio_dt = None
        fecha_fin_dt = None
        
        if fecha_inicio:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
        if fecha_fin:
            fecha_fin_dt = datetime.fromisoformat(fecha_fin)
        
        registros, total = AuditoriaService.obtener_registros_auditoria(
            db,
            usuario_admin=usuario_admin,
            accion=accion,
            tipo_objetivo=tipo_objetivo,
            id_objetivo=id_objetivo,
            fecha_inicio=fecha_inicio_dt,
            fecha_fin=fecha_fin_dt,
            skip=skip,
            limit=limit
        )
        
        # Mapear respuestas
        datos = []
        for reg in registros:
            datos.append({
                "id_bitacora": reg.id_bitacora,
                "id_usuario_admin": reg.id_usuario_admin,
                "usuario_admin": reg.usuario_admin.usuario if reg.usuario_admin else None,
                "accion": reg.accion,
                "descripcion": reg.descripcion,
                "fecha_hora": reg.fecha_hora.isoformat(),
                "id_objetivo": reg.id_objetivo,
                "tipo_objetivo": reg.tipo_objetivo,
                "estado_anterior": reg.estado_anterior,
                "estado_nuevo": reg.estado_nuevo,
                "ip_address": reg.ip_address
            })
        
        return ResponseModel.success(
            message="Registros de auditoría obtenidos",
            data={
                "total": total,
                "skip": skip,
                "limit": limit,
                "registros": datos
            },
            status_code=status.HTTP_200_OK
        )
    
    except ValueError as e:
        return ResponseModel.error(
            message="Formato de fecha inválido",
            error_details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener auditoría",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/usuario/{id_usuario}", response_model=dict)
async def obtener_auditoria_usuario(
    id_usuario: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener auditoría de un usuario específico"""
    try:
        registros, total = AuditoriaService.obtener_auditoria_usuario(db, id_usuario, skip, limit)
        
        datos = []
        for reg in registros:
            datos.append({
                "id_bitacora": reg.id_bitacora,
                "accion": reg.accion,
                "descripcion": reg.descripcion,
                "fecha_hora": reg.fecha_hora.isoformat(),
                "tipo_objetivo": reg.tipo_objetivo,
                "id_objetivo": reg.id_objetivo
            })
        
        return ResponseModel.success(
            message="Auditoría del usuario obtenida",
            data={
                "id_usuario": id_usuario,
                "total": total,
                "registros": datos
            },
            status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener auditoría del usuario",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/objeto/{tipo_objetivo}/{id_objetivo}", response_model=dict)
async def obtener_auditoria_objeto(
    tipo_objetivo: str,
    id_objetivo: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener historial de auditoría de un objeto específico"""
    try:
        registros, total = AuditoriaService.obtener_auditoria_por_tipo(
            db, tipo_objetivo, id_objetivo, skip, limit
        )
        
        datos = []
        for reg in registros:
            datos.append({
                "id_bitacora": reg.id_bitacora,
                "usuario_admin": reg.usuario_admin.usuario if reg.usuario_admin else None,
                "accion": reg.accion,
                "descripcion": reg.descripcion,
                "fecha_hora": reg.fecha_hora.isoformat(),
                "estado_anterior": reg.estado_anterior,
                "estado_nuevo": reg.estado_nuevo
            })
        
        return ResponseModel.success(
            message="Historial de objeto obtenido",
            data={
                "tipo_objetivo": tipo_objetivo,
                "id_objetivo": id_objetivo,
                "total": total,
                "registros": datos
            },
            status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener historial",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/estadisticas", response_model=dict)
async def obtener_estadisticas_auditoria(
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener estadísticas de auditoría"""
    try:
        fecha_inicio_dt = None
        if fecha_inicio:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
        
        stats = AuditoriaService.obtener_estadisticas_auditoria(db, fecha_inicio_dt)
        
        return ResponseModel.success(
            message="Estadísticas obtenidas",
            data=stats,
            status_code=status.HTTP_200_OK
        )
    
    except ValueError as e:
        return ResponseModel.error(
            message="Formato de fecha inválido",
            error_details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener estadísticas",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/resumen/{tipo_periodo}", response_model=dict)
async def obtener_resumen_auditoria(
    tipo_periodo: str = Query(..., description="dia, semana o mes"),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """Obtener resumen de actividades por período"""
    try:
        if tipo_periodo not in ['dia', 'semana', 'mes']:
            raise ValueError("tipo_periodo debe ser: dia, semana o mes")
        
        resumen = AuditoriaService.obtener_resumen_por_fecha(db, tipo_periodo)
        
        return ResponseModel.success(
            message="Resumen obtenido",
            data=resumen,
            status_code=status.HTTP_200_OK
        )
    
    except ValueError as e:
        return ResponseModel.error(
            message="Parámetro inválido",
            error_details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return ResponseModel.error(
            message="Error al obtener resumen",
            error_details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
