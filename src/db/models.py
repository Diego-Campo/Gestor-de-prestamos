"""
Modelos de datos para Gestor de Préstamos.

Define las clases que representan las entidades del sistema:
- Usuario
- Cliente
- Pago
- BaseSemanales
- GastoSemanales
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Usuario:
    """Modelo de Usuario (cobrador o administrador)."""
    id: Optional[int] = None
    username: str = ''
    password: str = ''
    nombre: str = ''
    es_admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convierte el usuario a diccionario (sin password)."""
        return {
            'id': self.id,
            'username': self.username,
            'nombre': self.nombre,
            'es_admin': self.es_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class Cliente:
    """Modelo de Cliente con préstamo."""
    id: Optional[int] = None
    usuario_id: int = 0
    nombre: str = ''
    cedula: str = ''
    telefono: str = ''
    monto_prestado: Decimal = Decimal('0.00')
    fecha_prestamo: Optional[date] = None
    tipo_plazo: str = ''
    tasa_interes: Decimal = Decimal('0.00')
    seguro: Decimal = Decimal('0.00')
    cuota_minima: Decimal = Decimal('0.00')
    dias_plazo: int = 0
    estado: str = 'activo'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convierte el cliente a diccionario."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'nombre': self.nombre,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'monto_prestado': float(self.monto_prestado),
            'fecha_prestamo': self.fecha_prestamo.isoformat() if self.fecha_prestamo else None,
            'tipo_plazo': self.tipo_plazo,
            'tasa_interes': float(self.tasa_interes),
            'seguro': float(self.seguro),
            'cuota_minima': float(self.cuota_minima),
            'dias_plazo': self.dias_plazo,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class Pago:
    """Modelo de Pago realizado por un cliente."""
    id: Optional[int] = None
    cliente_id: int = 0
    fecha: Optional[date] = None
    monto: Decimal = Decimal('0.00')
    tipo_pago: str = ''  # 'efectivo' o 'digital'
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convierte el pago a diccionario."""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'monto': float(self.monto),
            'tipo_pago': self.tipo_pago,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class BaseSemanales:
    """Modelo de Base Semanal de un cobrador."""
    id: Optional[int] = None
    usuario_id: int = 0
    monto: Decimal = Decimal('0.00')
    fecha: Optional[date] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convierte la base semanal a diccionario."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'monto': float(self.monto),
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class GastoSemanales:
    """Modelo de Gasto Semanal de un cobrador."""
    id: Optional[int] = None
    usuario_id: int = 0
    monto: Decimal = Decimal('0.00')
    descripcion: Optional[str] = None
    fecha: Optional[date] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convierte el gasto semanal a diccionario."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'monto': float(self.monto),
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
