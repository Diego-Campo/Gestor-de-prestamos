# Información de versión de la aplicación
__version__ = "1.0.0"
__app_name__ = "Gestor de Préstamos"
__description__ = "Sistema de Gestión y Control de Préstamos"
__author__ = "Equipo de Desarrollo"
__email__ = "desarrollo@gestorprestamos.com"
__url__ = "https://github.com/gestor-prestamos/sistema-prestamos"
__license__ = "MIT"

# Información de build
__build_date__ = "2024-11-11"
__python_version__ = "3.8+"
__platform__ = "Windows"

# Configuración de la aplicación
APP_CONFIG = {
    "name": __app_name__,
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "license": __license__,
    "min_python_version": "3.8.0",
    "supported_platforms": ["Windows"],
    "dependencies": [
        "PyQt6>=6.5.0",
        "bcrypt>=4.0.0", 
        "python-dotenv>=1.0.0"
    ]
}

def get_version_info():
    """Retorna información completa de la versión."""
    return {
        "version": __version__,
        "app_name": __app_name__,
        "build_date": __build_date__,
        "python_version": __python_version__,
        "platform": __platform__
    }

def get_version_string():
    """Retorna string formateado con la versión."""
    return f"{__app_name__} v{__version__}"

def get_full_version_string():
    """Retorna string completo con toda la información de versión."""
    return f"{__app_name__} v{__version__} - Build {__build_date__} - Python {__python_version__}"