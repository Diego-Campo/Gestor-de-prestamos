"""
Gestión de conexión a PostgreSQL.

Proporciona una clase Database que maneja:
- Pool de conexiones
- Transacciones
- Manejo de errores
- Inicialización de tablas
"""

import psycopg2
from psycopg2 import pool, extras
from contextlib import contextmanager
import os
from typing import Optional, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class Database:
    """
    Clase para manejar la conexión y operaciones con PostgreSQL.
    
    Usa un pool de conexiones para mejor rendimiento y manejo
    de múltiples clientes concurrentes.
    """
    
    _connection_pool: Optional[pool.SimpleConnectionPool] = None
    
    def __init__(self, 
                 host: str = None,
                 port: int = None,
                 database: str = None,
                 user: str = None,
                 password: str = None):
        """
        Inicializa el pool de conexiones a PostgreSQL.
        
        Args:
            host: Host del servidor PostgreSQL (default: localhost)
            port: Puerto del servidor (default: 5432)
            database: Nombre de la base de datos (default: gestor_prestamos)
            user: Usuario de PostgreSQL (default: postgres)
            password: Contraseña del usuario
        """
        # Usar variables de entorno o valores por defecto
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', '5432'))
        self.database = database or os.getenv('DB_NAME', 'gestor_prestamos')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', 'postgres')
        
        self._init_pool()
    
    def _init_pool(self):
        """Inicializa el pool de conexiones."""
        try:
            if Database._connection_pool is None:
                Database._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                logger.info(f"✅ Pool de conexiones creado: {self.database}@{self.host}:{self.port}")
        except psycopg2.Error as e:
            logger.error(f"❌ Error creando pool de conexiones: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener una conexión del pool.
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuarios")
        """
        conn = None
        try:
            conn = Database._connection_pool.getconn()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error en conexión: {e}")
            raise
        finally:
            if conn:
                Database._connection_pool.putconn(conn)
    
    @contextmanager
    def get_cursor(self, cursor_factory=None):
        """
        Context manager para obtener un cursor.
        
        Args:
            cursor_factory: Tipo de cursor (default: DictCursor para dict rows)
        
        Usage:
            with db.get_cursor() as cur:
                cur.execute("SELECT * FROM usuarios")
                users = cur.fetchall()
        """
        with self.get_connection() as conn:
            cursor_factory = cursor_factory or extras.RealDictCursor
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
            finally:
                cursor.close()
    
    def execute(self, query: str, params: Tuple = None) -> None:
        """
        Ejecuta una query que no retorna resultados (INSERT, UPDATE, DELETE).
        
        Args:
            query: Query SQL
            params: Parámetros para la query
        """
        with self.get_cursor() as cur:
            cur.execute(query, params)
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[dict]:
        """
        Ejecuta una query y retorna un solo resultado.
        
        Args:
            query: Query SQL
            params: Parámetros para la query
            
        Returns:
            dict con los resultados o None
        """
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()
    
    def fetch_all(self, query: str, params: Tuple = None) -> List[dict]:
        """
        Ejecuta una query y retorna todos los resultados.
        
        Args:
            query: Query SQL
            params: Parámetros para la query
            
        Returns:
            Lista de dicts con los resultados
        """
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    
    def create_tables(self):
        """Crea todas las tablas necesarias en la base de datos."""
        with self.get_cursor() as cur:
            # Tabla de usuarios
            cur.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    es_admin BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de bases semanales
            cur.execute('''
                CREATE TABLE IF NOT EXISTS bases_semanales (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                    monto DECIMAL(12, 2) NOT NULL,
                    fecha DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de clientes
            cur.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                    nombre VARCHAR(100) NOT NULL,
                    cedula VARCHAR(20) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    monto_prestado DECIMAL(12, 2) NOT NULL,
                    fecha_prestamo DATE NOT NULL,
                    tipo_plazo VARCHAR(20) NOT NULL,
                    tasa_interes DECIMAL(5, 4) NOT NULL,
                    seguro DECIMAL(12, 2) NOT NULL,
                    cuota_minima DECIMAL(12, 2) NOT NULL,
                    dias_plazo INTEGER NOT NULL,
                    estado VARCHAR(20) DEFAULT 'activo',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de pagos
            cur.execute('''
                CREATE TABLE IF NOT EXISTS pagos (
                    id SERIAL PRIMARY KEY,
                    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
                    fecha DATE NOT NULL,
                    monto DECIMAL(12, 2) NOT NULL,
                    tipo_pago VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de gastos semanales
            cur.execute('''
                CREATE TABLE IF NOT EXISTS gastos_semanales (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                    monto DECIMAL(12, 2) NOT NULL,
                    descripcion TEXT,
                    fecha DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Índices para mejorar rendimiento
            cur.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username)')
            cur.execute('CREATE INDEX IF NOT EXISTS idx_clientes_usuario_id ON clientes(usuario_id)')
            cur.execute('CREATE INDEX IF NOT EXISTS idx_clientes_estado ON clientes(estado)')
            cur.execute('CREATE INDEX IF NOT EXISTS idx_pagos_cliente_id ON pagos(cliente_id)')
            cur.execute('CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON pagos(fecha)')
            
            logger.info("✅ Tablas creadas exitosamente")
    
    def inicializar_admin(self):
        """Crea el usuario administrador por defecto si no existe."""
        import bcrypt
        
        # Verificar si ya existe un administrador
        admin = self.fetch_one(
            'SELECT id FROM usuarios WHERE es_admin = TRUE LIMIT 1'
        )
        
        if not admin:
            password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            self.execute('''
                INSERT INTO usuarios (username, password, nombre, es_admin)
                VALUES (%s, %s, %s, %s)
            ''', ('admin', password.decode('utf-8'), 'Administrador', True))
            logger.info("✅ Usuario administrador creado")
    
    def close_all_connections(self):
        """Cierra todas las conexiones del pool."""
        if Database._connection_pool:
            Database._connection_pool.closeall()
            Database._connection_pool = None
            logger.info("✅ Pool de conexiones cerrado")
    
    def __del__(self):
        """Destructor para cerrar conexiones al eliminar la instancia."""
        # No cerramos el pool aquí porque es compartido
        pass
