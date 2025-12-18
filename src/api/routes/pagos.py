"""
Rutas de gestión de pagos.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal

from src.api.server import get_db
from src.api.middleware.auth import get_current_user

router = APIRouter()


def actualizar_estado_cliente(db, cliente_id: int):
    """
    Actualiza el estado del cliente según su saldo pendiente.
    
    Estados:
    - 'pagado': Si el total pagado >= total a pagar
    - 'activo': Si tiene saldo pendiente
    """
    # Obtener información del cliente
    cliente = db.fetch_one(
        '''SELECT monto_prestado, tasa_interes, seguro FROM clientes WHERE id = %s''',
        (cliente_id,)
    )
    
    if not cliente:
        return
    
    # Calcular total a pagar (monto + interés, sin seguro ya que es descuento automático)
    monto = float(cliente['monto_prestado'])
    interes = monto * float(cliente['tasa_interes'])
    seguro = float(cliente['seguro'])
    total_a_pagar = monto + interes
    
    # Calcular total pagado
    total_pagado_result = db.fetch_one(
        'SELECT COALESCE(SUM(monto), 0) as total FROM pagos WHERE cliente_id = %s',
        (cliente_id,)
    )
    total_pagado = float(total_pagado_result['total']) if total_pagado_result else 0.0
    
    # Actualizar estado
    nuevo_estado = 'pagado' if total_pagado >= total_a_pagar else 'activo'
    
    db.execute(
        'UPDATE clientes SET estado = %s WHERE id = %s',
        (nuevo_estado, cliente_id)
    )


class PagoRequest(BaseModel):
    """Modelo para registrar un pago."""
    cliente_id: int
    monto: float
    tipo_pago: str  # 'efectivo' o 'digital'
    fecha: Optional[date] = None


class PagoResponse(BaseModel):
    """Modelo de respuesta de pago."""
    id: int
    cliente_id: int
    fecha: date
    monto: float
    tipo_pago: str
    cliente_nombre: Optional[str] = None


@router.get("/", response_model=List[PagoResponse])
async def list_pagos(
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicial"),
    fecha_fin: Optional[date] = Query(None, description="Fecha final"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Lista todos los pagos del usuario actual con filtros opcionales."""
    usuario_id = current_user['usuario_id']
    
    # Construir query dinámicamente según filtros
    query = '''
        SELECT p.id, p.cliente_id, p.fecha, p.monto, p.tipo_pago, c.nombre as cliente_nombre
        FROM pagos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE c.usuario_id = %s
    '''
    params = [usuario_id]
    
    if cliente_id:
        query += ' AND p.cliente_id = %s'
        params.append(cliente_id)
    
    if fecha_inicio:
        query += ' AND p.fecha >= %s'
        params.append(fecha_inicio)
    
    if fecha_fin:
        query += ' AND p.fecha <= %s'
        params.append(fecha_fin)
    
    query += ' ORDER BY p.fecha DESC, p.id DESC'
    
    pagos = db.fetch_all(query, tuple(params))
    return pagos


@router.get("/cliente/{cliente_id}", response_model=List[PagoResponse])
async def get_pagos_by_cliente(
    cliente_id: int,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Obtiene todos los pagos de un cliente específico."""
    usuario_id = current_user['usuario_id']
    
    # Verificar que el cliente pertenezca al usuario
    cliente = db.fetch_one(
        'SELECT id FROM clientes WHERE id = %s AND usuario_id = %s',
        (cliente_id, usuario_id)
    )
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Obtener pagos
    pagos = db.fetch_all(
        '''SELECT p.id, p.cliente_id, p.fecha, p.monto, p.tipo_pago, c.nombre as cliente_nombre
           FROM pagos p
           JOIN clientes c ON p.cliente_id = c.id
           WHERE p.cliente_id = %s
           ORDER BY p.fecha DESC''',
        (cliente_id,)
    )
    
    return pagos


@router.post("/", response_model=PagoResponse)
async def create_pago(
    data: PagoRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Registra un nuevo pago."""
    usuario_id = current_user['usuario_id']
    
    # Verificar que el cliente pertenezca al usuario
    cliente = db.fetch_one(
        'SELECT id, nombre FROM clientes WHERE id = %s AND usuario_id = %s',
        (data.cliente_id, usuario_id)
    )
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Usar fecha actual si no se proporciona
    fecha = data.fecha or date.today()
    
    # Insertar pago
    db.execute('''
        INSERT INTO pagos (cliente_id, fecha, monto, tipo_pago)
        VALUES (%s, %s, %s, %s)
    ''', (data.cliente_id, fecha, data.monto, data.tipo_pago))
    
    # Actualizar estado del cliente según el saldo
    actualizar_estado_cliente(db, data.cliente_id)
    
    # Obtener pago creado
    pago = db.fetch_one(
        '''SELECT p.id, p.cliente_id, p.fecha, p.monto, p.tipo_pago, c.nombre as cliente_nombre
           FROM pagos p
           JOIN clientes c ON p.cliente_id = c.id
           WHERE p.cliente_id = %s
           ORDER BY p.id DESC LIMIT 1''',
        (data.cliente_id,)
    )
    
    return pago


@router.delete("/{pago_id}")
async def delete_pago(
    pago_id: int,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Elimina un pago."""
    usuario_id = current_user['usuario_id']
    
    # Verificar que el pago exista y pertenezca a un cliente del usuario
    pago = db.fetch_one(
        '''SELECT p.id FROM pagos p
           JOIN clientes c ON p.cliente_id = c.id
           WHERE p.id = %s AND c.usuario_id = %s''',
        (pago_id, usuario_id)
    )
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    # Eliminar pago
    db.execute('DELETE FROM pagos WHERE id = %s', (pago_id,))
    
    return {
        "success": True,
        "message": "Pago eliminado exitosamente"
    }


@router.get("/resumen/hoy")
async def get_resumen_hoy(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Obtiene el resumen de cobros del día actual."""
    usuario_id = current_user['usuario_id']
    fecha_hoy = date.today()
    
    # Total cobrado hoy
    result = db.fetch_one(
        '''SELECT 
            COALESCE(SUM(CASE WHEN p.tipo_pago = 'efectivo' THEN p.monto ELSE 0 END), 0) as efectivo,
            COALESCE(SUM(CASE WHEN p.tipo_pago = 'digital' THEN p.monto ELSE 0 END), 0) as digital,
            COALESCE(SUM(p.monto), 0) as total,
            COUNT(p.id) as num_pagos
           FROM pagos p
           JOIN clientes c ON p.cliente_id = c.id
           WHERE c.usuario_id = %s AND p.fecha = %s''',
        (usuario_id, fecha_hoy)
    )
    
    # Clientes activos
    clientes_activos = db.fetch_one(
        '''SELECT COUNT(*) as total
           FROM clientes
           WHERE usuario_id = %s AND estado = 'activo' ''',
        (usuario_id,)
    )
    
    return {
        "fecha": fecha_hoy.isoformat(),
        "efectivo": float(result['efectivo']),
        "digital": float(result['digital']),
        "total_cobrado": float(result['total']),
        "num_pagos": result['num_pagos'],
        "clientes_activos": clientes_activos['total']
    }


@router.get("/resumen/semanal")
async def get_resumen_semanal(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Obtiene el resumen de cobros de la semana actual."""
    usuario_id = current_user['usuario_id']
    
    # Obtener cobros de la semana
    result = db.fetch_one(
        '''SELECT 
            COALESCE(SUM(CASE WHEN p.tipo_pago = 'efectivo' THEN p.monto ELSE 0 END), 0) as efectivo,
            COALESCE(SUM(CASE WHEN p.tipo_pago = 'digital' THEN p.monto ELSE 0 END), 0) as digital,
            COALESCE(SUM(p.monto), 0) as total,
            COUNT(DISTINCT p.cliente_id) as clientes_pagaron
           FROM pagos p
           JOIN clientes c ON p.cliente_id = c.id
           WHERE c.usuario_id = %s 
           AND p.fecha >= DATE_TRUNC('week', CURRENT_DATE)''',
        (usuario_id,)
    )
    
    # Gastos de la semana
    gastos = db.fetch_one(
        '''SELECT COALESCE(SUM(monto), 0) as total
           FROM gastos_semanales
           WHERE usuario_id = %s
           AND fecha >= DATE_TRUNC('week', CURRENT_DATE)''',
        (usuario_id,)
    )
    
    # Base semanal
    base = db.fetch_one(
        '''SELECT COALESCE(SUM(monto), 0) as total
           FROM bases_semanales
           WHERE usuario_id = %s
           AND fecha >= DATE_TRUNC('week', CURRENT_DATE)''',
        (usuario_id,)
    )
    
    return {
        "efectivo": float(result['efectivo']),
        "digital": float(result['digital']),
        "total_cobrado": float(result['total']),
        "clientes_pagaron": result['clientes_pagaron'],
        "gastos": float(gastos['total']),
        "base": float(base['total']),
        "neto": float(result['total']) - float(gastos['total'])
    }
