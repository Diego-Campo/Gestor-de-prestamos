"""
Rutas de gestión de usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import bcrypt

from src.api.server import get_db
from src.api.middleware.auth import get_current_user, get_current_admin

router = APIRouter()


class UsuarioResponse(BaseModel):
    """Modelo de respuesta de usuario."""
    id: int
    username: str
    nombre: str
    es_admin: bool


class CreateUsuarioRequest(BaseModel):
    """Modelo para crear usuario."""
    username: str
    password: str
    nombre: str
    es_admin: bool = False


class ChangePasswordRequest(BaseModel):
    """Modelo para cambiar contraseña."""
    password_actual: str
    password_nueva: str


@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    """Obtiene información del usuario actual."""
    user = db.fetch_one(
        'SELECT id, username, nombre, es_admin FROM usuarios WHERE id = %s',
        (current_user['usuario_id'],)
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user


@router.get("/", response_model=List[UsuarioResponse])
async def list_usuarios(
    current_user: dict = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Lista todos los usuarios (solo admin)."""
    users = db.fetch_all(
        'SELECT id, username, nombre, es_admin FROM usuarios ORDER BY nombre'
    )
    return users


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    current_user: dict = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Obtiene información de un usuario específico (solo admin)."""
    user = db.fetch_one(
        'SELECT id, username, nombre, es_admin FROM usuarios WHERE id = %s',
        (usuario_id,)
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user


@router.post("/", response_model=UsuarioResponse)
async def create_usuario(
    data: CreateUsuarioRequest,
    current_user: dict = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Crea un nuevo usuario (solo admin)."""
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
    ''', (data.username, hashed_password.decode('utf-8'), data.nombre, data.es_admin))
    
    # Obtener usuario creado
    user = db.fetch_one(
        'SELECT id, username, nombre, es_admin FROM usuarios WHERE username = %s',
        (data.username,)
    )
    
    return user


@router.put("/{usuario_id}/password")
async def change_password(
    usuario_id: int,
    data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Cambia la contraseña de un usuario."""
    # Solo admin puede cambiar contraseña de otros, o el usuario su propia contraseña
    if usuario_id != current_user['usuario_id'] and not current_user['es_admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cambiar esta contraseña"
        )
    
    # Obtener usuario
    user = db.fetch_one(
        'SELECT id, password FROM usuarios WHERE id = %s',
        (usuario_id,)
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar contraseña actual (solo si no es admin cambiando otra contraseña)
    if usuario_id == current_user['usuario_id']:
        if not bcrypt.checkpw(data.password_actual.encode('utf-8'), user['password'].encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta"
            )
    
    # Hash de la nueva contraseña
    new_hashed = bcrypt.hashpw(data.password_nueva.encode('utf-8'), bcrypt.gensalt())
    
    # Actualizar contraseña
    db.execute(
        'UPDATE usuarios SET password = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s',
        (new_hashed.decode('utf-8'), usuario_id)
    )
    
    return {
        "success": True,
        "message": "Contraseña actualizada exitosamente"
    }


class BaseRequest(BaseModel):
    """Modelo para registrar base."""
    monto: float


class GastoRequest(BaseModel):
    """Modelo para registrar gasto."""
    monto: float
    descripcion: str


@router.post("/base")
async def agregar_base(
    data: BaseRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Registra la base del día para el usuario actual."""
    from datetime import datetime
    
    fecha = datetime.now().date()
    usuario_id = current_user['usuario_id']
    
    # Verificar si ya hay una base para hoy
    existing = db.fetch_one(
        'SELECT id FROM bases_semanales WHERE usuario_id = %s AND fecha = %s',
        (usuario_id, fecha)
    )
    
    if existing:
        # Actualizar la base existente
        db.execute(
            'UPDATE bases_semanales SET monto = %s WHERE usuario_id = %s AND fecha = %s',
            (data.monto, usuario_id, fecha)
        )
    else:
        # Insertar nueva base
        db.execute(
            'INSERT INTO bases_semanales (usuario_id, monto, fecha) VALUES (%s, %s, %s)',
            (usuario_id, data.monto, fecha)
        )
    
    return {
        "success": True,
        "message": "Base registrada exitosamente"
    }


@router.post("/gasto")
async def registrar_gasto(
    data: GastoRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Registra un gasto para el usuario actual."""
    from datetime import datetime
    
    fecha = datetime.now().date()
    usuario_id = current_user['usuario_id']
    
    db.execute('''
        INSERT INTO gastos_semanales (usuario_id, monto, descripcion, fecha)
        VALUES (%s, %s, %s, %s)
    ''', (usuario_id, data.monto, data.descripcion, fecha))
    
    return {
        "success": True,
        "message": "Gasto registrado exitosamente"
    }


@router.delete("/{usuario_id}")
async def delete_usuario(
    usuario_id: int,
    current_user: dict = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Elimina un usuario (solo admin)."""
    # No permitir eliminar al propio admin
    if usuario_id == current_user['usuario_id']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario"
        )
    
    # Verificar que el usuario exista
    user = db.fetch_one('SELECT id FROM usuarios WHERE id = %s', (usuario_id,))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Eliminar usuario
    db.execute('DELETE FROM usuarios WHERE id = %s', (usuario_id,))
    
    return {
        "success": True,
        "message": "Usuario eliminado exitosamente"
    }


@router.get("/cobradores/resumen")
async def get_resumen_cobradores(
    current_user: dict = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Obtiene resumen de actividad de todos los cobradores (solo admin)."""
    from datetime import date as dt_date
    hoy = dt_date.today()
    
    # Obtener todos los cobradores (no admin)
    cobradores = db.fetch_all(
        'SELECT id, username, nombre FROM usuarios WHERE es_admin = FALSE ORDER BY nombre'
    )
    
    resumen = []
    for cobrador in cobradores:
        cobrador_id = cobrador['id']
        
        # Clientes activos
        clientes = db.fetch_one(
            'SELECT COUNT(*) as total FROM clientes WHERE usuario_id = %s AND estado = %s',
            (cobrador_id, 'activo')
        )
        
        # Cobrado hoy
        cobrado_hoy = db.fetch_one(
            '''SELECT COALESCE(SUM(p.monto), 0) as total
               FROM pagos p
               JOIN clientes c ON p.cliente_id = c.id
               WHERE c.usuario_id = %s AND p.fecha = %s''',
            (cobrador_id, hoy)
        )
        
        # Base del día
        base_hoy = db.fetch_one(
            '''SELECT COALESCE(SUM(monto), 0) as total
               FROM bases_semanales
               WHERE usuario_id = %s AND fecha = %s''',
            (cobrador_id, hoy)
        )
        
        # Gastos del día
        gastos_hoy = db.fetch_one(
            '''SELECT COALESCE(SUM(monto), 0) as total
               FROM gastos_semanales
               WHERE usuario_id = %s AND fecha = %s''',
            (cobrador_id, hoy)
        )
        
        resumen.append({
            'id': cobrador_id,
            'nombre': cobrador['nombre'],
            'username': cobrador['username'],
            'clientes_activos': clientes['total'] if clientes else 0,
            'cobrado_hoy': float(cobrado_hoy['total']) if cobrado_hoy else 0.0,
            'base_hoy': float(base_hoy['total']) if base_hoy else 0.0,
            'gastos_hoy': float(gastos_hoy['total']) if gastos_hoy else 0.0
        })
    
    return resumen
