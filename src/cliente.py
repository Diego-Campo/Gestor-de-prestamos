from datetime import datetime
from typing import List, Tuple, Optional, Union

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
            db: Instancia de la clase Database para operaciones con la base de datos
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
        
        self.db.cursor.execute('''
            INSERT INTO clientes (
                usuario_id, nombre, cedula, telefono, monto_prestado, 
                fecha_prestamo, tipo_plazo, tasa_interes, seguro, 
                cuota_minima, dias_plazo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nombre, cedula, telefono, monto_real, fecha, 
              tipo_plazo, tasa_interes, seguro, cuota_minima, dias_plazo))
        self.db.connection.commit()
        return self.db.cursor.lastrowid

    def registrar_pago(self, cliente_id, monto, tipo_pago):
        fecha = datetime.now().date()
        self.db.cursor.execute('''
            INSERT INTO pagos (cliente_id, fecha, monto, tipo_pago)
            VALUES (?, ?, ?, ?)
        ''', (cliente_id, fecha, monto, tipo_pago))
        self.db.connection.commit()

    def obtener_clientes(self, usuario_id):
        """
        Obtiene la lista de clientes activos para un cobrador.
        
        Args:
            usuario_id: ID del cobrador
            
        Returns:
            List[Tuple]: Lista de tuplas con los datos de los clientes:
                (id, nombre, cedula, telefono, monto_prestado, fecha_prestamo, 
                tipo_plazo, tasa_interes, seguro, cuota_minima, dias_plazo)
        """
        self.db.cursor.execute('''
            SELECT id, nombre, cedula, telefono, monto_prestado, fecha_prestamo, 
                   tipo_plazo, tasa_interes, seguro, cuota_minima, dias_plazo
            FROM clientes
            WHERE usuario_id = ? AND estado = 'activo'
        ''', (usuario_id,))
        return self.db.cursor.fetchall()

    def obtener_historial_pagos(self, cliente_id):
        self.db.cursor.execute('''
            SELECT fecha, monto, tipo_pago
            FROM pagos
            WHERE cliente_id = ?
            ORDER BY fecha DESC
        ''', (cliente_id,))
        return self.db.cursor.fetchall()

    def calcular_balance(self, cliente_id):
        # Obtener información del cliente
        self.db.cursor.execute('''
            SELECT monto_prestado, tasa_interes, seguro
            FROM clientes
            WHERE id = ?
        ''', (cliente_id,))
        cliente = self.db.cursor.fetchone()
        monto_prestado = cliente[0]
        tasa_interes = cliente[1]
        seguro = cliente[2]

        # Calcular monto total a pagar (incluyendo interés)
        monto_total = monto_prestado * (1 + tasa_interes)

        # Obtener total pagado
        self.db.cursor.execute('''
            SELECT SUM(monto)
            FROM pagos
            WHERE cliente_id = ?
        ''', (cliente_id,))
        total_pagado = self.db.cursor.fetchone()[0] or 0

        return monto_total - total_pagado

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
        if balance > 0:
            return False
            
        # Marcar el cliente como inactivo
        self.db.cursor.execute('''
            UPDATE clientes 
            SET estado = 'inactivo' 
            WHERE id = ?
        ''', (cliente_id,))
        self.db.connection.commit()
        return True