import sqlite3
from datetime import datetime

class Database:
    """
    Clase para manejar la conexión y operaciones con la base de datos SQLite.
    
    Esta clase se encarga de:
    - Establecer la conexión con la base de datos
    - Crear las tablas necesarias si no existen
    - Proporcionar acceso al cursor para operaciones SQL
    """
    
    def __init__(self):
        """
        Inicializa la conexión a la base de datos y crea las tablas necesarias.
        La base de datos se crea en el archivo 'gestor_prestamos.db'.
        """
        self.connection = sqlite3.connect('gestor_prestamos.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Crea todas las tablas necesarias en la base de datos si no existen.
        
        Tablas creadas:
        - usuarios: Almacena información de los cobradores
        - bases_semanales: Registra el dinero base de cada semana por cobrador
        - clientes: Guarda información de los clientes y sus préstamos
        - pagos: Registra los pagos realizados por los clientes
        - gastos_semanales: Almacena los gastos operativos de los cobradores
        """
        # Tabla de usuarios (cobradores y administradores)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre TEXT NOT NULL,
                es_admin BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        
        # Verificar si necesitamos migrar la tabla de usuarios
        self.cursor.execute("PRAGMA table_info(usuarios)")
        columnas = [col[1] for col in self.cursor.fetchall()]
        
        if 'es_admin' not in columnas:
            # Hacer backup de la tabla actual
            self.cursor.execute('''
                CREATE TABLE usuarios_backup AS SELECT * FROM usuarios
            ''')
            
            # Eliminar tabla actual
            self.cursor.execute('DROP TABLE usuarios')
            
            # Crear nueva tabla con la estructura actualizada
            self.cursor.execute('''
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    es_admin BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
            
            # Restaurar datos
            self.cursor.execute('''
                INSERT INTO usuarios (id, username, password, nombre, es_admin)
                SELECT id, username, password, nombre, 0
                FROM usuarios_backup
            ''')
            
            # Eliminar tabla de backup
            self.cursor.execute('DROP TABLE usuarios_backup')
            
            # Convertir el usuario 'admin' en administrador si existe
            self.cursor.execute('''
                UPDATE usuarios 
                SET es_admin = 1 
                WHERE username = 'admin'
            ''')
            
            self.connection.commit()

        # Tabla de bases semanales
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bases_semanales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                monto REAL NOT NULL,
                fecha DATE NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        # Tabla de clientes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nombre TEXT NOT NULL,
                cedula TEXT NOT NULL,
                telefono TEXT NOT NULL,
                monto_prestado REAL NOT NULL,
                fecha_prestamo DATE NOT NULL,
                tipo_plazo TEXT NOT NULL,
                tasa_interes REAL NOT NULL,
                seguro REAL NOT NULL,
                cuota_minima REAL NOT NULL,
                dias_plazo INTEGER NOT NULL,
                estado TEXT DEFAULT 'activo',
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        # Tabla de pagos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                fecha DATE NOT NULL,
                monto REAL NOT NULL,
                tipo_pago TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')

        # Tabla de gastos semanales
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos_semanales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                monto REAL NOT NULL,
                descripcion TEXT,
                fecha DATE NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        self.connection.commit()

    def inicializar_admin(self):
        """
        Asegura que existe al menos un usuario administrador en el sistema.
        Si no existe ninguno, crea el usuario admin por defecto.
        """
        self.cursor.execute('SELECT COUNT(*) FROM usuarios WHERE es_admin = 1')
        tiene_admin = self.cursor.fetchone()[0] > 0
        
        if not tiene_admin:
            # Crear usuario admin por defecto
            import bcrypt
            password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                INSERT INTO usuarios (username, password, nombre, es_admin)
                VALUES (?, ?, ?, ?)
            ''', ('admin', password, 'Administrador', True))
            self.connection.commit()

    def close(self):
        self.connection.close()