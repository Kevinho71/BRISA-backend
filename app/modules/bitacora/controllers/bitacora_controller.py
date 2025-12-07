"""
app/modules/bitacora/controllers/bitacora_controller.py
Controlador completo: LoginLog (autenticación) + Bitácora (auditoría general)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.shared.response import ResponseModel
from app.shared.permissions import requires_permission
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.modules.usuarios.models.usuario_models import Usuario, LoginLog, Bitacora

logger = logging.getLogger(__name__)
router = APIRouter()

# ============================================================
# RAÍZ DEL ROUTER
# ============================================================

@router.get("/", response_model=dict)
async def raiz_bitacora():
    """Rutas disponibles en el módulo de auditoría"""
    return {
        "message": "API de Auditoría BRISA",
        "endpoints": {
            "login_logs": "/api/bitacora/login-logs (autenticación)",
            "auditoria_general": "/api/bitacora/auditoria (CU-07)",
            "estadisticas": "/api/bitacora/estadisticas"
        }
    }


# ============================================================
# CU-07: CONSULTAR AUDITORÍA GENERAL (Tabla Bitácora)
# ============================================================

@router.get("/auditoria", response_model=dict)
@requires_permission('ver_bitacora')
async def consultar_auditoria(
    # CU-07 Paso 2-3: Filtros opcionales
    usuario_admin: Optional[int] = Query(None, description="ID del usuario que ejecutó la acción"),
    accion: Optional[str] = Query(None, description="Tipo de acción (LOGIN, CREAR_USUARIO, etc)"),
    tipo_objetivo: Optional[str] = Query(None, description="Tipo de objeto (Usuario, Rol, etc)"),
    id_objetivo: Optional[int] = Query(None, description="ID del objeto afectado"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    
    # Paginación
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    📋 CU-07: Consultar Auditoría General
    
    Muestra registros de la tabla Bitácora (acciones del sistema):
    - Creación/edición/eliminación de usuarios
    - Asignación/revocación de roles
    - Cambios de permisos
    - Todas las acciones administrativas
    """
    try:
        # CU-07 Paso 5: Consultar tabla Bitácora
        query = db.query(Bitacora)
        
        # Aplicar filtros
        if usuario_admin:
            query = query.filter(Bitacora.id_usuario_admin == usuario_admin)
        
        if accion:
            query = query.filter(Bitacora.accion.ilike(f"%{accion}%"))
        
        if tipo_objetivo:
            query = query.filter(Bitacora.tipo_objetivo == tipo_objetivo)
        
        if id_objetivo:
            query = query.filter(Bitacora.id_objetivo == id_objetivo)
        
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
                query = query.filter(Bitacora.fecha_hora >= fecha_inicio_dt)
            except ValueError:
                return ResponseModel.error(
                    message="Formato de fecha_inicio inválido. Use YYYY-MM-DD",
                    status_code=400
                )
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.fromisoformat(fecha_fin)
                fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Bitacora.fecha_hora <= fecha_fin_dt)
            except ValueError:
                return ResponseModel.error(
                    message="Formato de fecha_fin inválido. Use YYYY-MM-DD",
                    status_code=400
                )
        
        # CU-07 Paso 5: Contar total
        total = query.count()
        
        # CU-07 Paso 6: Ordenar por fecha descendente
        registros = query.order_by(desc(Bitacora.fecha_hora)).offset(skip).limit(limit).all()
        
        # CU-07 Paso 7: Formatear respuesta
        items = []
        for registro in registros:
            # Obtener info del usuario
            usuario = db.query(Usuario).filter(
                Usuario.id_usuario == registro.id_usuario_admin
            ).first()
            
            items.append({
                "id_bitacora": registro.id_bitacora,
                "id_usuario_admin": registro.id_usuario_admin,
                "usuario": usuario.usuario if usuario else "Sistema",
                "nombre_completo": usuario.persona.nombre_completo if usuario and usuario.persona else "Sistema",
                "accion": registro.accion,
                "descripcion": registro.descripcion,
                "fecha_hora": registro.fecha_hora.isoformat() if registro.fecha_hora else None,
                "tipo_objetivo": registro.tipo_objetivo,
                "id_objetivo": registro.id_objetivo,
                # Indicador visual
                "icono": _obtener_icono_accion(registro.accion)
            })
        
        # Calcular paginación
        import math
        pages = math.ceil(total / limit) if limit > 0 else 1
        current_page = (skip // limit) + 1 if limit > 0 else 1
        
        return ResponseModel.success(
            message=f"Registros de auditoría obtenidos ({total} total)",
            data={
                "items": items,
                "total": total,
                "page": current_page,
                "pages": pages,
                "skip": skip,
                "limit": limit,
                "has_more": current_page < pages,
                "filtros_aplicados": {
                    "usuario_admin": usuario_admin,
                    "accion": accion,
                    "tipo_objetivo": tipo_objetivo,
                    "id_objetivo": id_objetivo,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            },
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error en CU-07 Consultar Auditoría: {str(e)}", exc_info=True)
        return ResponseModel.error(
            message="Error al consultar auditoría",
            error_details=str(e),
            status_code=500
        )


# ============================================================
# ESTADÍSTICAS DE AUDITORÍA GENERAL
# ============================================================

@router.get("/auditoria/estadisticas", response_model=dict)
@requires_permission('ver_bitacora')
async def estadisticas_auditoria(
    dias: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    📊 Estadísticas de auditoría general
    
    Muestra:
    - Acciones más frecuentes
    - Usuarios más activos
    - Distribución por tipo de acción
    """
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        # Total de registros
        total_registros = db.query(Bitacora).filter(
            Bitacora.fecha_hora >= fecha_inicio
        ).count()
        
        # Acciones más comunes
        acciones_comunes = db.query(
            Bitacora.accion,
            func.count(Bitacora.id_bitacora).label('cantidad')
        ).filter(
            Bitacora.fecha_hora >= fecha_inicio
        ).group_by(
            Bitacora.accion
        ).order_by(desc('cantidad')).limit(10).all()
        
        # Usuarios más activos
        usuarios_activos = db.query(
            Usuario.usuario,
            func.count(Bitacora.id_bitacora).label('cantidad')
        ).join(
            Bitacora, Usuario.id_usuario == Bitacora.id_usuario_admin
        ).filter(
            Bitacora.fecha_hora >= fecha_inicio
        ).group_by(
            Usuario.usuario
        ).order_by(desc('cantidad')).limit(10).all()
        
        # Distribución por tipo de objetivo
        por_tipo = db.query(
            Bitacora.tipo_objetivo,
            func.count(Bitacora.id_bitacora).label('cantidad')
        ).filter(
            Bitacora.fecha_hora >= fecha_inicio,
            Bitacora.tipo_objetivo.isnot(None)
        ).group_by(
            Bitacora.tipo_objetivo
        ).order_by(desc('cantidad')).all()
        
        return ResponseModel.success(
            message="Estadísticas de auditoría obtenidas",
            data={
                "periodo": {
                    "dias": dias,
                    "desde": fecha_inicio.isoformat(),
                    "hasta": datetime.now().isoformat()
                },
                "resumen": {
                    "total_registros": total_registros
                },
                "acciones_comunes": [
                    {"accion": accion, "cantidad": cantidad}
                    for accion, cantidad in acciones_comunes
                ],
                "usuarios_activos": [
                    {"usuario": usuario, "cantidad": cantidad}
                    for usuario, cantidad in usuarios_activos
                ],
                "por_tipo_objetivo": [
                    {"tipo": tipo, "cantidad": cantidad}
                    for tipo, cantidad in por_tipo
                ]
            },
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}", exc_info=True)
        return ResponseModel.error(
            message="Error al obtener estadísticas",
            error_details=str(e),
            status_code=500
        )


# ============================================================
# TIPOS DE ACCIONES DISPONIBLES
# ============================================================

@router.get("/auditoria/acciones", response_model=dict)
@requires_permission('ver_bitacora')
async def listar_tipos_acciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    📝 Listar tipos de acciones disponibles
    Útil para los filtros en el frontend
    """
    try:
        from sqlalchemy import distinct
        
        acciones = db.query(distinct(Bitacora.accion)).order_by(Bitacora.accion).all()
        acciones_list = [a[0] for a in acciones if a[0]]
        
        return ResponseModel.success(
            message="Tipos de acciones obtenidos",
            data={
                "acciones": acciones_list,
                "total": len(acciones_list)
            },
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error al listar acciones: {str(e)}")
        return ResponseModel.error(
            message="Error al listar acciones",
            error_details=str(e),
            status_code=500
        )


# ============================================================
# LOGIN LOGS (Autenticación) - TU CÓDIGO ORIGINAL
# ============================================================

@router.get("/login-logs", response_model=dict)
@requires_permission('ver_bitacora')
async def obtener_login_logs(
    usuario_id: Optional[int] = Query(None),
    estado: Optional[str] = Query(None),
    ip_address: Optional[str] = Query(None),
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    🔐 Logs de autenticación (LOGIN/LOGOUT)
    Vista específica para seguridad
    """
    try:
        query = db.query(LoginLog)
        
        if usuario_id:
            query = query.filter(LoginLog.id_usuario == usuario_id)
        
        if estado:
            if estado not in ['exitoso', 'fallido']:
                return ResponseModel.error(
                    message="Estado inválido. Use 'exitoso' o 'fallido'",
                    status_code=400
                )
            query = query.filter(LoginLog.estado == estado)
        
        if ip_address:
            query = query.filter(LoginLog.ip_address.contains(ip_address))
        
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
                query = query.filter(LoginLog.fecha_hora >= fecha_inicio_dt)
            except ValueError:
                return ResponseModel.error(
                    message="Formato de fecha_inicio inválido",
                    status_code=400
                )
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.fromisoformat(fecha_fin)
                fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(LoginLog.fecha_hora <= fecha_fin_dt)
            except ValueError:
                return ResponseModel.error(
                    message="Formato de fecha_fin inválido",
                    status_code=400
                )
        
        total = query.count()
        logs = query.order_by(desc(LoginLog.fecha_hora)).offset(skip).limit(limit).all()
        
        logs_data = []
        for log in logs:
            usuario = db.query(Usuario).filter(
                Usuario.id_usuario == log.id_usuario
            ).first()
            
            from app.modules.auth.repositories.auth_repository import AuthRepository
            bloqueado, fecha_desbloqueo = AuthRepository.verificar_cuenta_bloqueada(
                db, log.id_usuario
            ) if log.estado == 'fallido' else (False, None)
            
            logs_data.append({
                "id_log": log.id_log,
                "usuario_id": log.id_usuario,
                "usuario": usuario.usuario if usuario else "N/A",
                "nombre_completo": usuario.persona.nombre_completo if usuario and usuario.persona else "N/A",
                "fecha_hora": log.fecha_hora.isoformat() if log.fecha_hora else None,
                "estado": log.estado,
                "ip_address": log.ip_address or "N/A",
                "user_agent": log.user_agent or "N/A",
                "usuario_activo": usuario.is_active if usuario else False,
                "cuenta_bloqueada": bloqueado,
                "fecha_desbloqueo": fecha_desbloqueo.isoformat() if fecha_desbloqueo else None,
                "icono": "🟢" if log.estado == 'exitoso' else "🔴",
                "navegador": _extraer_navegador(log.user_agent),
                "sistema_operativo": _extraer_sistema_operativo(log.user_agent)
            })
        
        estadisticas = _calcular_estadisticas_login(db, fecha_inicio, fecha_fin)
        
        return ResponseModel.success(
            message="Login logs obtenidos",
            data={
                "logs": logs_data,
                "total": total,
                "skip": skip,
                "limit": limit,
                "paginas": (total + limit - 1) // limit if limit > 0 else 1,
                "estadisticas": estadisticas
            },
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error al obtener login logs: {str(e)}", exc_info=True)
        return ResponseModel.error(
            message="Error al obtener login logs",
            error_details=str(e),
            status_code=500
        )


@router.get("/login-logs/estadisticas", response_model=dict)
@requires_permission('ver_bitacora')
async def obtener_estadisticas_login(
    dias: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """📊 Estadísticas de autenticación"""
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        total_exitosos = db.query(LoginLog).filter(
            and_(LoginLog.estado == 'exitoso', LoginLog.fecha_hora >= fecha_inicio)
        ).count()
        
        total_fallidos = db.query(LoginLog).filter(
            and_(LoginLog.estado == 'fallido', LoginLog.fecha_hora >= fecha_inicio)
        ).count()
        
        total_intentos = total_exitosos + total_fallidos
        tasa_exito = (total_exitosos / total_intentos * 100) if total_intentos > 0 else 0
        
        return ResponseModel.success(
            message="Estadísticas de autenticación obtenidas",
            data={
                "periodo": {"dias": dias},
                "resumen": {
                    "total_intentos": total_intentos,
                    "exitosos": total_exitosos,
                    "fallidos": total_fallidos,
                    "tasa_exito": round(tasa_exito, 2)
                }
            },
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return ResponseModel.error(message="Error al obtener estadísticas", status_code=500)


@router.get("/login-logs/usuario/{usuario_id}", response_model=dict)
@requires_permission('ver_bitacora')
async def obtener_historial_login_usuario(
    usuario_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """👤 Historial de autenticación de un usuario"""
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            return ResponseModel.error(message="Usuario no encontrado", status_code=404)
        
        logs = db.query(LoginLog).filter(
            LoginLog.id_usuario == usuario_id
        ).order_by(desc(LoginLog.fecha_hora)).limit(limit).all()
        
        logs_data = [{
            "id_log": log.id_log,
            "fecha_hora": log.fecha_hora.isoformat() if log.fecha_hora else None,
            "estado": log.estado,
            "ip_address": log.ip_address,
            "navegador": _extraer_navegador(log.user_agent),
            "icono": "🟢" if log.estado == 'exitoso' else "🔴"
        } for log in logs]
        
        return ResponseModel.success(
            message="Historial obtenido",
            data={"usuario": usuario.usuario, "historial": logs_data},
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return ResponseModel.error(message="Error al obtener historial", status_code=500)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def _obtener_icono_accion(accion: str) -> str:
    """Obtener icono según tipo de acción"""
    accion_lower = accion.lower()
    if 'crear' in accion_lower or 'login' in accion_lower:
        return "🟢"
    elif 'editar' in accion_lower or 'actualizar' in accion_lower:
        return "🔵"
    elif 'eliminar' in accion_lower or 'logout' in accion_lower:
        return "🔴"
    elif 'asignar' in accion_lower or 'revocar' in accion_lower:
        return "🟡"
    return "⚪"

def _calcular_estadisticas_login(db: Session, fecha_inicio: Optional[str], fecha_fin: Optional[str]) -> dict:
    """Calcular estadísticas de login"""
    query = db.query(LoginLog)
    if fecha_inicio:
        query = query.filter(LoginLog.fecha_hora >= datetime.fromisoformat(fecha_inicio))
    if fecha_fin:
        query = query.filter(LoginLog.fecha_hora <= datetime.fromisoformat(fecha_fin))
    
    total = query.count()
    exitosos = query.filter(LoginLog.estado == 'exitoso').count()
    fallidos = query.filter(LoginLog.estado == 'fallido').count()
    
    return {
        "total_intentos": total,
        "exitosos": exitosos,
        "fallidos": fallidos,
        "tasa_exito": round((exitosos / total * 100), 2) if total > 0 else 0
    }

def _extraer_navegador(user_agent: str) -> str:
    """Extraer navegador del user agent"""
    if not user_agent:
        return "Desconocido"
    ua = user_agent.lower()
    if 'firefox' in ua:
        return "Firefox"
    elif 'chrome' in ua and 'edg' not in ua:
        return "Chrome"
    elif 'safari' in ua and 'chrome' not in ua:
        return "Safari"
    elif 'edg' in ua:
        return "Edge"
    return "Otro"

def _extraer_sistema_operativo(user_agent: str) -> str:
    """Extraer sistema operativo"""
    if not user_agent:
        return "Desconocido"
    ua = user_agent.lower()
    if 'windows' in ua:
        return "Windows"
    elif 'mac' in ua:
        return "macOS"
    elif 'linux' in ua:
        return "Linux"
    elif 'android' in ua:
        return "Android"
    elif 'iphone' in ua or 'ipad' in ua:
        return "iOS"
    return "Otro"