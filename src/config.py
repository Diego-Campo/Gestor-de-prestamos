"""
Configuración de la aplicación Gestor de Préstamos.

Este módulo contiene las configuraciones por defecto de la aplicación,
incluyendo parámetros de negocio, configuración de la base de datos
y otras constantes importantes.
"""

import os
from pathlib import Path

# Información de la aplicación
APP_NAME = "Gestor de Préstamos"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Gestión y Control de Préstamos"

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'gestor_prestamos'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# Configuración de negocio
class BusinessConfig:
    """Configuraciones relacionadas con la lógica de negocio."""
    
    # Intereses
    INTERES_DEFECTO = 0.20  # 20%
    MONTO_MINIMO_INTERES_PERSONALIZADO = 500000  # $500,000
    
    # Plazos disponibles (en días)
    PLAZOS_DISPONIBLES = [30, 40]
    
    # Cuotas
    CUOTA_BASE = 2000  # $2,000 por cada $50,000
    MONTO_BASE_CUOTA = 50000  # $50,000
    
    # Días de gracia antes de considerar un pago como atrasado
    DIAS_GRACIA = 3

# Configuración de la interfaz
class UIConfig:
    """Configuraciones relacionadas con la interfaz de usuario."""
    
    # Ventana principal
    WINDOW_MIN_WIDTH = 1200
    WINDOW_MIN_HEIGHT = 800
    
    # Colores principales
    PRIMARY_COLOR = "#2E7D32"  # Verde
    SECONDARY_COLOR = "#388E3C"
    ACCENT_COLOR = "#4CAF50"
    ERROR_COLOR = "#D32F2F"  # Rojo
    WARNING_COLOR = "#F57C00"  # Naranja
    SUCCESS_COLOR = "#388E3C"  # Verde
    
    # Tipografía
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_HEADER = 12
    FONT_SIZE_TITLE = 14

# Configuración de seguridad
class SecurityConfig:
    """Configuraciones relacionadas con la seguridad."""
    
    # Contraseñas
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 50
    
    # Sesiones
    SESSION_TIMEOUT = 3600  # 1 hora en segundos
    
    # Intentos de login
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 300  # 5 minutos en segundos

# Configuración de logging
class LogConfig:
    """Configuraciones para el sistema de logs."""
    
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = "gestor_prestamos.log"
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT = 5

# Configuración por defecto de usuarios
class DefaultUsers:
    """Usuarios por defecto del sistema."""
    
    ADMIN_USER = {
        'username': 'admin',
        'password': 'admin123',
        'nombre': 'Administrador',
        'rol': 'admin'
    }
    
    TEST_USERS = [
        {
            'username': 'cobrador1',
            'password': 'pass1',
            'nombre': 'Juan Pérez',
            'rol': 'cobrador'
        },
        {
            'username': 'cobrador2',
            'password': 'pass2',
            'nombre': 'María López',
            'rol': 'cobrador'
        },
        {
            'username': 'cobrador3',
            'password': 'pass3',
            'nombre': 'Carlos Rodríguez',
            'rol': 'cobrador'
        }
    ]

# Mensajes del sistema
class Messages:
    """Mensajes estándar del sistema."""
    
    # Éxito
    LOGIN_SUCCESS = "Inicio de sesión exitoso"
    SAVE_SUCCESS = "Información guardada correctamente"
    DELETE_SUCCESS = "Eliminado correctamente"
    UPDATE_SUCCESS = "Actualizado correctamente"
    
    # Errores
    LOGIN_ERROR = "Usuario o contraseña incorrectos"
    SAVE_ERROR = "Error al guardar la información"
    DELETE_ERROR = "Error al eliminar"
    UPDATE_ERROR = "Error al actualizar"
    VALIDATION_ERROR = "Por favor, verifique los datos ingresados"
    PERMISSION_ERROR = "No tiene permisos para realizar esta acción"
    
    # Advertencias
    DELETE_CONFIRMATION = "¿Está seguro de que desea eliminar este elemento?"
    UNSAVED_CHANGES = "Tiene cambios sin guardar. ¿Desea continuar?"
    
    # Información
    NO_DATA = "No hay información disponible"
    PROCESSING = "Procesando..."
    LOADING = "Cargando..."

# Utilidades para obtener rutas
def get_app_dir() -> Path:
    """Obtiene el directorio de la aplicación."""
    return Path(__file__).parent

def get_data_dir() -> Path:
    """Obtiene el directorio de datos."""
    return get_app_dir()

def get_log_path() -> str:
    """Obtiene la ruta completa del archivo de log."""
    return os.path.join(get_data_dir(), LogConfig.LOG_FILE)

def get_db_path() -> str:
    """Obtiene la ruta completa de la base de datos."""
    return os.path.join(get_data_dir(), DB_NAME)