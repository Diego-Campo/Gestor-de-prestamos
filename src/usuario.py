"""
Gestión de usuarios para PostgreSQL.

Este módulo ha sido adaptado para funcionar con PostgreSQL
en lugar de SQLite. Los métodos han sido refactorizados para
usar psycopg2 y el pool de conexiones.
"""

import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from psycopg2 import IntegrityError

class Usuario:
    """
    Clase para gestionar todas las operaciones relacionadas con los usuarios (cobradores).
    
    Esta clase maneja:
    - Registro e inicio de sesión de usuarios
    - Gestión de bases semanales
    - Control de gastos
    - Generación de resúmenes semanales
    """

    def __init__(self, db):
        """
        Inicializa el gestor de usuarios.
        
        Args:
            db: Instancia de la clase Database (PostgreSQL) para operaciones con la base de datos
        """
        self.db = db

    def crear_usuario(self, username: str, password: str, nombre: str, es_admin: bool = False) -> bool:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario único
            password: Contraseña (se almacenará hasheada)
            nombre: Nombre completo del cobrador
            es_admin: True si el usuario es administrador, False si es cobrador
        
        Returns:
            bool: True si el usuario se creó exitosamente, False si el username ya existe
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.db.execute('''
                INSERT INTO usuarios (username, password, nombre, es_admin)
                VALUES (%s, %s, %s, %s)
            ''', (username, hashed.decode('utf-8'), nombre, es_admin))
            return True
        except IntegrityError:
            return False

    def validar_usuario(self, username: str, password: str) -> Optional[int]:
        """
        Valida las credenciales de un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
        
        Returns:
            Optional[int]: ID del usuario si las credenciales son válidas, None en caso contrario
        """
        user = self.db.fetch_one(
            'SELECT id, password FROM usuarios WHERE username = %s',
            (username,)
        )
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user['id']
        return None

    def registrar_base_semanal(self, usuario_id: int, monto: float):
        """Registra la base semanal de un cobrador."""
        fecha = datetime.now().date()
        self.db.execute('''
            INSERT INTO bases_semanales (usuario_id, monto, fecha)
            VALUES (%s, %s, %s)
        ''', (usuario_id, monto, fecha))

    def registrar_gasto(self, usuario_id: int, monto: float, descripcion: str):
        """Registra un gasto operativo del cobrador."""
        fecha = datetime.now().date()
        self.db.execute('''
            INSERT INTO gastos_semanales (usuario_id, monto, descripcion, fecha)
            VALUES (%s, %s, %s, %s)
        ''', (usuario_id, monto, descripcion, fecha))

    def obtener_resumen_semanal(self, usuario_id: int) -> Dict:
        """
        Obtiene el resumen de actividad semanal del cobrador.
        
        Args:
            usuario_id: ID del cobrador
            
        Returns:
            Dict con base, cobrado, prestado, gastos, etc.
        """
        fecha_actual = datetime.now().date()
        
        # Obtener base semanal
        base_result = self.db.fetch_one('''
            SELECT monto FROM bases_semanales 
            WHERE usuario_id = %s AND fecha = %s
        ''', (usuario_id, fecha_actual))
        base = float(base_result['monto']) if base_result else 0.0

        # Obtener total cobrado
        cobrado_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(p.monto), 0) as total
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = %s AND p.fecha = %s
        ''', (usuario_id, fecha_actual))
        cobrado = float(cobrado_result['total']) if cobrado_result else 0.0

        # Obtener total prestado y seguros
        prestado_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(monto_prestado), 0) as prestado,
                   COALESCE(SUM(seguro), 0) as seguros
            FROM clientes
            WHERE usuario_id = %s AND fecha_prestamo = %s
        ''', (usuario_id, fecha_actual))
        prestado = float(prestado_result['prestado']) if prestado_result else 0.0
        seguros = float(prestado_result['seguros']) if prestado_result else 0.0

        # Obtener gastos
        gastos_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM gastos_semanales
            WHERE usuario_id = %s AND fecha = %s
        ''', (usuario_id, fecha_actual))
        gastos = float(gastos_result['total']) if gastos_result else 0.0

        # Obtener pagos digitales
        digital_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(p.monto), 0) as total
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = %s AND p.fecha = %s AND p.tipo_pago = 'digital'
        ''', (usuario_id, fecha_actual))
        digital = float(digital_result['total']) if digital_result else 0.0

        return {
            'base': base,
            'cobrado': cobrado,
            'prestado': prestado,
            'seguros': seguros,
            'gastos': gastos,
            'digital': digital,
            'efectivo': cobrado - digital
        }

    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[Dict]:
        """
        Obtiene la información de un usuario por su ID.
        
        Args:
            usuario_id: ID del usuario a buscar
            
        Returns:
            Optional[Dict]: Información del usuario o None si no existe
        """
        usuario = self.db.fetch_one('''
            SELECT id, username, nombre, es_admin
            FROM usuarios 
            WHERE id = %s
        ''', (usuario_id,))
        
        if usuario:
            return dict(usuario)
        return None

    def eliminar_usuario(self, admin_id: int, usuario_id: int) -> bool:
        """
        Elimina un usuario del sistema. Solo se permite si el que ejecuta es admin.
        
        Args:
            admin_id: ID del administrador que intenta eliminar
            usuario_id: ID del usuario a eliminar
            
        Returns:
            bool: True si el usuario fue eliminado, False si no se pudo
        """
        # Verificar si quien ejecuta es administrador
        admin = self.db.fetch_one(
            'SELECT es_admin FROM usuarios WHERE id = %s',
            (admin_id,)
        )
        if not admin or not admin['es_admin']:
            return False

        # Verificar que no se intente eliminar un admin
        usuario = self.db.fetch_one(
            'SELECT es_admin FROM usuarios WHERE id = %s',
            (usuario_id,)
        )
        if not usuario or usuario['es_admin']:
            return False
            
        # Eliminar el usuario
        self.db.execute('DELETE FROM usuarios WHERE id = %s', (usuario_id,))
        return True

    def es_administrador(self, usuario_id: int) -> bool:
        """
        Verifica si un usuario es administrador.
        
        Args:
            usuario_id: ID del usuario a verificar
            
        Returns:
            bool: True si es administrador, False si no
        """
        resultado = self.db.fetch_one(
            'SELECT es_admin FROM usuarios WHERE id = %s',
            (usuario_id,)
        )
        return bool(resultado and resultado['es_admin'])

    def obtener_actividad_cobrador(self, usuario_id: int, fecha: datetime = None) -> Dict:
        """
        Obtiene un resumen detallado de la actividad de un cobrador.
        
        Args:
            usuario_id: ID del cobrador
            fecha: Fecha opcional para filtrar (por defecto, hoy)
            
        Returns:
            Dict con la información de actividad
        """
        if fecha is None:
            fecha = datetime.now().date()

        # Obtener información básica del cobrador
        usuario = self.db.fetch_one('''
            SELECT nombre, username, es_admin 
            FROM usuarios 
            WHERE id = %s
        ''', (usuario_id,))
        
        # Contar clientes activos
        clientes_result = self.db.fetch_one('''
            SELECT COUNT(*) as total
            FROM clientes 
            WHERE usuario_id = %s AND estado = 'activo'
        ''', (usuario_id,))
        clientes_activos = clientes_result['total'] if clientes_result else 0

        # Obtener total prestado hoy
        prestado_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(monto_prestado), 0) as total
            FROM clientes
            WHERE usuario_id = %s AND fecha_prestamo = %s
        ''', (usuario_id, fecha))
        prestado_hoy = float(prestado_result['total']) if prestado_result else 0.0

        # Obtener total cobrado hoy
        cobrado_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(p.monto), 0) as total
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = %s AND p.fecha = %s
        ''', (usuario_id, fecha))
        cobrado_hoy = float(cobrado_result['total']) if cobrado_result else 0.0

        # Obtener gastos de hoy
        gastos_result = self.db.fetch_one('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM gastos_semanales
            WHERE usuario_id = %s AND fecha = %s
        ''', (usuario_id, fecha))
        gastos_hoy = float(gastos_result['total']) if gastos_result else 0.0

        return {
            'nombre': usuario['nombre'],
            'username': usuario['username'],
            'es_admin': usuario['es_admin'],
            'clientes_activos': clientes_activos,
            'prestado_hoy': prestado_hoy,
            'cobrado_hoy': cobrado_hoy,
            'gastos_hoy': gastos_hoy
        }

    def obtener_historial_cobrador(self, usuario_id: int, dias: int = 7) -> List[Dict]:
        """
        Obtiene el historial de actividades de un cobrador.
        
        Args:
            usuario_id: ID del cobrador
            dias: Número de días hacia atrás para obtener el historial
            
        Returns:
            List[Dict]: Lista de actividades diarias
        """
        historial = []
        fecha_actual = datetime.now().date()
        
        for i in range(dias):
            fecha = fecha_actual - timedelta(days=i)
            actividad = self.obtener_actividad_cobrador(usuario_id, fecha)
            actividad['fecha'] = fecha.isoformat()
            historial.append(actividad)
            
        return historial

    def cambiar_password(self, usuario_id: int, password_actual: str, password_nueva: str) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            usuario_id: ID del usuario
            password_actual: Contraseña actual
            password_nueva: Nueva contraseña
            
        Returns:
            bool: True si se cambió correctamente, False si la contraseña actual es incorrecta
        """
        # Validar contraseña actual
        usuario = self.db.fetch_one(
            'SELECT password FROM usuarios WHERE id = %s',
            (usuario_id,)
        )
        
        if not usuario:
            return False
            
        if not bcrypt.checkpw(password_actual.encode('utf-8'), usuario['password'].encode('utf-8')):
            return False
        
        # Hash de la nueva contraseña
        new_hashed = bcrypt.hashpw(password_nueva.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar contraseña
        self.db.execute(
            'UPDATE usuarios SET password = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s',
            (new_hashed.decode('utf-8'), usuario_id)
        )
        
        return True
