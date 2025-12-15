"""
app/shared/security.py
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

# Límite de bcrypt
BCRYPT_MAX_BYTES = 72

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def _normalize_password(password: str) -> str:
    """
    Normalizar contraseña para bcrypt.
    Si excede 72 bytes, usar SHA256 para reducir tamaño.
    """
    password_bytes = password.encode('utf-8')
    
    if len(password_bytes) > BCRYPT_MAX_BYTES:
        return hashlib.sha256(password_bytes).hexdigest()
    
    return password


def hash_password(password: str) -> str:
    """Encriptar contraseña con bcrypt"""
    try:
        normalized_password = _normalize_password(password)
        return pwd_context.hash(normalized_password)
    except Exception as e:
        logger.error(f"Error al hashear contraseña: {str(e)}")
        raise ValueError("Error al procesar contraseña")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña contra hash"""
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
        to_encode["sub"] = str(to_encode["sub"])
        if "usuario_id" not in to_encode:
            to_encode["usuario_id"] = int(to_encode["sub"]) if str(to_encode["sub"]).isdigit() else to_encode["sub"]
    elif "usuario_id" in to_encode:
        to_encode["sub"] = str(to_encode["usuario_id"])

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    ✅ FUNCIÓN PARA EL MIDDLEWARE (recibe string)
    Verificar y decodificar token JWT
    
    Args:
        token: String del token JWT
    
    Returns:
        dict con payload decodificado
        
    Raises:
        HTTPException si el token es inválido
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Buscar usuario_id en payload
        usuario_id = payload.get("usuario_id") or payload.get("sub")
        
        # Convertir a int si es string
        if isinstance(usuario_id, str) and usuario_id.isdigit():
            usuario_id = int(usuario_id)
        
        if usuario_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta identificador de usuario",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return payload
    
    except jwt.ExpiredSignatureError:
        logger.warning("Token JWT expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except JWTError as e:
        logger.warning(f"Token JWT inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def verify_token_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    ✅ FUNCIÓN PARA DEPENDENCY INJECTION (recibe HTTPAuthorizationCredentials)
    Verificar y decodificar token JWT para uso en endpoints
    
    Args:
        credentials: Credenciales extraídas por FastAPI Security
    
    Returns:
        dict: {"usuario_id": int, "payload": dict}
        
    Raises:
        HTTPException si el token es inválido
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Buscar usuario_id en payload
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
    
    except jwt.ExpiredSignatureError:
        logger.warning("Token JWT expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except JWTError as e:
        logger.warning(f"Token JWT inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
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
    
    # Opcional: verificar contraseñas comunes
    contraseñas_comunes = ["password", "12345678", "qwerty", "admin"]
    if password.lower() in contraseñas_comunes:
        errores.append("La contraseña es demasiado común")
    
    return (len(errores) == 0, errores)