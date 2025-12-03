"""
app/shared/permission_mapper.py - VERSIÓN CON MÓDULOS
Mapeo de acciones específicas a permisos genéricos + módulos

CAMBIO CLAVE: 
- Antes: solo validaba permisos genéricos (Lectura, Agregar, etc)
- Ahora: valida permiso genérico + módulo específico
"""
from typing import Dict, List, Set, Tuple
from app.modules.usuarios.models.usuario_models import Usuario
import logging

logger = logging.getLogger(__name__)


# ================ MAPEO: ACCIÓN → (PERMISO_GENÉRICO, MÓDULO) ================ 

PERMISSION_MAP: Dict[str, Tuple[List[str], str]] = {
    # Formato: "accion": (["permisos_genericos"], "modulo")
    
    # ============ MÓDULO USUARIOS ============
    "crear_usuario": (["Agregar"], "usuarios"),
    "ver_usuario": (["Lectura"], "usuarios"),
    "editar_usuario": (["Modificar"], "usuarios"),
    "eliminar_usuario": (["Eliminar"], "usuarios"),
    
    # ============ MÓDULO PERSONAS ============
    "crear_persona": (["Agregar"], "usuarios"),  # Las personas están en módulo usuarios
    "ver_personas": (["Lectura"], "usuarios"),
    "editar_persona": (["Modificar"], "usuarios"),
    "eliminar_persona": (["Eliminar"], "usuarios"),
    
    # ============ MÓDULO ROLES ============
    "crear_rol": (["Agregar"], "usuarios"),  # Gestión de roles está en usuarios
    "ver_rol": (["Lectura"], "usuarios"),
    "editar_rol": (["Modificar"], "usuarios"),
    "eliminar_rol": (["Eliminar"], "usuarios"),
    "asignar_permisos": (["Modificar"], "usuarios"),
    
    # ============ MÓDULO ESQUELAS ============
    "crear_esquela": (["Agregar"], "esquelas"),
    "ver_esquela": (["Lectura"], "esquelas"),
    "editar_esquela": (["Modificar"], "esquelas"),
    "eliminar_esquela": (["Eliminar"], "esquelas"),
    
    # ============ MÓDULO INCIDENTES ============
    "crear_incidente": (["Agregar"], "incidentes"),
    "ver_incidente": (["Lectura"], "incidentes"),
    "editar_incidente": (["Modificar"], "incidentes"),
    "eliminar_incidente": (["Eliminar"], "incidentes"),
    
    # ============ MÓDULO RETIROS TEMPRANOS ============
    "crear_retiro": (["Agregar"], "retiros_tempranos"),
    "ver_retiro": (["Lectura"], "retiros_tempranos"),
    "editar_retiro": (["Modificar"], "retiros_tempranos"),
    "eliminar_retiro": (["Eliminar"], "retiros_tempranos"),
    
    # ============ MÓDULO REPORTES ============
    "ver_reportes": (["Lectura"], "reportes"),
    "generar_reportes": (["Agregar"], "reportes"),
    "exportar_reportes": (["Modificar"], "reportes"),
    
    # ============ MÓDULO PROFESORES ============
    "crear_profesor": (["Agregar"], "profesores"),
    "ver_profesor": (["Lectura"], "profesores"),
    "editar_profesor": (["Modificar"], "profesores"),
    "eliminar_profesor": (["Eliminar"], "profesores"),
    "asignar_materia": (["Modificar"], "profesores"),
    
    # ============ MÓDULO ADMINISTRACIÓN ============
    "ver_bitacora": (["Lectura"], "administracion"),
    "gestionar_sistema": (["Modificar"], "administracion"),
    "configurar_sistema": (["Modificar", "Agregar"], "administracion"),
}


# ================ ROLES CON ACCESO TOTAL ================ 

ADMIN_ROLES = ["Director", "Admin"]


def tiene_permiso(usuario: Usuario, accion: str) -> bool:
    """
    Verificar si un usuario tiene permiso para realizar una acción
    AHORA VALIDA: permiso genérico + módulo correcto
    
    Args:
        usuario: Instancia del usuario
        accion: Acción a verificar (ej: "editar_usuario", "crear_incidente")
    
    Returns:
        bool: True si tiene permiso, False si no
    
    Lógica:
        1. Si el usuario tiene rol "Director" o "Admin" -> acceso total
        2. Buscar en PERMISSION_MAP: accion → (permisos_genericos, modulo)
        3. Verificar que el usuario tenga:
           - Al menos UNO de los permisos genéricos requeridos
           - Y que ese permiso sea del módulo correcto
    """
    if not usuario or not hasattr(usuario, 'roles'):
        logger.warning(f"Usuario sin roles intentando acción: {accion}")
        return False
    
    # DEBUG: Roles del usuario
    roles_usuario = [r.nombre for r in usuario.roles if r.is_active]
    logger.debug(f"Usuario {usuario.usuario} tiene roles: {roles_usuario}")
    
    # 1. Verificar si tiene un rol de administrador (acceso total)
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        if rol.nombre in ADMIN_ROLES:
            logger.debug(f"✅ Usuario {usuario.usuario} tiene rol admin: {rol.nombre}")
            return True
    
    # 2. Buscar el mapeo de la acción
    mapeo = PERMISSION_MAP.get(accion)
    
    if not mapeo:
        logger.warning(f"❌ Acción no mapeada: {accion}")
        return False
    
    permisos_requeridos, modulo_requerido = mapeo
    
    logger.debug(f"Acción '{accion}' requiere:")
    logger.debug(f"  - Permisos: {permisos_requeridos}")
    logger.debug(f"  - Módulo: {modulo_requerido}")
    
    # 3. Obtener permisos del usuario (con módulo)
    permisos_usuario: Set[Tuple[str, str]] = set()  # Set de (permiso_nombre, modulo)
    
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active:
                permisos_usuario.add((permiso.nombre, permiso.modulo))
    
    logger.debug(f"Permisos del usuario: {permisos_usuario}")
    
    # 4. Verificar si el usuario tiene el permiso correcto en el módulo correcto
    for permiso_req in permisos_requeridos:
        # Buscar tupla (permiso_req, modulo_requerido) en permisos_usuario
        if (permiso_req, modulo_requerido) in permisos_usuario:
            logger.debug(f"✅ PERMISO CONCEDIDO: {permiso_req} en módulo {modulo_requerido}")
            return True
    
    logger.warning(f"❌ Usuario {usuario.usuario} NO tiene permisos para: {accion}")
    logger.warning(f"   Necesita: {permisos_requeridos} en módulo '{modulo_requerido}'")
    return False


def obtener_permisos_usuario(usuario: Usuario) -> List[Dict[str, str]]:
    """
    Obtener lista de todos los permisos de un usuario (con módulo)
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Lista de diccionarios con formato:
        [
            {"permiso": "Lectura", "modulo": "usuarios"},
            {"permiso": "Agregar", "modulo": "esquelas"},
            ...
        ]
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return []
    
    permisos: Set[Tuple[str, str]] = set()
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active:
                permisos.add((permiso.nombre, permiso.modulo))
    
    return [
        {"permiso": p[0], "modulo": p[1]} 
        for p in permisos
    ]


def obtener_acciones_usuario(usuario: Usuario) -> List[str]:
    """
    Obtener lista de acciones específicas que puede realizar un usuario
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Lista de acciones (ej: ["crear_usuario", "ver_incidente"])
    """
    if not usuario:
        return []
    
    acciones = []
    for accion in PERMISSION_MAP.keys():
        if tiene_permiso(usuario, accion):
            acciones.append(accion)
    
    return acciones


def obtener_modulos_permitidos(usuario: Usuario) -> List[str]:
    """
    Obtener lista de módulos a los que el usuario tiene acceso
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Lista de módulos únicos
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return []
    
    modulos: Set[str] = set()
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active:
                modulos.add(permiso.modulo)
    
    return list(modulos)


def puede_acceder_modulo(usuario: Usuario, modulo: str) -> bool:
    """
    Verificar si un usuario tiene al menos UN permiso en un módulo
    
    Args:
        usuario: Instancia del usuario
        modulo: Nombre del módulo (ej: "usuarios", "incidentes")
    
    Returns:
        bool: True si tiene al menos un permiso en ese módulo
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return False
    
    # Administradores tienen acceso a todo
    if es_administrador(usuario):
        return True
    
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active and permiso.modulo == modulo:
                return True
    
    return False


def es_administrador(usuario: Usuario) -> bool:
    """
    Verificar si el usuario tiene un rol de administrador
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        bool: True si es administrador
    """
    if not usuario or not hasattr(usuario, 'roles'):
        logger.warning("es_administrador: usuario sin roles")
        return False
    
    roles_usuario = []
    for rol in usuario.roles:
        if rol.is_active:
            roles_usuario.append(rol.nombre)
            if rol.nombre in ADMIN_ROLES:
                logger.debug(f"✅ Usuario {usuario.usuario} ES administrador con rol: {rol.nombre}")
                return True
    
    logger.debug(f"❌ Usuario {usuario.usuario} NO es admin. Roles: {roles_usuario}")
    return False


def puede_modificar_usuario(usuario_actual: Usuario, usuario_objetivo_id: int) -> bool:
    """
    Verificar si un usuario puede modificar a otro usuario
    
    Reglas:
    1. Un usuario puede modificar su propio perfil
    2. Un administrador puede modificar a cualquier usuario
    3. Un usuario con permiso "Modificar" en módulo "usuarios" puede modificar a otros
    
    Args:
        usuario_actual: Usuario que intenta hacer la modificación
        usuario_objetivo_id: ID del usuario a modificar
    
    Returns:
        bool: True si puede modificar
    """
    if not usuario_actual:
        logger.warning("puede_modificar_usuario: usuario_actual es None")
        return False
    
    # Puede modificar su propio perfil
    if usuario_actual.id_usuario == usuario_objetivo_id:
        logger.debug(f"Usuario {usuario_actual.usuario} modificando su propio perfil")
        return True
    
    # Administradores pueden modificar a cualquiera
    if es_administrador(usuario_actual):
        logger.debug(f"✅ Admin {usuario_actual.usuario} puede modificar usuario {usuario_objetivo_id}")
        return True
    
    # Verificar si tiene permiso específico
    tiene_perm = tiene_permiso(usuario_actual, "editar_usuario")
    logger.debug(f"¿Usuario {usuario_actual.usuario} tiene permiso editar_usuario? {tiene_perm}")
    
    return tiene_perm


def puede_eliminar_usuario(usuario_actual: Usuario, usuario_objetivo_id: int) -> bool:
    """
    Verificar si un usuario puede eliminar a otro usuario
    
    Reglas:
    1. Nadie puede eliminarse a sí mismo
    2. Solo administradores o usuarios con permiso "Eliminar" en módulo "usuarios"
    
    Args:
        usuario_actual: Usuario que intenta eliminar
        usuario_objetivo_id: ID del usuario a eliminar
    
    Returns:
        bool: True si puede eliminar
    """
    if not usuario_actual:
        return False
    
    # No puede eliminarse a sí mismo
    if usuario_actual.id_usuario == usuario_objetivo_id:
        return False
    
    # Administradores pueden eliminar
    if es_administrador(usuario_actual):
        return True
    
    # Verificar si tiene permiso específico
    return tiene_permiso(usuario_actual, "eliminar_usuario")


# ================ HELPERS PARA FRONTEND ================ 

def obtener_permisos_por_modulo(usuario: Usuario) -> Dict[str, List[str]]:
    """
    Agrupar permisos del usuario por módulo (útil para el frontend)
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Diccionario: {
            "usuarios": ["Lectura", "Agregar"],
            "incidentes": ["Lectura", "Modificar"],
            ...
        }
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return {}
    
    permisos_por_modulo: Dict[str, Set[str]] = {}
    
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active:
                if permiso.modulo not in permisos_por_modulo:
                    permisos_por_modulo[permiso.modulo] = set()
                permisos_por_modulo[permiso.modulo].add(permiso.nombre)
    
    # Convertir sets a listas
    return {
        modulo: list(permisos) 
        for modulo, permisos in permisos_por_modulo.items()
    }


def tiene_permiso_completo_modulo(usuario: Usuario, modulo: str) -> bool:
    """
    Verificar si el usuario tiene TODOS los permisos en un módulo
    (Lectura, Agregar, Modificar, Eliminar)
    
    Args:
        usuario: Instancia del usuario
        modulo: Nombre del módulo
    
    Returns:
        bool: True si tiene los 4 permisos
    """
    permisos_completos = {"Lectura", "Agregar", "Modificar", "Eliminar"}
    
    if es_administrador(usuario):
        return True
    
    permisos_usuario = set()
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active and permiso.modulo == modulo:
                permisos_usuario.add(permiso.nombre)
    
    return permisos_completos.issubset(permisos_usuario)