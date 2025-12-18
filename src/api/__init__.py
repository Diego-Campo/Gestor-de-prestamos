"""
API REST con FastAPI para Gestor de Préstamos.

Proporciona endpoints para:
- Autenticación (login, logout, refresh token)
- Gestión de usuarios
- Gestión de clientes
- Registro de pagos
- Consultas y reportes
"""

from .server import app
from . import routes

__all__ = ['app']
