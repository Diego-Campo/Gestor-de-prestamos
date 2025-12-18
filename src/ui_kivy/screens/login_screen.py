"""
Pantalla de Login
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.app import App


class LoginScreen(MDScreen):
    """Pantalla de inicio de sesión."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        """Construye la interfaz de usuario."""
        layout = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )
        
        # Título
        title = MDLabel(
            text="GESTOR DE PRÉSTAMOS",
            halign="center",
            font_style="H4",
            theme_text_color="Primary"
        )
        layout.add_widget(title)
        
        # Subtítulo
        subtitle = MDLabel(
            text="Sistema de Gestión de Cobranza",
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary"
        )
        layout.add_widget(subtitle)
        
        # Espacio
        layout.add_widget(MDLabel(text=""))
        
        # Campo de usuario
        self.username_field = MDTextField(
            hint_text="Usuario",
            mode="rectangle",
            size_hint_x=1
        )
        layout.add_widget(self.username_field)
        
        # Campo de contraseña
        self.password_field = MDTextField(
            hint_text="Contraseña",
            password=True,
            mode="rectangle",
            size_hint_x=1
        )
        layout.add_widget(self.password_field)
        
        # Botón de login
        login_btn = MDRaisedButton(
            text="INICIAR SESIÓN",
            size_hint_x=1,
            pos_hint={"center_x": 0.5},
            on_release=self.do_login
        )
        layout.add_widget(login_btn)
        
        # Botón de registro
        register_btn = MDRaisedButton(
            text="REGISTRARSE",
            size_hint_x=1,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.4, 0.4, 0.4, 1),
            on_release=self.show_register
        )
        layout.add_widget(register_btn)
        
        # Información de versión
        version_label = MDLabel(
            text="v2.0.0",
            halign="center",
            font_style="Caption",
            theme_text_color="Hint"
        )
        layout.add_widget(version_label)
        
        self.add_widget(layout)
    
    def do_login(self, *args):
        """Realiza el proceso de login."""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        if not username or not password:
            self.show_dialog("Error", "Por favor ingresa usuario y contraseña")
            return
        
        app = App.get_running_app()
        success, message = app.login(username, password)
        
        if success:
            # Limpiar campos
            self.username_field.text = ""
            self.password_field.text = ""
            # Ir a home
            self.manager.current = 'home'
        else:
            self.show_dialog("Error de Login", message)
    
    def show_dialog(self, title, text):
        """Muestra un diálogo de alerta."""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        else:
            self.dialog.title = title
            self.dialog.text = text
        
        self.dialog.open()
    
    def show_register(self, *args):
        """Muestra el diálogo de registro."""
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(250))
        
        username_field = MDTextField(hint_text="Usuario", mode="rectangle")
        password_field = MDTextField(hint_text="Contraseña", password=True, mode="rectangle")
        nombre_field = MDTextField(hint_text="Nombre completo", mode="rectangle")
        
        content.add_widget(username_field)
        content.add_widget(password_field)
        content.add_widget(nombre_field)
        
        register_dialog = MDDialog(
            title="Registrar Usuario",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    on_release=lambda x: register_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="REGISTRAR",
                    on_release=lambda x: self.do_register(
                        register_dialog,
                        username_field.text,
                        password_field.text,
                        nombre_field.text
                    )
                )
            ]
        )
        register_dialog.open()
    
    def do_register(self, dialog, username, password, nombre):
        """Realiza el proceso de registro."""
        username = username.strip()
        password = password.strip()
        nombre = nombre.strip()
        
        if not username or not password or not nombre:
            self.show_dialog("Error", "Todos los campos son obligatorios")
            return
        
        # Llamar directamente a la API sin token (registro público)
        import requests
        try:
            response = requests.post(
                'http://localhost:8000/api/auth/register',
                json={
                    'username': username,
                    'password': password,
                    'nombre': nombre
                },
                timeout=10
            )
            
            if response.status_code == 200:
                success = True
                response_msg = "Usuario registrado correctamente"
            else:
                success = False
                error_data = response.json()
                response_msg = error_data.get('detail', 'Error desconocido')
        except Exception as e:
            success = False
            response_msg = f"Error de conexión: {str(e)}"
        
        if success:
            dialog.dismiss()
            self.show_dialog("Éxito", "Usuario registrado correctamente. Ya puedes iniciar sesión.")
        else:
            self.show_dialog("Error", f"No se pudo registrar: {response_msg}")
