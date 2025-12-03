"""
bitacora_controller.py -
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from app.core.database import get_db
from app.modules.auth.services.auth_service import get_current_user_dependency
from app.modules.usuarios.models.usuario_models import Usuario, LoginLog
from app.shared.response import ResponseModel
from app.shared.permissions import requires_permission

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================
# LISTAR TODOS LOS LOGIN LOGS
# ============================================================

@router.get("/login-logs", response_model=dict)
@requires_permission('ver_bitacora')
async def obtener_login_logs(
    # Filtros
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    estado: Optional[str] = Query(
        None, 
        description="Filtrar por estado: 'exitoso' o 'fallido'"
    ),
    ip_address: Optional[str] = Query(None, description="Filtrar por dirección IP"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    
    # Paginación
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    
    # Dependencias
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    🔐 Obtener logs de autenticación (LOGIN/LOGOUT)
    
    **Vista específica para seguridad:**
    - Muestra todos los intentos de login (exitosos y fallidos)
    - Incluye IP y User-Agent completos
    - Útil para detectar intentos de acceso no autorizado
    - Muestra usuarios bloqueados
    
    **Ejemplo de uso:**
    - Ver intentos fallidos: `?estado=fallido`
    - Ver accesos desde una IP: `?ip_address=192.168.1.100`
    - Ver actividad de un usuario: `?usuario_id=5`
    """
    try:

        # 1️ CONSTRUIR QUERY BASE

        query = db.query(LoginLog)
        

        # 2️ APLICAR FILTROS

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
                    message="Formato de fecha_inicio inválido. Use YYYY-MM-DD",
                    status_code=400
                )
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.fromisoformat(fecha_fin)
                # Incluir todo el día
                fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(LoginLog.fecha_hora <= fecha_fin_dt)
            except ValueError:
                return ResponseModel.error(
                    message="Formato de fecha_fin inválido. Use YYYY-MM-DD",
                    status_code=400
                )
        

        # 3️ CONTAR TOTAL

        total = query.count()
        

        # 4️ ORDENAR Y PAGINAR

        logs = query.order_by(desc(LoginLog.fecha_hora)).offset(skip).limit(limit).all()
        

        # 5️ FORMATEAR RESULTADOS

        logs_data = []
        for log in logs:
            # Obtener info del usuario
            usuario = db.query(Usuario).filter(
                Usuario.id_usuario == log.id_usuario
            ).first()
            
            # Detectar si el usuario está actualmente bloqueado
            from app.modules.auth.repositories.auth_repository import AuthRepository
            bloqueado, fecha_desbloqueo = AuthRepository.verificar_cuenta_bloqueada(
                db, log.id_usuario
            ) if log.estado == 'fallido' else (False, None)
            
            log_dict = {
                "id_log": log.id_log,
                "usuario_id": log.id_usuario,
                "usuario": usuario.usuario if usuario else "N/A",
                "nombre_completo": usuario.persona.nombre_completo if usuario and usuario.persona else "N/A",
                "fecha_hora": log.fecha_hora.isoformat() if log.fecha_hora else None,
                "estado": log.estado,
                "ip_address": log.ip_address or "N/A",
                "user_agent": log.user_agent or "N/A",
                
                # ✅ Información adicional de seguridad
                "usuario_activo": usuario.is_active if usuario else False,
                "cuenta_bloqueada": bloqueado,
                "fecha_desbloqueo": fecha_desbloqueo.isoformat() if fecha_desbloqueo else None,
                
                # ✅ Indicadores visuales
                "icono": "🟢" if log.estado == 'exitoso' else "🔴",
                "color": "success" if log.estado == 'exitoso' else "danger",
                "navegador": _extraer_navegador(log.user_agent),
                "sistema_operativo": _extraer_sistema_operativo(log.user_agent)
            }
            logs_data.append(log_dict)

        # 6️ CALCULAR ESTADÍSTICAS

        estadisticas = _calcular_estadisticas_login(db, fecha_inicio, fecha_fin)
        
        return ResponseModel.success(
            message="Login logs obtenidos",
            data={
                "logs": logs_data,
                "total": total,
                "skip": skip,
                "limit": limit,
                "paginas": (total + limit - 1) // limit if limit > 0 else 1,
                "estadisticas": estadisticas,
                "filtros_aplicados": {
                    "usuario_id": usuario_id,
                    "estado": estado,
                    "ip_address": ip_address,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
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


# ============================================================
#  ESTADÍSTICAS DE AUTENTICACIÓN
# ============================================================

@router.get("/login-logs/estadisticas", response_model=dict)
@requires_permission('ver_bitacora')
async def obtener_estadisticas_login(
    dias: int = Query(7, ge=1, le=365, description="Últimos N días"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    📊 Estadísticas de autenticación de los últimos N días
    
    **Muestra:**
    - Total de logins exitosos/fallidos
    - IPs más activas
    - Usuarios con más intentos fallidos
    - Horarios pico de actividad
    - Detección de patrones sospechosos
    """
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        # Total de intentos
        total_exitosos = db.query(LoginLog).filter(
            and_(
                LoginLog.estado == 'exitoso',
                LoginLog.fecha_hora >= fecha_inicio
            )
        ).count()
        
        total_fallidos = db.query(LoginLog).filter(
            and_(
                LoginLog.estado == 'fallido',
                LoginLog.fecha_hora >= fecha_inicio
            )
        ).count()
        
        # IPs más activas
        ips_activas = db.query(
            LoginLog.ip_address,
            func.count(LoginLog.id_log).label('intentos'),
            func.sum(func.case((LoginLog.estado == 'fallido', 1), else_=0)).label('fallidos')
        ).filter(
            LoginLog.fecha_hora >= fecha_inicio
        ).group_by(
            LoginLog.ip_address
        ).order_by(
            desc('intentos')
        ).limit(10).all()
        
        # Usuarios con más intentos fallidos
        usuarios_fallidos = db.query(
            Usuario.usuario,
            func.count(LoginLog.id_log).label('intentos_fallidos')
        ).join(
            LoginLog,
            Usuario.id_usuario == LoginLog.id_usuario
        ).filter(
            and_(
                LoginLog.estado == 'fallido',
                LoginLog.fecha_hora >= fecha_inicio
            )
        ).group_by(
            Usuario.usuario
        ).order_by(
            desc('intentos_fallidos')
        ).limit(10).all()
        
        # Actividad por hora (últimas 24h)
        hace_24h = datetime.now() - timedelta(hours=24)
        actividad_por_hora = db.query(
            func.hour(LoginLog.fecha_hora).label('hora'),
            func.count(LoginLog.id_log).label('intentos')
        ).filter(
            LoginLog.fecha_hora >= hace_24h
        ).group_by(
            'hora'
        ).order_by('hora').all()
        
        # Tasa de éxito
        total_intentos = total_exitosos + total_fallidos
        tasa_exito = (total_exitosos / total_intentos * 100) if total_intentos > 0 else 0
        
        # ⚠️ ALERTAS DE SEGURIDAD
        alertas = []
        
        # Detectar IPs con muchos intentos fallidos
        for ip, intentos, fallidos in ips_activas:
            if fallidos >= 10:
                alertas.append({
                    "tipo": "ip_sospechosa",
                    "severidad": "alta",
                    "mensaje": f"IP {ip} tiene {fallidos} intentos fallidos",
                    "ip": ip
                })
        
        # Detectar usuarios con intentos fallidos recientes
        for usuario, fallidos in usuarios_fallidos:
            if fallidos >= 5:
                alertas.append({
                    "tipo": "usuario_comprometido",
                    "severidad": "media",
                    "mensaje": f"Usuario '{usuario}' tiene {fallidos} intentos fallidos",
                    "usuario": usuario
                })
        
        return ResponseModel.success(
            message="Estadísticas de autenticación obtenidas",
            data={
                "periodo": {
                    "dias": dias,
                    "desde": fecha_inicio.isoformat(),
                    "hasta": datetime.now().isoformat()
                },
                "resumen": {
                    "total_intentos": total_intentos,
                    "exitosos": total_exitosos,
                    "fallidos": total_fallidos,
                    "tasa_exito": round(tasa_exito, 2)
                },
                "ips_activas": [
                    {
                        "ip": ip,
                        "total_intentos": intentos,
                        "intentos_fallidos": fallidos,
                        "tasa_fallo": round((fallidos / intentos * 100), 2)
                    }
                    for ip, intentos, fallidos in ips_activas
                ],
                "usuarios_con_fallos": [
                    {
                        "usuario": usuario,
                        "intentos_fallidos": fallidos
                    }
                    for usuario, fallidos in usuarios_fallidos
                ],
                "actividad_por_hora": [
                    {
                        "hora": f"{hora:02d}:00",
                        "intentos": intentos
                    }
                    for hora, intentos in actividad_por_hora
                ],
                "alertas_seguridad": alertas
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
# HISTORIAL DE LOGIN DE UN USUARIO ESPECÍFICO
# ============================================================

@router.get("/login-logs/usuario/{usuario_id}", response_model=dict)
@requires_permission('ver_bitacora')
async def obtener_historial_login_usuario(
    usuario_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user_dependency)
) -> dict:
    """
    👤 Historial de autenticación de un usuario específico
    
    **Muestra:**
    - Últimos N intentos de login (exitosos y fallidos)
    - Patrón de acceso (horarios, IPs)
    - Estado actual de la cuenta
    """
    try:
        # Verificar que el usuario existe
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
        if not usuario:
            return ResponseModel.error(
                message="Usuario no encontrado",
                status_code=404
            )
        
        # Obtener logs
        logs = db.query(LoginLog).filter(
            LoginLog.id_usuario == usuario_id
        ).order_by(desc(LoginLog.fecha_hora)).limit(limit).all()
        
        # Formatear logs
        logs_data = []
        for log in logs:
            logs_data.append({
                "id_log": log.id_log,
                "fecha_hora": log.fecha_hora.isoformat() if log.fecha_hora else None,
                "estado": log.estado,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "navegador": _extraer_navegador(log.user_agent),
                "icono": "🟢" if log.estado == 'exitoso' else "🔴"
            })
        
        # Estadísticas del usuario
        exitosos = db.query(LoginLog).filter(
            and_(
                LoginLog.id_usuario == usuario_id,
                LoginLog.estado == 'exitoso'
            )
        ).count()
        
        fallidos = db.query(LoginLog).filter(
            and_(
                LoginLog.id_usuario == usuario_id,
                LoginLog.estado == 'fallido'
            )
        ).count()
        
        ultimo_login = db.query(LoginLog).filter(
            and_(
                LoginLog.id_usuario == usuario_id,
                LoginLog.estado == 'exitoso'
            )
        ).order_by(desc(LoginLog.fecha_hora)).first()
        
        # Verificar si está bloqueado
        from app.modules.auth.repositories.auth_repository import AuthRepository
        bloqueado, fecha_desbloqueo = AuthRepository.verificar_cuenta_bloqueada(db, usuario_id)
        
        return ResponseModel.success(
            message="Historial de login obtenido",
            data={
                "usuario": {
                    "id": usuario.id_usuario,
                    "usuario": usuario.usuario,
                    "nombre_completo": usuario.persona.nombre_completo if usuario.persona else "N/A",
                    "activo": usuario.is_active,
                    "bloqueado": bloqueado,
                    "fecha_desbloqueo": fecha_desbloqueo.isoformat() if fecha_desbloqueo else None
                },
                "estadisticas": {
                    "total_logins": exitosos + fallidos,
                    "exitosos": exitosos,
                    "fallidos": fallidos,
                    "ultimo_login": ultimo_login.fecha_hora.isoformat() if ultimo_login else None,
                    "ultima_ip": ultimo_login.ip_address if ultimo_login else None
                },
                "historial": logs_data
            },
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error al obtener historial: {str(e)}", exc_info=True)
        return ResponseModel.error(
            message="Error al obtener historial",
            error_details=str(e),
            status_code=500
        )


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def _calcular_estadisticas_login(
    db: Session, 
    fecha_inicio: Optional[str] = None, 
    fecha_fin: Optional[str] = None
) -> dict:
    """Calcular estadísticas generales de login"""
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
    """Extraer nombre del navegador del user agent"""
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
    elif 'opera' in ua or 'opr' in ua:
        return "Opera"
    else:
        return "Otro"


def _extraer_sistema_operativo(user_agent: str) -> str:
    """Extraer sistema operativo del user agent"""
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
    else:
        return "Otro"