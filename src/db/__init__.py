"""
Módulo de base de datos PostgreSQL para Gestor de Préstamos.

Este módulo proporciona:
- Conexión a PostgreSQL
- Modelos de datos
- Operaciones CRUD
"""

from .connection import Database
from .models import Usuario, Cliente, Pago, BaseSemanales, GastoSemanales

__all__ = [
    'Database',
    'Usuario',
    'Cliente',
    'Pago',
    'BaseSemanales',
    'GastoSemanales'
]
