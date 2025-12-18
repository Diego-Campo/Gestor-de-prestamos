# Información de versión de la aplicación
__version__ = "2.0.0"
__app_name__ = "Gestor de Préstamos"
__description__ = "Sistema Multi-plataforma de Gestión y Control de Préstamos (Android/Windows)"
__author__ = "Diego Campo"
__email__ = "campoviverodiego@gmail.com"
__url__ = "https://github.com/Diego-Campo/Gestor-de-prestamos"
__license__ = "MIT"
  
# Información de build
__build_date__ = "2025-12-18"
__python_version__ = "3.9+"
__platform__ = "Android, Windows"

# Configuración de la aplicación
APP_CONFIG = {
    "name": __app_name__,
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "license": __license__,
    "min_python_version": "3.9.0",
    "supported_platforms": ["Android", "Windows"],
    "architecture": "Client-Server (REST API)",
    "database": "PostgreSQL 15+",
    "dependencies": [
        "kivy>=2.2.0",
        "kivymd>=1.1.1",
        "fastapi>=0.104.0",
        "psycopg2-binary>=2.9.0",
        "bcrypt>=4.0.0", 
        "python-dotenv>=1.0.0",
        "requests>=2.31.0"
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