"""
Punto de entrada principal de Gestor de Préstamos v2.0.0

Aplicación multi-plataforma (Android/Windows) con:
- UI Kivy/KivyMD
- API REST con FastAPI
- Base de datos PostgreSQL
"""

import os
# os.environ['KIVY_NO_CONSOLELOG'] = '1'  # Desactivar logs de consola en producción

from kivy.app import App
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.properties import StringProperty
import requests
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gestor_prestamos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configuración de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')


class GestorPrestamosApp(MDApp):
    """Aplicación principal de Gestor de Préstamos."""
    
    # Variables globales
    token = StringProperty('')
    usuario_id = 0
    usuario_nombre = StringProperty('')
    es_admin = False
    
    def build(self):
        """Construye la interfaz de usuario."""
        self.title = "Gestor de Préstamos"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        
        # Configurar tamaño de ventana para desktop
        if not self.is_mobile():
            Window.size = (400, 700)  # Tamaño móvil en desktop
        
        # Crear screen manager
        from src.ui_kivy.screens import (
            LoginScreen,
            HomeScreen,
            ClientesScreen,
            PagosScreen,
            UsuariosScreen
        )
        
        self.sm = MDScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(ClientesScreen(name='clientes'))
        self.sm.add_widget(PagosScreen(name='pagos'))
        self.sm.add_widget(UsuariosScreen(name='usuarios'))
        
        return self.sm
    
    def is_mobile(self):
        """Detecta si estamos en dispositivo móvil."""
        from kivy.utils import platform
        return platform in ('android', 'ios')
    
    def login(self, username, password):
        """
        Realiza el login del usuario.
        
        Returns:
            tuple: (success, message)
        """
        try:
            response = requests.post(
                f'{API_URL}/api/auth/login',
                json={'username': username, 'password': password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']
                usuario = data['usuario']
                self.usuario_id = usuario['id']
                self.usuario_nombre = usuario['nombre']
                self.es_admin = usuario['es_admin']
                logger.info(f"Login exitoso: {username}")
                return True, "Login exitoso"
            else:
                logger.warning(f"Login fallido: {username}")
                return False, "Usuario o contraseña incorrectos"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión: {e}")
            return False, f"Error de conexión: {str(e)}"
    
    def logout(self):
        """Cierra la sesión del usuario."""
        self.token = ''
        self.usuario_id = 0
        self.usuario_nombre = ''
        self.es_admin = False
        self.sm.current = 'login'
        logger.info("Logout exitoso")
    
    def get_headers(self):
        """Retorna los headers HTTP con el token de autenticación."""
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def api_request(self, method, endpoint, data=None, params=None):
        """
        Realiza una petición a la API.
        
        Args:
            method: Método HTTP ('GET', 'POST', 'PUT', 'DELETE')
            endpoint: Endpoint de la API (ej: '/api/clientes')
            data: Datos para enviar (POST, PUT)
            params: Parámetros de query string (GET)
            
        Returns:
            tuple: (success, response_data_or_error_message)
        """
        try:
            url = f'{API_URL}{endpoint}'
            headers = self.get_headers()
            
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return False, "Método HTTP no soportado"
            
            if response.status_code in (200, 201):
                return True, response.json()
            else:
                error_data = response.json()
                return False, error_data.get('detail', 'Error desconocido')
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en API request: {e}")
            return False, f"Error de conexión: {str(e)}"


def main():
    """Función principal."""
    try:
        logger.info("=" * 60)
        logger.info("Iniciando Gestor de Préstamos v2.0.0")
        logger.info("=" * 60)
        
        GestorPrestamosApp().run()
        
    except Exception as e:
        logger.error(f"Error crítico: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
