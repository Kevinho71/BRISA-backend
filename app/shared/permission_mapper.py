"""
app/shared/permission_mapper.py
Mapeo de permisos genéricos a acciones específicas

Como la BD usa permisos genéricos (Lectura, Agregar, Modificar, Eliminar),
este módulo traduce esos permisos a acciones específicas del sistema.
"""
from typing import Dict, List, Set
from app.modules.usuarios.models.usuario_models import Usuario

# ========================================
# MAPEO DE ACCIONES A PERMISOS GENÉRICOS
# ========================================
PERMISSION_MAP: Dict[str, List[str]] = {
    # Usuarios
    "crear_usuario": ["Agregar"],
    "ver_usuario": ["Lectura"],
    "editar_usuario": ["Modificar"],
    "eliminar_usuario": ["Eliminar"],
    
    # Personas
    "crear_persona": ["Agregar"],
    "ver_persona": ["Lectura"],
    "editar_persona": ["Modificar"],
    "eliminar_persona": ["Eliminar"],
    
    # Roles
    "crear_rol": ["Agregar"],
    "ver_rol": ["Lectura"],
    "editar_rol": ["Modificar"],
    "eliminar_rol": ["Eliminar"],
    "asignar_permisos": ["Modificar"],
    
    # Reportes
    "ver_reportes": ["Lectura"],
    "generar_reportes": ["Agregar"],
    
    # Sistema
    "gestionar_sistema": ["Modificar", "Eliminar"],
    "ver_bitacora": ["Lectura"],
}

# ========================================
# ROLES CON ACCESO TOTAL
# ========================================
ADMIN_ROLES = ["Director", "Administrativo"]


def tiene_permiso(usuario: Usuario, accion: str) -> bool:
    """
    Verificar si un usuario tiene permiso para realizar una acción
    
    Args:
        usuario: Instancia del usuario
        accion: Acción a verificar (ej: "editar_usuario", "crear_rol")
    
    Returns:
        bool: True si tiene permiso, False si no
    
    Lógica:
        1. Si el usuario tiene rol "Director" -> acceso total
        2. Si la acción requiere permisos genéricos, verificar si el usuario los tiene
        3. Si no encuentra mapeo, denegar por defecto
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return False
    
    # Verificar si tiene un rol de administrador
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        if rol.nombre in ADMIN_ROLES:
            return True
    
    # Obtener permisos genéricos requeridos para esta acción
    permisos_requeridos = PERMISSION_MAP.get(accion, [])
    
    if not permisos_requeridos:
        # Si no hay mapeo definido, denegar por defecto
        return False
    
    # Obtener todos los permisos del usuario
    permisos_usuario: Set[str] = set()
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active:
                permisos_usuario.add(permiso.nombre)
    
    # Verificar si el usuario tiene AL MENOS UNO de los permisos requeridos
    for permiso_req in permisos_requeridos:
        if permiso_req in permisos_usuario:
            return True
    
    return False


def obtener_permisos_usuario(usuario: Usuario) -> List[str]:
    """
    Obtener lista de todos los permisos de un usuario (genéricos)
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Lista de nombres de permisos
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return []
    
    permisos: Set[str] = set()
    for rol in usuario.roles:
        if not rol.is_active:
            continue
        for permiso in rol.permisos:
            if permiso.is_active:
                permisos.add(permiso.nombre)
    
    return list(permisos)


def obtener_acciones_usuario(usuario: Usuario) -> List[str]:
    """
    Obtener lista de acciones específicas que puede realizar un usuario
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Lista de acciones (ej: ["crear_usuario", "editar_usuario"])
    """
    if not usuario:
        return []
    
    acciones = []
    for accion in PERMISSION_MAP.keys():
        if tiene_permiso(usuario, accion):
            acciones.append(accion)
    
    return acciones


def es_administrador(usuario: Usuario) -> bool:
    """
    Verificar si el usuario tiene un rol de administrador
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        bool: True si es administrador
    """
    if not usuario or not hasattr(usuario, 'roles'):
        return False
    
    for rol in usuario.roles:
        if rol.is_active and rol.nombre in ADMIN_ROLES:
            return True
    
    return False


def puede_modificar_usuario(usuario_actual: Usuario, usuario_objetivo_id: int) -> bool:
    """
    Verificar si un usuario puede modificar a otro usuario
    
    Reglas:
    1. Un usuario puede modificar su propio perfil
    2. Un administrador puede modificar a cualquier usuario
    3. Un usuario con permiso "Modificar" puede modificar a otros
    
    Args:
        usuario_actual: Usuario que intenta hacer la modificación
        usuario_objetivo_id: ID del usuario a modificar
    
    Returns:
        bool: True si puede modificar
    """
    if not usuario_actual:
        return False
    
    # Puede modificar su propio perfil
    if usuario_actual.id_usuario == usuario_objetivo_id:
        return True
    
    # Administradores pueden modificar a cualquiera
    if es_administrador(usuario_actual):
        return True
    
    # Verificar si tiene permiso específico
    return tiene_permiso(usuario_actual, "editar_usuario")


def puede_eliminar_usuario(usuario_actual: Usuario, usuario_objetivo_id: int) -> bool:
    """
    Verificar si un usuario puede eliminar a otro usuario
    
    Reglas:
    1. Nadie puede eliminarse a sí mismo
    2. Solo administradores o usuarios con permiso "Eliminar"
    
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