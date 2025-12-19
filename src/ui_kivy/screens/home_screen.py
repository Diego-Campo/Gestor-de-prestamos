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
        
        # Contenido según el rol
        if app.es_admin:
            # ADMIN: Panel de supervisión embebido en la página principal
            # Card para estadísticas generales (más compacto para móvil)
            self.card_stats = MDCard(
                orientation='vertical',
                padding=dp(10),
                size_hint_y=None,
                height=dp(150)
            )
            self.label_stats = MDLabel(
                text="Cargando estadísticas...",
                theme_text_color="Primary",
                font_size='11sp'
            )
            self.card_stats.add_widget(self.label_stats)
            content.add_widget(self.card_stats)
            
            # Separador más compacto
            sep_label = MDLabel(
                text="═══ COBRADORES ═══",
                size_hint_y=None,
                height=dp(30),
                halign='center',
                font_size='13sp',
                bold=True
            )
            content.add_widget(sep_label)
            
            # Contenedor para botones de cobradores (más compacto)
            self.cobradores_container = BoxLayout(
                orientation='vertical',
                spacing=dp(5),
                size_hint_y=None
            )
            self.cobradores_container.bind(minimum_height=self.cobradores_container.setter('height'))
            content.add_widget(self.cobradores_container)
            
            # Botones de acción apilados verticalmente para móvil
            botones_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(75), spacing=dp(5))
            
            btn_usuarios = MDRaisedButton(
                text="Gestión Usuarios",
                size_hint_y=None,
                height=dp(35),
                md_bg_color=(0.3, 0.5, 0.3, 1),
                on_release=self.show_usuarios
            )
            botones_box.add_widget(btn_usuarios)
            
            btn_reportes = MDRaisedButton(
                text="Ver Reportes",
                size_hint_y=None,
                height=dp(35),
                md_bg_color=(0.2, 0.4, 0.6, 1),
                on_release=self.show_reportes
            )
            botones_box.add_widget(btn_reportes)
            
            content.add_widget(botones_box)
            
        else:
            # COBRADOR: Resumen y opciones operativas
            # Card de resumen solo para cobradores
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
            
            # COBRADOR: Opciones de operación diaria
            btn_clientes = MDRaisedButton(
                text="GESTIONAR CLIENTES",
                size_hint_y=None,
                height=dp(50),
                on_release=self.go_to_clientes
            )
            content.add_widget(btn_clientes)
            
            btn_pagos = MDRaisedButton(
                text="REGISTRAR PAGO",
                size_hint_y=None,
                height=dp(50),
                on_release=self.go_to_pagos
            )
            content.add_widget(btn_pagos)
            
            # Botones de base y gastos (solo cobradores)
            base_gastos_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
            
            btn_base = MDRaisedButton(
                text="AGREGAR BASE",
                size_hint_x=0.5,
                md_bg_color=(0.2, 0.6, 0.2, 1),
                on_release=self.show_agregar_base
            )
            base_gastos_box.add_widget(btn_base)
            
            btn_gasto = MDRaisedButton(
                text="REGISTRAR GASTO",
                size_hint_x=0.5,
                md_bg_color=(0.6, 0.2, 0.2, 1),
                on_release=self.show_registrar_gasto
            )
            base_gastos_box.add_widget(btn_gasto)
            
            content.add_widget(base_gastos_box)
            
            # Botón de reportes solo para cobradores
            btn_reportes = MDRaisedButton(
                text="VER REPORTES",
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
        """Carga el resumen del día y semanal (cobradores) o panel de supervisión (admin)."""
        app = App.get_running_app()
        
        # Admin: cargar panel de supervisión
        if app.es_admin:
            self.load_panel_supervision()
            return
        
        success_hoy, data_hoy = app.api_request('GET', '/api/pagos/resumen/hoy')
        success_semanal, data_semanal = app.api_request('GET', '/api/pagos/resumen/semanal')
        
        if success_hoy:
            resumen_text = f"""═══ RESUMEN DE HOY ═══

Efectivo: ${data_hoy.get('efectivo', 0):,.0f}
Digital: ${data_hoy.get('digital', 0):,.0f}
━━━━━━━━━━━━━━━━━━━━
Total Cobrado: ${data_hoy.get('total_cobrado', 0):,.0f}

Pagos Registrados: {data_hoy.get('num_pagos', 0)}
Clientes Activos: {data_hoy.get('clientes_activos', 0)}
"""
            
            if success_semanal:
                base = data_semanal.get('base', 0)
                gastos = data_semanal.get('gastos', 0)
                cobrado_semanal = data_semanal.get('total_cobrado', 0)
                neto = cobrado_semanal - gastos
                
                resumen_text += f"""
═══ RESUMEN SEMANAL ═══

Base: ${base:,.0f}
Cobrado: ${cobrado_semanal:,.0f}
Gastos: ${gastos:,.0f}
━━━━━━━━━━━━━━━━━━━━
Neto: ${neto:,.0f}
"""
            
            self.label_resumen.text = resumen_text
        else:
            self.label_resumen.text = "Error cargando resumen"
    
    def load_panel_supervision(self):
        """Carga el panel de supervisión con estadísticas y lista de cobradores."""
        app = App.get_running_app()
        success, data = app.api_request('GET', '/api/usuarios/cobradores/resumen')
        
        if not success:
            self.label_stats.text = "Error cargando estadísticas"
            return
        
        # Calcular totales
        total_clientes = sum(c['clientes_activos'] for c in data)
        total_cobrado = sum(c['cobrado_hoy'] for c in data)
        total_base = sum(c['base_hoy'] for c in data)
        total_gastos = sum(c['gastos_hoy'] for c in data)
        ganancia_neta = total_cobrado - total_gastos
        
        # Actualizar estadísticas generales (formato compacto para móvil)
        stats_text = f"""═══ ESTADÍSTICAS ═══
Cobradores: {len(data)} | Clientes: {total_clientes}
Cobrado: ${total_cobrado:,.0f}
Base: ${total_base:,.0f} | Gastos: ${total_gastos:,.0f}
━━━━━━━━━━━━━━━━
Ganancia: ${ganancia_neta:,.0f}"""
        self.label_stats.text = stats_text
        
        # Limpiar y agregar botones de cobradores (más compactos)
        self.cobradores_container.clear_widgets()
        
        for cobrador in data:
            # Texto más corto para móvil (2 líneas)
            btn = MDRaisedButton(
                text=f"{cobrador['nombre'][:20]}\n{cobrador['clientes_activos']} cli. | ${cobrador['cobrado_hoy']:,.0f}",
                size_hint_y=None,
                height=dp(45),
                md_bg_color=(0.3, 0.5, 0.7, 1),
                font_size='11sp'
            )
            btn.bind(on_release=lambda x, c=cobrador: self.show_detalle_cobrador(c))
            self.cobradores_container.add_widget(btn)
    
    def go_to_clientes(self, *args):
        """Navega a la pantalla de clientes."""
        self.manager.current = 'clientes'
    
    def go_to_pagos(self, *args):
        """Navega a la pantalla de pagos."""
        self.manager.current = 'pagos'
    
    def mostrar_clientes_tabla(self, clientes):
        """Muestra los clientes en formato lista optimizado para móvil"""
        self.content_clientes.clear_widgets()
        
        if not clientes:
            lbl_empty = MDLabel(
                text="No hay clientes",
                size_hint_y=None,
                height=dp(50),
                halign='center'
            )
            self.content_clientes.add_widget(lbl_empty)
            return
        
        # Mostrar cada cliente en formato compacto tipo tarjeta
        for cliente in clientes:
            # Mapeo de tipo_plazo
            plazo_map = {
                'diario': 'Diario',
                'semanal': 'Semanal',
                'quincenal': 'Quincenal',
                'mensual': 'Mensual'
            }
            plazo_texto = plazo_map.get(cliente['tipo_plazo'], cliente['tipo_plazo'])
            
            fecha = cliente['fecha_prestamo'][:10] if cliente.get('fecha_prestamo') else 'N/A'
            monto = f"${cliente['monto_prestado']:,.0f}"
            abonado = f"${cliente.get('total_pagado', 0):,.0f}"
            
            # Formato de 2 líneas para móvil
            linea1 = f"[b]{cliente['nombre'][:22]}[/b] | {cliente['telefono']}"
            linea2 = f"Monto: {monto} | Abonado: {abonado} | {plazo_texto} | {fecha}"
            
            from kivymd.uix.card import MDCard
            fila = MDCard(
                orientation='vertical',
                padding=(dp(8), dp(5)),
                size_hint_y=None,
                height=dp(48),
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )
            
            lbl1 = MDLabel(
                text=linea1,
                size_hint_y=None,
                height=dp(18),
                font_size='11sp',
                markup=True
            )
            lbl2 = MDLabel(
                text=linea2,
                size_hint_y=None,
                height=dp(16),
                font_size='10sp',
                markup=True,
                color=(0.3, 0.3, 0.3, 1)
            )
            fila.add_widget(lbl1)
            fila.add_widget(lbl2)
            self.content_clientes.add_widget(fila)
    
    def filtrar_clientes_cobrador(self, instance, value):
        """Filtra los clientes por nombre o cédula"""
        if not hasattr(self, 'clientes_cobrador_completos'):
            return
        
        if not value:
            # Sin filtro, mostrar todos
            self.mostrar_clientes_tabla(self.clientes_cobrador_completos)
            return
        
        # Filtrar por nombre o cédula
        value_lower = value.lower()
        clientes_filtrados = [
            c for c in self.clientes_cobrador_completos
            if value_lower in c['nombre'].lower() or value_lower in c.get('cedula', '').lower()
        ]
        
        self.mostrar_clientes_tabla(clientes_filtrados)
    
    def show_detalle_cobrador(self, cobrador):
        """Muestra estadísticas y clientes de un cobrador específico"""
        # Cerrar el diálogo de supervisión
        if hasattr(self, 'dialog_supervision'):
            self.dialog_supervision.dismiss()
        
        # Obtener clientes del cobrador
        app = App.get_running_app()
        success, clientes = app.api_request('GET', f'/api/clientes?usuario_id={cobrador["id"]}')
        
        if not success:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="No se pudo cargar información de clientes",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        # Guardar datos para filtrado
        self.clientes_cobrador_completos = clientes
        self.cobrador_actual = cobrador
        
        # Crear contenedor principal (optimizado para móvil)
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.textfield import MDTextField
        
        container = MDBoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10), size_hint_y=None, height=dp(450))
        
        # Estadísticas del cobrador (compacto)
        stats_text = f"""═══ {cobrador['nombre'][:20]} ═══
Clientes: {cobrador['clientes_activos']} | Cobrado: ${cobrador['cobrado_hoy']:,.0f}
Base: ${cobrador['base_hoy']:,.0f} | Gastos: ${cobrador['gastos_hoy']:,.0f}
Ganancia: ${cobrador['cobrado_hoy'] - cobrador['gastos_hoy']:,.0f}"""
        
        lbl_stats = MDLabel(
            text=stats_text,
            size_hint_y=None,
            height=dp(70),
            font_size='11sp'
        )
        container.add_widget(lbl_stats)
        
        # Campo de búsqueda más compacto
        self.search_field_cobrador = MDTextField(
            hint_text="Buscar cliente",
            mode="rectangle",
            size_hint_y=None,
            height=dp(45),
            font_size='12sp'
        )
        self.search_field_cobrador.bind(text=self.filtrar_clientes_cobrador)
        container.add_widget(self.search_field_cobrador)
        
        # Contenedor scrollable para lista de clientes
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(size_hint_y=None, height=dp(315))
        
        self.content_clientes = MDBoxLayout(orientation='vertical', spacing=dp(3), size_hint_y=None)
        self.content_clientes.bind(minimum_height=self.content_clientes.setter('height'))
        
        # Mostrar todos los clientes
        self.mostrar_clientes_tabla(clientes)
        
        scroll.add_widget(self.content_clientes)
        container.add_widget(scroll)

        
        from kivymd.uix.dialog import MDDialog
        self.dialog_detalle = MDDialog(
            title=f"Detalles - {cobrador['nombre']}",
            type="custom",
            content_cls=container,
            buttons=[
                MDFlatButton(text="VOLVER", on_release=lambda x: self.volver_supervision()),
                MDFlatButton(text="CERRAR", on_release=lambda x: self.dialog_detalle.dismiss())
            ]
        )
        self.dialog_detalle.open()
    
    def volver_supervision(self):
        """Vuelve al panel de supervisión"""
        if hasattr(self, 'dialog_detalle'):
            self.dialog_detalle.dismiss()
        self.show_panel_supervision(None)
    
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

BASE INICIAL
   ${base:,.0f}

COBROS
   Efectivo: ${efectivo:,.0f}
   Digital: ${digital:,.0f}
   ─────────────────────
   Total: ${cobrado:,.0f}
   
   Clientes que pagaron: {clientes_pagaron}

GASTOS
   ${gastos:,.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━
NETO (Cobrado - Gastos)
   ${neto:,.0f}

EN MANO
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
    
    def show_panel_supervision(self, *args):
        """Muestra panel de supervisión con estadísticas de todos los cobradores (como v1)."""
        app = App.get_running_app()
        success, data = app.api_request('GET', '/api/usuarios/cobradores/resumen')
        
        if not success or not data:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="No se pudo cargar información de cobradores",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        # Calcular totales
        total_clientes = sum(c['clientes_activos'] for c in data)
        total_cobrado = sum(c['cobrado_hoy'] for c in data)
        total_base = sum(c['base_hoy'] for c in data)
        total_gastos = sum(c['gastos_hoy'] for c in data)
        ganancia_neta = total_cobrado - total_gastos
        
        # Crear texto del resumen general
        resumen_text = f"""═══ ESTADÍSTICAS GLOBALES ═══

Total Cobradores: {len(data)}
Total Clientes Activos: {total_clientes}

Total Cobrado Hoy: ${total_cobrado:,.0f}
Total Base: ${total_base:,.0f}
Total Gastos: ${total_gastos:,.0f}
━━━━━━━━━━━━━━━━━━━━
Ganancia Neta: ${ganancia_neta:,.0f}
"""
        
        # Crear contenido con botones para cada cobrador
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.scrollview import ScrollView
        
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Label con estadísticas generales
        lbl_general = MDLabel(
            text=resumen_text,
            size_hint_y=None,
            height=dp(220)
        )
        content.add_widget(lbl_general)
        
        # Separador
        sep = MDLabel(
            text="═══ SELECCIONAR COBRADOR ═══",
            size_hint_y=None,
            height=dp(30),
            halign='center'
        )
        content.add_widget(sep)
        
        # Botón por cada cobrador
        for cobrador in data:
            btn = MDRaisedButton(
                text=f"{cobrador['nombre']} - {cobrador['clientes_activos']} clientes",
                size_hint_y=None,
                height=dp(50),
                md_bg_color=(0.3, 0.5, 0.7, 1)
            )
            btn.bind(on_release=lambda x, c=cobrador: self.show_detalle_cobrador(c))
            content.add_widget(btn)
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(content)
        
        from kivymd.uix.dialog import MDDialog
        self.dialog_supervision = MDDialog(
            title="Panel de Supervisión",
            type="custom",
            content_cls=scroll,
            size_hint=(0.9, 0.8),
            buttons=[MDFlatButton(text="CERRAR", on_release=lambda x: self.dialog_supervision.dismiss())]
        )
        self.dialog_supervision.open()
