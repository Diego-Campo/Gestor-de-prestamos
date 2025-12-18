"""
Rutas de gestión de clientes y préstamos.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal

from src.api.server import get_db
from src.api.middleware.auth import get_current_user

router = APIRouter()


class ClienteRequest(BaseModel):
    """Modelo para crear/actualizar cliente."""
    nombre: str
    cedula: str
    telefono: str
    monto_prestado: float
    fecha_prestamo: date
    tipo_plazo: str
    tasa_interes: float
    seguro: float
    cuota_minima: float
    dias_plazo: int


class ClienteSimpleRequest(BaseModel):
    """Modelo simplificado para crear cliente (calcula automáticamente los campos)."""
    nombre: str
    cedula: str
    telefono: str
    monto: float
    tipo_plazo: str = "semanal"
    tasa_interes: Optional[float] = None


class ClienteResponse(BaseModel):
    """Modelo de respuesta de cliente."""
    id: int
    usuario_id: int
    nombre: str
    cedula: str
    telefono: str
    monto_prestado: float
    fecha_prestamo: date
    tipo_plazo: str
    tasa_interes: float
    seguro: float
    cuota_minima: float
    dias_plazo: int
    estado: str


class ClienteDetalladoResponse(ClienteResponse):
    """Modelo de respuesta de cliente con información adicional."""
    total_pagado: float
    saldo_pendiente: float
    dias_transcurridos: int
    total_a_pagar: float


@router.get("/", response_model=List[ClienteResponse])
async def list_clientes(
    estado: Optional[str] = Query(None, description="Filtrar por estado: activo, pagado, atrasado"),
    search: Optional[str] = Query(None, description="Buscar por nombre o cédula"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Lista todos los clientes del usuario actual."""
    usuario_id = current_user['usuario_id']
    
    # Construir query con filtros
    query = '''SELECT id, usuario_id, nombre, cedula, telefono, monto_prestado,
                      fecha_prestamo, tipo_plazo, tasa_interes, seguro, cuota_minima,
                      dias_plazo, estado
               FROM clientes
               WHERE usuario_id = %s'''
    params = [usuario_id]
    
    if estado:
        query += ' AND estado = %s'
        params.append(estado)
    
    if search:
        query += ' AND (nombre ILIKE %s OR cedula ILIKE %s)'
        search_pattern = f'%{search}%'
        params.extend([search_pattern, search_pattern])
    
    query += ' ORDER BY fecha_prestamo DESC'
    
    clientes = db.fetch_all(query, tuple(params))
    
    return clientes


@router.get("/{cliente_id}", response_model=ClienteDetalladoResponse)
async def get_cliente(
    cliente_id: int,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Obtiene información detallada de un cliente."""
    usuario_id = current_user['usuario_id']
    
    # Obtener cliente
    cliente = db.fetch_one(
        '''SELECT id, usuario_id, nombre, cedula, telefono, monto_prestado,
                  fecha_prestamo, tipo_plazo, tasa_interes, seguro, cuota_minima,
                  dias_plazo, estado
           FROM clientes
           WHERE id = %s AND usuario_id = %s''',
        (cliente_id, usuario_id)
    )
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Calcular total pagado
    total_pagado_result = db.fetch_one(
        'SELECT COALESCE(SUM(monto), 0) as total FROM pagos WHERE cliente_id = %s',
        (cliente_id,)
    )
    total_pagado = float(total_pagado_result['total']) if total_pagado_result else 0.0
    
    # Calcular total a pagar (monto + interés, sin seguro ya que es descuento automático)
    monto = float(cliente['monto_prestado'])
    interes = monto * float(cliente['tasa_interes'])
    seguro = float(cliente['seguro'])
    total_a_pagar = monto + interes
    
    # Calcular saldo pendiente
    saldo_pendiente = total_a_pagar - total_pagado
    
    # Calcular días transcurridos
    from datetime import date as dt_date
    dias_transcurridos = (dt_date.today() - cliente['fecha_prestamo']).days
    
    return {
        **cliente,
        'total_pagado': total_pagado,
        'saldo_pendiente': saldo_pendiente,
        'dias_transcurridos': dias_transcurridos,
        'total_a_pagar': total_a_pagar
    }


@router.post("/", response_model=ClienteResponse)
async def create_cliente(
    data: ClienteSimpleRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Crea un nuevo cliente con préstamo (simplificado con cálculos automáticos)."""
    from datetime import date as dt_date
    
    usuario_id = current_user['usuario_id']
    
    # Calcular campos automáticamente
    fecha_prestamo = dt_date.today()
    
    # Tasa de interés por defecto: 20%
    tasa_interes = data.tasa_interes if data.tasa_interes else 0.20
    
    # Calcular días de plazo según tipo
    plazos = {
        "diario": 1,
        "semanal": 7,
        "quincenal": 15,
        "mensual": 30
    }
    dias_plazo = plazos.get(data.tipo_plazo, 7)
    
    # Calcular cuota mínima: $2,000 por cada $50,000
    cuota_minima = (data.monto // 50000) * 2000 if data.monto >= 50000 else 2000
    
    # Seguro = una cuota mínima
    seguro = cuota_minima
    
    # Insertar cliente
    db.execute('''
        INSERT INTO clientes (
            usuario_id, nombre, cedula, telefono, monto_prestado,
            fecha_prestamo, tipo_plazo, tasa_interes, seguro,
            cuota_minima, dias_plazo, estado
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        usuario_id, data.nombre, data.cedula, data.telefono,
        data.monto, fecha_prestamo, data.tipo_plazo,
        tasa_interes, seguro, cuota_minima,
        dias_plazo, 'activo'
    ))
    
    # Obtener cliente creado
    cliente = db.fetch_one(
        '''SELECT id, usuario_id, nombre, cedula, telefono, monto_prestado,
                  fecha_prestamo, tipo_plazo, tasa_interes, seguro, cuota_minima,
                  dias_plazo, estado
           FROM clientes
           WHERE cedula = %s AND usuario_id = %s
           ORDER BY id DESC LIMIT 1''',
        (data.cedula, usuario_id)
    )
    
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update_cliente(
    cliente_id: int,
    data: ClienteRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Actualiza información de un cliente."""
    usuario_id = current_user['usuario_id']
    
    # Verificar que el cliente exista y pertenezca al usuario
    cliente = db.fetch_one(
        'SELECT id FROM clientes WHERE id = %s AND usuario_id = %s',
        (cliente_id, usuario_id)
    )
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizar cliente
    db.execute('''
        UPDATE clientes SET
            nombre = %s, cedula = %s, telefono = %s, monto_prestado = %s,
            fecha_prestamo = %s, tipo_plazo = %s, tasa_interes = %s,
            seguro = %s, cuota_minima = %s, dias_plazo = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s AND usuario_id = %s
    ''', (
        data.nombre, data.cedula, data.telefono, data.monto_prestado,
        data.fecha_prestamo, data.tipo_plazo, data.tasa_interes,
        data.seguro, data.cuota_minima, data.dias_plazo,
        cliente_id, usuario_id
    ))
    
    # Obtener cliente actualizado
    cliente_updated = db.fetch_one(
        '''SELECT id, usuario_id, nombre, cedula, telefono, monto_prestado,
                  fecha_prestamo, tipo_plazo, tasa_interes, seguro, cuota_minima,
                  dias_plazo, estado
           FROM clientes WHERE id = %s''',
        (cliente_id,)
    )
    
    return cliente_updated


@router.patch("/{cliente_id}/estado")
async def update_cliente_estado(
    cliente_id: int,
    estado: str = Query(..., description="Nuevo estado: activo, pagado, atrasado"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Actualiza el estado de un cliente."""
    usuario_id = current_user['usuario_id']
    
    # Verificar que el cliente exista
    cliente = db.fetch_one(
        'SELECT id FROM clientes WHERE id = %s AND usuario_id = %s',
        (cliente_id, usuario_id)
    )
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizar estado
    db.execute(
        'UPDATE clientes SET estado = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s',
        (estado, cliente_id)
    )
    
    return {
        "success": True,
        "message": f"Estado actualizado a '{estado}'"
    }


@router.delete("/{cliente_id}")
async def delete_cliente(
    cliente_id: int,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Elimina un cliente y todos sus pagos asociados."""
    usuario_id = current_user['usuario_id']
    
    # Verificar que el cliente exista
    cliente = db.fetch_one(
        'SELECT id FROM clientes WHERE id = %s AND usuario_id = %s',
        (cliente_id, usuario_id)
    )
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Eliminar cliente (los pagos se eliminan automáticamente por CASCADE)
    db.execute('DELETE FROM clientes WHERE id = %s', (cliente_id,))
    
    return {
        "success": True,
        "message": "Cliente eliminado exitosamente"
    }
