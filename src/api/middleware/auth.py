"""
Middleware de autenticación JWT.

Proporciona:
- Generación de tokens JWT
- Validación de tokens
- Dependencias para rutas protegidas
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

# Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET", "tu_secret_key_super_segura_aqui")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT.
    
    Args:
        data: Datos a incluir en el token (usuario_id, username, es_admin)
        expires_delta: Tiempo de expiración opcional
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodifica y valida un token JWT.
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        Datos del token decodificado
        
    Raises:
        HTTPException: Si el token es inválido o expiró
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependencia para obtener el usuario actual del token JWT.
    
    Args:
        credentials: Credenciales HTTP Bearer
        
    Returns:
        Datos del usuario (usuario_id, username, es_admin)
        
    Raises:
        HTTPException: Si el token es inválido
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    usuario_id: int = payload.get("usuario_id")
    username: str = payload.get("username")
    es_admin: bool = payload.get("es_admin", False)
    
    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "usuario_id": usuario_id,
        "username": username,
        "es_admin": es_admin
    }


async def get_current_admin(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependencia para rutas que requieren privilegios de administrador.
    
    Args:
        current_user: Usuario actual obtenido del token
        
    Returns:
        Datos del usuario administrador
        
    Raises:
        HTTPException: Si el usuario no es administrador
    """
    if not current_user.get("es_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    
    return current_user
