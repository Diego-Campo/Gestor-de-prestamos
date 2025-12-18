"""
Pantalla de gestión de usuarios (solo admin)
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, ThreeLineIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.app import App


class UsuariosScreen(MDScreen):
    """Pantalla de gestión de usuarios (solo admin)."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self):
        """Se ejecuta al entrar a la pantalla."""
        self.clear_widgets()
        self.build_ui()
        self.load_usuarios()
    
    def build_ui(self):
        """Construye la interfaz de usuario."""
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back
        )
        header.add_widget(back_btn)
        header.add_widget(MDLabel(text="GESTIÓN DE USUARIOS", font_style="H6"))
        
        add_btn = MDIconButton(
            icon="account-plus",
            on_release=self.show_add_usuario
        )
        header.add_widget(add_btn)
        layout.add_widget(header)
        
        # Lista de usuarios
        scroll = ScrollView()
        self.usuarios_list = MDList()
        scroll.add_widget(self.usuarios_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_usuarios(self):
        """Carga la lista de usuarios."""
        app = App.get_running_app()
        success, data = app.api_request('GET', '/api/usuarios')
        
        self.usuarios_list.clear_widgets()
        
        if success and isinstance(data, list):
            for usuario in data:
                rol = "ADMIN" if usuario.get('es_admin') else "Cobrador"
                item = ThreeLineIconListItem(
                    text=usuario['nombre'],
                    secondary_text=f"Usuario: {usuario['username']}",
                    tertiary_text=f"Rol: {rol}",
                    on_release=lambda x, u=usuario: self.show_usuario_detail(u)
                )
                self.usuarios_list.add_widget(item)
            
            if not data:
                self.usuarios_list.add_widget(
                    MDLabel(text="No hay usuarios registrados", halign="center")
                )
        else:
            self.usuarios_list.add_widget(
                MDLabel(text="Error cargando usuarios", halign="center")
            )
    
    def show_add_usuario(self, *args):
        """Muestra diálogo para agregar usuario."""
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(250))
        
        username_field = MDTextField(hint_text="Nombre de usuario", mode="rectangle")
        password_field = MDTextField(hint_text="Contraseña", password=True, mode="rectangle")
        nombre_field = MDTextField(hint_text="Nombre completo", mode="rectangle")
        
        content.add_widget(username_field)
        content.add_widget(password_field)
        content.add_widget(nombre_field)
        
        # Checkbox para admin
        from kivymd.uix.selectioncontrol import MDCheckbox
        admin_box = BoxLayout(size_hint_y=None, height=dp(40))
        admin_box.add_widget(MDLabel(text="Es Administrador:"))
        es_admin_check = MDCheckbox()
        admin_box.add_widget(es_admin_check)
        content.add_widget(admin_box)
        
        dialog = MDDialog(
            title="Nuevo Usuario",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="CREAR",
                    on_release=lambda x: self.do_add_usuario(
                        dialog, username_field.text, password_field.text,
                        nombre_field.text, es_admin_check.active
                    )
                )
            ]
        )
        dialog.open()
    
    def do_add_usuario(self, dialog, username, password, nombre, es_admin):
        """Crea un nuevo usuario."""
        if not all([username, password, nombre]):
            MDDialog(
                title="Error",
                text="Todos los campos son obligatorios",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        app = App.get_running_app()
        success, data = app.api_request('POST', '/api/usuarios', {
            'username': username,
            'password': password,
            'nombre': nombre,
            'es_admin': es_admin
        })
        
        if success:
            dialog.dismiss()
            MDDialog(
                title="Éxito",
                text="Usuario creado correctamente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            self.load_usuarios()
        else:
            MDDialog(
                title="Error",
                text=f"No se pudo crear el usuario: {data}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
    
    def show_usuario_detail(self, usuario):
        """Muestra detalles y opciones para un usuario."""
        detail_text = f"""
Nombre: {usuario['nombre']}
Usuario: {usuario['username']}
Rol: {'Administrador' if usuario.get('es_admin') else 'Cobrador'}
"""
        
        buttons = [MDFlatButton(text="CERRAR", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
        
        # No permitir eliminar si es el usuario actual o si es admin
        app = App.get_running_app()
        if usuario['id'] != app.usuario_id and not usuario.get('es_admin'):
            buttons.append(
                MDRaisedButton(
                    text="ELIMINAR",
                    md_bg_color=(0.6, 0.2, 0.2, 1),
                    on_release=lambda x: self.confirm_delete_usuario(usuario)
                )
            )
        
        MDDialog(
            title="Detalles del Usuario",
            text=detail_text,
            buttons=buttons
        ).open()
    
    def confirm_delete_usuario(self, usuario):
        """Confirma eliminación de usuario."""
        dialog = MDDialog(
            title="Confirmar Eliminación",
            text=f"¿Estás seguro de eliminar al usuario {usuario['nombre']}?",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="ELIMINAR",
                    md_bg_color=(0.6, 0.2, 0.2, 1),
                    on_release=lambda x: self.do_delete_usuario(dialog, usuario['id'])
                )
            ]
        )
        dialog.open()
    
    def do_delete_usuario(self, dialog, usuario_id):
        """Elimina el usuario."""
        app = App.get_running_app()
        success, data = app.api_request('DELETE', f'/api/usuarios/{usuario_id}')
        
        dialog.dismiss()
        
        if success:
            MDDialog(
                title="Éxito",
                text="Usuario eliminado correctamente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            self.load_usuarios()
        else:
            MDDialog(
                title="Error",
                text=f"No se pudo eliminar el usuario: {data}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
    
    def go_back(self, *args):
        """Regresa a la pantalla anterior."""
        self.manager.current = 'home'
