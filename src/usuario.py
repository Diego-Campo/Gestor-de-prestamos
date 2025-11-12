import bcrypt
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Optional, Union, List

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
            db: Instancia de la clase Database para operaciones con la base de datos
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
            self.db.cursor.execute('''
                INSERT INTO usuarios (username, password, nombre, es_admin)
                VALUES (?, ?, ?, ?)
            ''', (username, hashed, nombre, es_admin))
            self.db.connection.commit()
            return True
        except sqlite3.IntegrityError:
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
        self.db.cursor.execute('SELECT id, password FROM usuarios WHERE username = ?', (username,))
        user = self.db.cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
            return user[0]
        return None

    def registrar_base_semanal(self, usuario_id, monto):
        fecha = datetime.now().date()
        self.db.cursor.execute('''
            INSERT INTO bases_semanales (usuario_id, monto, fecha)
            VALUES (?, ?, ?)
        ''', (usuario_id, monto, fecha))
        self.db.connection.commit()

    def registrar_gasto(self, usuario_id, monto, descripcion):
        fecha = datetime.now().date()
        self.db.cursor.execute('''
            INSERT INTO gastos_semanales (usuario_id, monto, descripcion, fecha)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, monto, descripcion, fecha))
        self.db.connection.commit()

    def obtener_resumen_semanal(self, usuario_id):
        fecha_actual = datetime.now().date()
        
        # Obtener base semanal
        self.db.cursor.execute('''
            SELECT monto FROM bases_semanales 
            WHERE usuario_id = ? AND fecha = ?
        ''', (usuario_id, fecha_actual))
        base = self.db.cursor.fetchone()
        base = base[0] if base else 0

        # Obtener total cobrado
        self.db.cursor.execute('''
            SELECT SUM(p.monto)
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = ? AND p.fecha = ?
        ''', (usuario_id, fecha_actual))
        cobrado = self.db.cursor.fetchone()[0] or 0

        # Obtener total prestado y seguros
        self.db.cursor.execute('''
            SELECT SUM(monto_prestado), SUM(seguro)
            FROM clientes
            WHERE usuario_id = ? AND fecha_prestamo = ?
        ''', (usuario_id, fecha_actual))
        result = self.db.cursor.fetchone()
        prestado = result[0] or 0
        seguros = result[1] or 0

        # Obtener gastos
        self.db.cursor.execute('''
            SELECT SUM(monto)
            FROM gastos_semanales
            WHERE usuario_id = ? AND fecha = ?
        ''', (usuario_id, fecha_actual))
        gastos = self.db.cursor.fetchone()[0] or 0

        # Obtener pagos digitales
        self.db.cursor.execute('''
            SELECT SUM(p.monto)
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = ? AND p.fecha = ? AND p.tipo_pago = 'digital'
        ''', (usuario_id, fecha_actual))
        digital = self.db.cursor.fetchone()[0] or 0

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
        self.db.cursor.execute('''
            SELECT id, username, nombre 
            FROM usuarios 
            WHERE id = ?
        ''', (usuario_id,))
        usuario = self.db.cursor.fetchone()
        if usuario:
            return {
                'id': usuario[0],
                'username': usuario[1],
                'nombre': usuario[2]
            }
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
        self.db.cursor.execute('SELECT es_admin FROM usuarios WHERE id = ?', (admin_id,))
        es_admin = self.db.cursor.fetchone()[0]
        if not es_admin:
            return False

        # Verificar que no se intente eliminar un admin
        self.db.cursor.execute('SELECT es_admin FROM usuarios WHERE id = ?', (usuario_id,))
        usuario = self.db.cursor.fetchone()
        if not usuario or usuario[0]:  # No existe o es admin
            return False
            
        # Eliminar el usuario
        self.db.cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
        self.db.connection.commit()
        return True

    def es_administrador(self, usuario_id: int) -> bool:
        """
        Verifica si un usuario es administrador.
        
        Args:
            usuario_id: ID del usuario a verificar
            
        Returns:
            bool: True si es administrador, False si no
        """
        self.db.cursor.execute('SELECT es_admin FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = self.db.cursor.fetchone()
        return bool(resultado and resultado[0])

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
        self.db.cursor.execute('''
            SELECT nombre, username, es_admin 
            FROM usuarios 
            WHERE id = ?
        ''', (usuario_id,))
        usuario = self.db.cursor.fetchone()
        
        # Contar clientes activos
        self.db.cursor.execute('''
            SELECT COUNT(*) 
            FROM clientes 
            WHERE usuario_id = ? AND estado = 'activo'
        ''', (usuario_id,))
        clientes_activos = self.db.cursor.fetchone()[0]

        # Obtener total prestado hoy
        self.db.cursor.execute('''
            SELECT SUM(monto_prestado)
            FROM clientes
            WHERE usuario_id = ? AND fecha_prestamo = ?
        ''', (usuario_id, fecha))
        prestado_hoy = self.db.cursor.fetchone()[0] or 0

        # Obtener total cobrado hoy
        self.db.cursor.execute('''
            SELECT SUM(p.monto)
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.usuario_id = ? AND p.fecha = ?
        ''', (usuario_id, fecha))
        cobrado_hoy = self.db.cursor.fetchone()[0] or 0

        # Obtener gastos de hoy
        self.db.cursor.execute('''
            SELECT SUM(monto)
            FROM gastos_semanales
            WHERE usuario_id = ? AND fecha = ?
        ''', (usuario_id, fecha))
        gastos_hoy = self.db.cursor.fetchone()[0] or 0

        return {
            'nombre': usuario[0],
            'username': usuario[1],
            'es_admin': usuario[2],
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
            actividad['fecha'] = fecha
            historial.append(actividad)
            
        return historial