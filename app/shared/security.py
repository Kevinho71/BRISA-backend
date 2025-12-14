"""
app/shared/security
Módulo de seguridad con manejo robusto de contraseñas
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import hashlib
import logging

logger = logging.getLogger(__name__)

# Configuración
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_cambiar_en_produccion")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Límite de bcrypt (72 bytes menos margen de seguridad)
BCRYPT_MAX_BYTES = 72

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def _normalize_password(password: str) -> str:
    """
    Normalizar contraseña para bcrypt.
    Si excede 72 bytes, usar SHA256 para reducir tamaño.
    
    IMPORTANTE: SHA256 es criptográficamente seguro y produce
    un hash de longitud fija (64 caracteres hex) sin importar
    la longitud de entrada.
    """
    password_bytes = password.encode('utf-8')
    
    # Si la contraseña es muy larga, usar SHA256 primero
    if len(password_bytes) > BCRYPT_MAX_BYTES:
        # SHA256 reduce cualquier longitud a 64 caracteres hex
        return hashlib.sha256(password_bytes).hexdigest()
    
    return password


def hash_password(password: str) -> str:
    """
    Encriptar contraseña con bcrypt.
    Maneja automáticamente contraseñas largas usando SHA256 pre-hash.
    """
    try:
        normalized_password = _normalize_password(password)
        return pwd_context.hash(normalized_password)
    except Exception as e:
        logger.error(f"Error al hashear contraseña: {str(e)}")
        raise ValueError("Error al procesar contraseña")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar contraseña contra hash.
    Maneja automáticamente contraseñas largas con el mismo
    pre-procesamiento que hash_password.
    """
    try:
        normalized_password = _normalize_password(plain_password)
        return pwd_context.verify(normalized_password, hashed_password)
    except Exception as e:
        logger.error(f"Error al verificar contraseña: {str(e)}")
        return False


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Crear token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Manejar sub y usuario_id para compatibilidad
    if "sub" in to_encode:
        # JWT spec requiere sub como string
        to_encode["sub"] = str(to_encode["sub"])
        # Mantener usuario_id como int para uso interno
        if "usuario_id" not in to_encode:
            to_encode["usuario_id"] = int(to_encode["sub"]) if to_encode["sub"].isdigit() else to_encode["sub"]
    elif "usuario_id" in to_encode:
        to_encode["sub"] = str(to_encode["usuario_id"])

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verificar y decodificar token JWT"""
    
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Buscar usuario_id en payload (puede estar en 'sub' o 'usuario_id')
        usuario_id = payload.get("usuario_id") or payload.get("sub")
        
        # Convertir a int si es string
        if isinstance(usuario_id, str) and usuario_id.isdigit():
            usuario_id = int(usuario_id)
        
        if usuario_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return {"usuario_id": usuario_id, "payload": payload}
    
    except JWTError as e:
        logger.warning(f"Token JWT inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado o inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )


def validate_password_complexity(password: str) -> bool:
    """
    Validar complejidad de contraseña.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Validar fortaleza de contraseña con mensajes detallados.
    
    Returns:
        tuple: (es_valida: bool, errores: list[str])
    """
    errores = []
    
    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres")
    
    if not any(c.isupper() for c in password):
        errores.append("La contraseña debe contener al menos una mayúscula")
    
    if not any(c.islower() for c in password):
        errores.append("La contraseña debe contener al menos una minúscula")
    
    if not any(c.isdigit() for c in password):
        errores.append("La contraseña debe contener al menos un número")
    
    # Opcional: validar caracteres especiales
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        # No es error, solo advertencia
        pass
    
    # Opcional: verificar contraseñas comunes
    contraseñas_comunes = ["password", "12345678", "qwerty", "admin"]
    if password.lower() in contraseñas_comunes:
        errores.append("La contraseña es demasiado común")
    
    return (len(errores) == 0, errores)