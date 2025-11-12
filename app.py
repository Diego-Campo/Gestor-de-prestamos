"""
Punto de entrada principal de la aplicación Gestor de Préstamos.

Este script inicializa la interfaz gráfica y establece las conexiones
necesarias con la base de datos. Es el archivo que debe ejecutarse
para iniciar la aplicación.

Versión: 1.0.0
Autor: Equipo de Desarrollo
Licencia: MIT
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication

from src.database import Database
from src.usuario import Usuario
from src.cliente import Cliente
from src.ui.main_window import MainWindow
from version import get_version_string, get_full_version_string

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gestor_prestamos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """
    Función principal que inicializa y ejecuta la aplicación.
    
    Esta función:
    1. Crea la aplicación Qt
    2. Inicializa la base de datos
    3. Configura los gestores de usuarios y clientes
    4. Crea y muestra la ventana principal
    5. Ejecuta el bucle principal de la aplicación
    """
    # Configurar información de la aplicación
    QCoreApplication.setApplicationName("Gestor de Préstamos")
    QCoreApplication.setApplicationVersion("1.0.0")
    QCoreApplication.setOrganizationName("Gestor de Préstamos")
    
    app = QApplication(sys.argv)
    db = None
    
    # Log de inicio
    logger.info(f"Iniciando {get_full_version_string()}")
    
    try:
        # Inicializar la base de datos y managers
        db = Database()
        db.inicializar_admin()  # Asegurar que existe un usuario administrador
        usuario_manager = Usuario(db)
        cliente_manager = Cliente(db)
        
        # Crear y mostrar la ventana principal
        window = MainWindow(db, usuario_manager, cliente_manager)
        window.show()
        
        logger.info("Aplicación iniciada correctamente")
        
        # Ejecutar la aplicación
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error crítico al iniciar la aplicación: {str(e)}")
        raise
    finally:
        # Asegurar que la conexión a la base de datos se cierre correctamente
        if db is not None:
            try:
                db.close()
                logger.info("Base de datos cerrada correctamente")
            except Exception as close_error:
                logger.warning(f"Error al cerrar la base de datos: {str(close_error)}")

if __name__ == "__main__":
    main()