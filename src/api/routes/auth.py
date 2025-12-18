"""
Rutas de autenticación (login, registro).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import bcrypt

from src.api.server import get_db
from src.api.middleware.auth import create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    """Modelo para solicitud de login."""
    username: str
    password: str


class RegisterRequest(BaseModel):
    """Modelo para solicitud de registro."""
    username: str
    password: str
    nombre: str


class LoginResponse(BaseModel):
    """Modelo para respuesta de login."""
    success: bool
    message: str
    token: str
    usuario: dict


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db=Depends(get_db)):
    """
    Endpoint de login.
    
    Valida las credenciales y retorna un token JWT.
    """
    # Buscar usuario
    user = db.fetch_one(
        'SELECT id, username, password, nombre, es_admin FROM usuarios WHERE username = %s',
        (credentials.username,)
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Validar contraseña
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Crear token JWT
    token_data = {
        "usuario_id": user['id'],
        "username": user['username'],
        "es_admin": user['es_admin']
    }
    access_token = create_access_token(data=token_data)
    
    return {
        "success": True,
        "message": "Login exitoso",
        "token": access_token,
        "usuario": {
            "id": user['id'],
            "username": user['username'],
            "nombre": user['nombre'],
            "es_admin": user['es_admin']
        }
    }


@router.post("/register")
async def register(data: RegisterRequest, db=Depends(get_db)):
    """
    Endpoint de registro de nuevos usuarios.
    
    Crea un nuevo usuario (cobrador) en el sistema.
    """
    # Verificar que el username no exista
    existing = db.fetch_one(
        'SELECT id FROM usuarios WHERE username = %s',
        (data.username,)
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe"
        )
    
    # Hash de la contraseña
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
    
    # Insertar usuario
    db.execute('''
        INSERT INTO usuarios (username, password, nombre, es_admin)
        VALUES (%s, %s, %s, %s)
    ''', (data.username, hashed_password.decode('utf-8'), data.nombre, False))
    
    return {
        "success": True,
        "message": "Usuario registrado exitosamente"
    }


@router.post("/logout")
async def logout():
    """
    Endpoint de logout.
    
    En JWT, el logout se maneja en el cliente eliminando el token.
    Este endpoint es principalmente informativo.
    """
    return {
        "success": True,
        "message": "Sesión cerrada exitosamente"
    }
