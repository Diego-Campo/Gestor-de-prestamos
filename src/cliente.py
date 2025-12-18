"""
Gestión de clientes y préstamos para PostgreSQL.

Este módulo ha sido adaptado para funcionar con PostgreSQL
en lugar de SQLite. Los métodos han sido refactorizados para
usar psycopg2 y el pool de conexiones.
"""

from datetime import datetime
from typing import List, Dict, Optional

class Cliente:
    """
    Clase para gestionar todas las operaciones relacionadas con los clientes.
    
    Esta clase maneja:
    - Registro y gestión de clientes
    - Cálculo de cuotas y montos
    - Registro de pagos
    - Seguimiento de balances
    """

    def __init__(self, db):
        """
        Inicializa el gestor de clientes.
        
        Args:
            db: Instancia de la clase Database (PostgreSQL) para operaciones con la base de datos
        """
        self.db = db

    def calcular_cuota_minima(self, monto: float) -> float:
        """
        Calcula la cuota mínima para un préstamo basado en el monto.
        
        La cuota se calcula como $2,000 por cada $50,000 prestados.
        Para montos menores a $50,000, la cuota mínima es $2,000.
        
        Args:
            monto: Cantidad del préstamo
        
        Returns:
            float: Monto de la cuota mínima
        """
        return (monto // 50000) * 2000 if monto >= 50000 else 2000

    def registrar_cliente(self, usuario_id: int, nombre: str, cedula: str, 
                       telefono: str, monto: float, tipo_plazo: str, 
                       tasa_interes: Optional[float] = None) -> int:
        """
        Registra un nuevo cliente con su préstamo en el sistema.
        
        Args:
            usuario_id: ID del cobrador que registra al cliente
            nombre: Nombre completo del cliente
            cedula: Número de cédula del cliente
            telefono: Número de teléfono del cliente
            monto: Monto solicitado del préstamo
            tipo_plazo: Plazo del préstamo ("diario", "semanal", "quincenal" o "mensual")
            tasa_interes: Tasa de interés personalizada (opcional)
        
        Returns:
            int: ID del cliente registrado
            
        Notas:
            - Si no se especifica tasa_interes, se usa 20% por defecto
            - Se retiene un seguro igual a una cuota mínima
            - El monto real entregado es el monto solicitado menos el seguro
        """
        fecha = datetime.now().date()
        
        # Calcular tasa de interés
        if tasa_interes is None:
            tasa_interes = 0.20  # 20% por defecto
        
        # Calcular días de plazo
        plazos = {
            "diario": 1,
            "semanal": 7,
            "quincenal": 15,
            "mensual": 30
        }
        dias_plazo = plazos.get(tipo_plazo, 7)  # Por defecto semanal si el tipo no es válido
        
        # Calcular cuota mínima y seguro
        cuota_minima = self.calcular_cuota_minima(monto)
        seguro = cuota_minima
        
        # El monto real que recibe el cliente es el monto solicitado menos el seguro
        monto_real = monto - seguro
        
        # Insertar cliente y obtener ID
        result = self.db.fetch_one('''
            INSERT INTO clientes (
                usuario_id, nombre, cedula, telefono, monto_prestado, 
                fecha_prestamo, tipo_plazo, tasa_interes, seguro, 
                cuota_minima, dias_plazo, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (usuario_id, nombre, cedula, telefono, monto_real, fecha, 
              tipo_plazo, tasa_interes, seguro, cuota_minima, dias_plazo, 'activo'))
        
        return result['id']

    def registrar_pago(self, cliente_id: int, monto: float, tipo_pago: str) -> int:
        """
        Registra un pago realizado por un cliente.
        
        Args:
            cliente_id: ID del cliente
            monto: Monto del pago
            tipo_pago: Tipo de pago ('efectivo' o 'digital')
            
        Returns:
            int: ID del pago registrado
        """
        fecha = datetime.now().date()
        result = self.db.fetch_one('''
            INSERT INTO pagos (cliente_id, fecha, monto, tipo_pago)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        ''', (cliente_id, fecha, monto, tipo_pago))
        
        return result['id']

    def obtener_clientes(self, usuario_id: int) -> List[Dict]:
        """
        Obtiene la lista de clientes activos para un cobrador.
        
        Args:
            usuario_id: ID del cobrador
            
        Returns:
            List[Dict]: Lista de diccionarios con los datos de los clientes
        """
        clientes = self.db.fetch_all('''
            SELECT id, nombre, cedula, telefono, monto_prestado, fecha_prestamo, 
                   tipo_plazo, tasa_interes, seguro, cuota_minima, dias_plazo, estado
            FROM clientes
            WHERE usuario_id = %s AND estado = 'activo'
            ORDER BY fecha_prestamo DESC
        ''', (usuario_id,))
        
        return [dict(cliente) for cliente in clientes]

    def obtener_cliente_por_id(self, cliente_id: int) -> Optional[Dict]:
        """
        Obtiene la información completa de un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Optional[Dict]: Información del cliente o None si no existe
        """
        cliente = self.db.fetch_one('''
            SELECT id, usuario_id, nombre, cedula, telefono, monto_prestado, 
                   fecha_prestamo, tipo_plazo, tasa_interes, seguro, 
                   cuota_minima, dias_plazo, estado
            FROM clientes
            WHERE id = %s
        ''', (cliente_id,))
        
        return dict(cliente) if cliente else None

    def obtener_historial_pagos(self, cliente_id: int) -> List[Dict]:
        """
        Obtiene el historial de pagos de un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            List[Dict]: Lista de pagos ordenados por fecha descendente
        """
        pagos = self.db.fetch_all('''
            SELECT id, fecha, monto, tipo_pago
            FROM pagos
            WHERE cliente_id = %s
            ORDER BY fecha DESC, id DESC
        ''', (cliente_id,))
        
        return [dict(pago) for pago in pagos]

    def calcular_balance(self, cliente_id: int) -> Dict:
        """
        Calcula el balance completo de un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Dict con información del balance (monto_total, total_pagado, saldo_pendiente, etc.)
        """
        # Obtener información del cliente
        cliente = self.db.fetch_one('''
            SELECT monto_prestado, tasa_interes, seguro
            FROM clientes
            WHERE id = %s
        ''', (cliente_id,))
        
        if not cliente:
            return {}
        
        monto_prestado = float(cliente['monto_prestado'])
        tasa_interes = float(cliente['tasa_interes'])
        seguro = float(cliente['seguro'])

        # Calcular monto total a pagar (monto + interés + seguro)
        interes = monto_prestado * tasa_interes
        monto_total = monto_prestado + interes + seguro

        # Obtener total pagado
        pagado_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM pagos
            WHERE cliente_id = %s
        ''', (cliente_id,))
        total_pagado = float(pagado_result['total']) if pagado_result else 0.0

        saldo_pendiente = monto_total - total_pagado

        return {
            'monto_prestado': monto_prestado,
            'interes': interes,
            'seguro': seguro,
            'monto_total': monto_total,
            'total_pagado': total_pagado,
            'saldo_pendiente': saldo_pendiente,
            'porcentaje_pagado': (total_pagado / monto_total * 100) if monto_total > 0 else 0
        }

    def actualizar_estado_cliente(self, cliente_id: int, nuevo_estado: str) -> bool:
        """
        Actualiza el estado de un cliente.
        
        Args:
            cliente_id: ID del cliente
            nuevo_estado: Nuevo estado ('activo', 'pagado', 'atrasado', 'inactivo')
            
        Returns:
            bool: True si se actualizó correctamente
        """
        self.db.execute('''
            UPDATE clientes 
            SET estado = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        ''', (nuevo_estado, cliente_id))
        return True

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """
        Elimina un cliente del sistema (marcándolo como inactivo).
        Solo se permite si el cliente ha pagado completamente su préstamo.
        
        Args:
            cliente_id: ID del cliente a eliminar
            
        Returns:
            bool: True si el cliente fue eliminado, False si no se puede eliminar
        """
        # Verificar si el cliente ha pagado completamente
        balance = self.calcular_balance(cliente_id)
        if balance.get('saldo_pendiente', 0) > 0:
            return False
            
        # Marcar el cliente como inactivo
        return self.actualizar_estado_cliente(cliente_id, 'inactivo')

    def buscar_clientes(self, usuario_id: int, termino: str) -> List[Dict]:
        """
        Busca clientes por nombre, cédula o teléfono.
        
        Args:
            usuario_id: ID del cobrador
            termino: Término de búsqueda
            
        Returns:
            List[Dict]: Lista de clientes que coinciden con la búsqueda
        """
        termino_busqueda = f'%{termino}%'
        clientes = self.db.fetch_all('''
            SELECT id, nombre, cedula, telefono, monto_prestado, fecha_prestamo, 
                   tipo_plazo, tasa_interes, seguro, cuota_minima, dias_plazo, estado
            FROM clientes
            WHERE usuario_id = %s 
            AND (nombre ILIKE %s OR cedula ILIKE %s OR telefono ILIKE %s)
            ORDER BY fecha_prestamo DESC
        ''', (usuario_id, termino_busqueda, termino_busqueda, termino_busqueda))
        
        return [dict(cliente) for cliente in clientes]

    def obtener_estadisticas_cobrador(self, usuario_id: int) -> Dict:
        """
        Obtiene estadísticas generales del cobrador.
        
        Args:
            usuario_id: ID del cobrador
            
        Returns:
            Dict con estadísticas (total_clientes, monto_prestado_total, monto_cobrado, etc.)
        """
        # Clientes activos
        clientes_result = self.db.fetch_one('''
            SELECT COUNT(*) as total,
                   COALESCE(SUM(monto_prestado), 0) as monto_total
            FROM clientes
            WHERE usuario_id = %s AND estado = 'activo'
        ''', (usuario_id,))
        
        # Total cobrado (todos los tiempos)
        cobrado_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(p.monto), 0) as total
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = %s
        ''', (usuario_id,))
        
        return {
            'total_clientes_activos': clientes_result['total'] if clientes_result else 0,
            'monto_prestado_total': float(clientes_result['monto_total']) if clientes_result else 0.0,
            'total_cobrado': float(cobrado_result['total']) if cobrado_result else 0.0
        }
