"""
Pantalla principal (Home)
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.app import App


class HomeScreen(MDScreen):
    """Pantalla principal con resumen y navegación."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self):
        """Se ejecuta al entrar a la pantalla."""
        self.clear_widgets()
        self.build_ui()
        self.load_data()
    
    def build_ui(self):
        """Construye la interfaz de usuario."""
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header con nombre de usuario
        app = App.get_running_app()
        header = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        header.add_widget(MDLabel(
            text=f"Bienvenido, {app.usuario_nombre}",
            font_style="H6"
        ))
        
        from kivymd.uix.button import MDIconButton
        pass_btn = MDIconButton(
            icon="key",
            on_release=self.show_cambiar_password
        )
        header.add_widget(pass_btn)
        
        logout_btn = MDFlatButton(
            text="Salir",
            on_release=lambda x: app.logout()
        )
        header.add_widget(logout_btn)
        layout.add_widget(header)
        
        # Scroll con contenido
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Card de resumen
        self.card_resumen = MDCard(
            orientation='vertical',
            padding=dp(20),
            size_hint_y=None,
            height=dp(200)
        )
        self.label_resumen = MDLabel(
            text="Cargando resumen...",
            theme_text_color="Primary"
        )
        self.card_resumen.add_widget(self.label_resumen)
        content.add_widget(self.card_resumen)
        
        # Botones de navegación
        btn_clientes = MDRaisedButton(
            text="📋 GESTIONAR CLIENTES",
            size_hint_y=None,
            height=dp(50),
            on_release=self.go_to_clientes
        )
        content.add_widget(btn_clientes)
        
        btn_pagos = MDRaisedButton(
            text="💰 REGISTRAR PAGO",
            size_hint_y=None,
            height=dp(50),
            on_release=self.go_to_pagos
        )
        content.add_widget(btn_pagos)
        
        # Mostrar opciones de admin
        if app.es_admin:
            btn_usuarios = MDRaisedButton(
                text="👥 GESTIONAR USUARIOS",
                size_hint_y=None,
                height=dp(50),
                md_bg_color=(0.3, 0.5, 0.3, 1),
                on_release=self.show_usuarios
            )
            content.add_widget(btn_usuarios)
        
        # Botones de base y gastos
        base_gastos_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_base = MDRaisedButton(
            text="💵 AGREGAR BASE",
            size_hint_x=0.5,
            md_bg_color=(0.2, 0.6, 0.2, 1),
            on_release=self.show_agregar_base
        )
        base_gastos_box.add_widget(btn_base)
        
        btn_gasto = MDRaisedButton(
            text="💸 REGISTRAR GASTO",
            size_hint_x=0.5,
            md_bg_color=(0.6, 0.2, 0.2, 1),
            on_release=self.show_registrar_gasto
        )
        base_gastos_box.add_widget(btn_gasto)
        
        content.add_widget(base_gastos_box)
        
        btn_reportes = MDRaisedButton(
            text="📊 VER REPORTES",
            size_hint_y=None,
            height=dp(50),
            md_bg_color=(0.2, 0.4, 0.6, 1),
            on_release=self.show_reportes
        )
        content.add_widget(btn_reportes)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_data(self):
        """Carga el resumen del día y semanal."""
        app = App.get_running_app()
        success_hoy, data_hoy = app.api_request('GET', '/api/pagos/resumen/hoy')
        success_semanal, data_semanal = app.api_request('GET', '/api/pagos/resumen/semanal')
        
        if success_hoy:
            resumen_text = f"""═══ RESUMEN DE HOY ═══

💵 Efectivo: ${data_hoy.get('efectivo', 0):,.0f}
💳 Digital: ${data_hoy.get('digital', 0):,.0f}
━━━━━━━━━━━━━━━━━━━━
💰 Total Cobrado: ${data_hoy.get('total_cobrado', 0):,.0f}

📋 Pagos Registrados: {data_hoy.get('num_pagos', 0)}
👥 Clientes Activos: {data_hoy.get('clientes_activos', 0)}
"""
            
            if success_semanal:
                base = data_semanal.get('base', 0)
                gastos = data_semanal.get('gastos', 0)
                cobrado_semanal = data_semanal.get('total_cobrado', 0)
                neto = cobrado_semanal - gastos
                
                resumen_text += f"""
═══ RESUMEN SEMANAL ═══

💵 Base: ${base:,.0f}
💰 Cobrado: ${cobrado_semanal:,.0f}
💸 Gastos: ${gastos:,.0f}
━━━━━━━━━━━━━━━━━━━━
✅ Neto: ${neto:,.0f}
"""
            
            self.label_resumen.text = resumen_text
        else:
            self.label_resumen.text = "Error cargando resumen"
    
    def go_to_clientes(self, *args):
        """Navega a la pantalla de clientes."""
        self.manager.current = 'clientes'
    
    def go_to_pagos(self, *args):
        """Navega a la pantalla de pagos."""
        self.manager.current = 'pagos'
    
    def show_usuarios(self, *args):
        """Navega a la pantalla de gestión de usuarios (solo admin)."""
        self.manager.current = 'usuarios'
    
    def show_agregar_base(self, *args):
        """Muestra diálogo para agregar base del día."""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(100))
        monto_field = MDTextField(hint_text="Monto de la base", mode="rectangle")
        content.add_widget(monto_field)
        
        dialog = MDDialog(
            title="Agregar Base del Día",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="GUARDAR",
                    on_release=lambda x: self.do_agregar_base(dialog, monto_field.text)
                )
            ]
        )
        dialog.open()
    
    def do_agregar_base(self, dialog, monto):
        """Registra la base del día."""
        try:
            monto = float(monto)
        except ValueError:
            return
        
        app = App.get_running_app()
        success, data = app.api_request('POST', '/api/usuarios/base', {'monto': monto})
        
        if success:
            dialog.dismiss()
            self.load_data()
    
    def show_registrar_gasto(self, *args):
        """Muestra diálogo para registrar gasto."""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(150))
        monto_field = MDTextField(hint_text="Monto del gasto", mode="rectangle")
        descripcion_field = MDTextField(hint_text="Descripción", mode="rectangle")
        content.add_widget(monto_field)
        content.add_widget(descripcion_field)
        
        dialog = MDDialog(
            title="Registrar Gasto",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="GUARDAR",
                    on_release=lambda x: self.do_registrar_gasto(
                        dialog, monto_field.text, descripcion_field.text
                    )
                )
            ]
        )
        dialog.open()
    
    def do_registrar_gasto(self, dialog, monto, descripcion):
        """Registra un gasto."""
        try:
            monto = float(monto)
        except ValueError:
            return
        
        app = App.get_running_app()
        success, data = app.api_request('POST', '/api/usuarios/gasto', {
            'monto': monto,
            'descripcion': descripcion
        })
        
        if success:
            dialog.dismiss()
            self.load_data()
    
    def show_cambiar_password(self, *args):
        """Muestra diálogo para cambiar contraseña."""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(200))
        
        actual_field = MDTextField(hint_text="Contraseña actual", password=True, mode="rectangle")
        nueva_field = MDTextField(hint_text="Nueva contraseña", password=True, mode="rectangle")
        confirmar_field = MDTextField(hint_text="Confirmar nueva contraseña", password=True, mode="rectangle")
        
        content.add_widget(actual_field)
        content.add_widget(nueva_field)
        content.add_widget(confirmar_field)
        
        dialog = MDDialog(
            title="Cambiar Contraseña",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="CAMBIAR",
                    on_release=lambda x: self.do_cambiar_password(
                        dialog, actual_field.text, nueva_field.text, confirmar_field.text
                    )
                )
            ]
        )
        dialog.open()
    
    def do_cambiar_password(self, dialog, actual, nueva, confirmar):
        """Cambia la contraseña del usuario."""
        if not all([actual, nueva, confirmar]):
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="Todos los campos son obligatorios",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        if nueva != confirmar:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="Las contraseñas nuevas no coinciden",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        if len(nueva) < 6:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="La contraseña debe tener al menos 6 caracteres",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        app = App.get_running_app()
        success, data = app.api_request('PUT', '/api/usuarios/cambiar-password', {
            'password_actual': actual,
            'password_nueva': nueva
        })
        
        dialog.dismiss()
        
        if success:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Éxito",
                text="Contraseña actualizada correctamente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
        else:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text=f"No se pudo cambiar la contraseña: {data}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
    
    def show_reportes(self, *args):
        """Muestra reportes y estadísticas completas."""
        app = App.get_running_app()
        
        # Obtener resumen semanal
        success, data = app.api_request('GET', '/api/pagos/resumen/semanal')
        
        if not success:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="No se pudo cargar el reporte",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        base = data.get('base', 0)
        gastos = data.get('gastos', 0)
        efectivo = data.get('efectivo', 0)
        digital = data.get('digital', 0)
        cobrado = data.get('total_cobrado', 0)
        clientes_pagaron = data.get('clientes_pagaron', 0)
        neto = data.get('neto', 0)
        
        reporte_text = f"""
╔═══════════════════════════╗
║   REPORTE SEMANAL        ║
╚═══════════════════════════╝

💵 BASE INICIAL
   ${base:,.0f}

💰 COBROS
   Efectivo: ${efectivo:,.0f}
   Digital: ${digital:,.0f}
   ─────────────────────
   Total: ${cobrado:,.0f}
   
   👥 Clientes que pagaron: {clientes_pagaron}

💸 GASTOS
   ${gastos:,.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━
✅ NETO (Cobrado - Gastos)
   ${neto:,.0f}

📊 EN MANO
   Base + Cobrado - Gastos:
   ${base + cobrado - gastos:,.0f}
   
   (Menos Digital: ${digital:,.0f})
   Efectivo Real: ${base + efectivo - gastos:,.0f}
"""
        
        from kivymd.uix.dialog import MDDialog
        MDDialog(
            title="Reportes y Estadísticas",
            text=reporte_text,
            size_hint=(0.9, None),
            height=dp(600),
            buttons=[MDFlatButton(text="CERRAR", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
        ).open()
