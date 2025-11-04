"""
Decoradores compartidos para el sistema BRISA Backend
"""
from functools import wraps
from typing import List, Optional
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError
import jwt
from datetime import datetime, timedelta

async def get_token_from_request(request: Request) -> str:
    """Extrae el token JWT del header Authorization"""
    authorization = request.headers.get("Authorization")
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(request: Request = None):
    """
    Dependency para obtener el usuario actual autenticado.
    Implementado por el Módulo 1.
    """
    if request is None:
        raise HTTPException(status_code=401, detail="No request context")
    
    try:
        token = await get_token_from_request(request)
        # Esta función será completamente implementada por usuarios/auth_service.py
        # Por ahora es un stub
        return {"id": 1, "email": "user@example.com", "roles": []}
    except HTTPException:
        raise


async def require_auth():
    """Verificar que el usuario esté autenticado"""
    pass


def require_permissions(*permissions: str):
    """Dependency para requerir permisos específicos"""
    async def dependency():
        pass
    return dependency


def require_roles(*roles: str):
    """Dependency para requerir roles específicos"""
    async def dependency():
        pass
    return dependency
