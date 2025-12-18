"""
Pantalla de registro de pagos
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.app import App


class PagosScreen(MDScreen):
    """Pantalla de registro de pagos."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
    
    def on_enter(self):
        """Se ejecuta al entrar a la pantalla."""
        self.clear_widgets()
        self.build_ui()
    
    def build_ui(self):
        """Construye la interfaz de usuario."""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back
        )
        header.add_widget(back_btn)
        header.add_widget(MDLabel(text="PAGOS", font_style="H6"))
        layout.add_widget(header)
        
        # Botones de acción
        actions_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_registrar = MDRaisedButton(
            text="REGISTRAR",
            size_hint_x=0.33,
            on_release=self.show_registrar_pago
        )
        actions_box.add_widget(btn_registrar)
        
        btn_historial = MDRaisedButton(
            text="HISTORIAL",
            size_hint_x=0.33,
            md_bg_color=(0.2, 0.4, 0.6, 1),
            on_release=self.show_historial
        )
        actions_box.add_widget(btn_historial)
        
        from kivymd.uix.button import MDIconButton
        btn_filtros = MDIconButton(
            icon="filter",
            on_release=self.show_filtros_pagos
        )
        actions_box.add_widget(btn_filtros)
        
        layout.add_widget(actions_box)
        
        # Variables para filtros
        self.filtro_pagos = {'tipo': None}
        
        # Área de contenido
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        self.content_area = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.content_area.bind(minimum_height=self.content_area.setter('height'))
        scroll.add_widget(self.content_area)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        # Mostrar resumen por defecto
        self.show_resumen()
    
    def show_resumen(self):
        """Muestra resumen de pagos del día."""
        self.content_area.clear_widgets()
        
        app = App.get_running_app()
        success, data = app.api_request('GET', '/api/pagos/resumen/hoy')
        
        if success:
            resumen = MDLabel(
                text=f"""RESUMEN DE HOY\n\nEfectivo: ${data.get('efectivo', 0):,.0f}\nDigital: ${data.get('digital', 0):,.0f}\nTotal: ${data.get('total_cobrado', 0):,.0f}\n\nPagos: {data.get('num_pagos', 0)}""",
                size_hint_y=None,
                height=dp(200)
            )
            self.content_area.add_widget(resumen)
    
    def show_registrar_pago(self, *args):
        """Muestra diálogo para registrar pago."""
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(250))
        
        # Búsqueda de cliente
        buscar_field = MDTextField(hint_text="Buscar cliente (nombre o cédula)", mode="rectangle")
        content.add_widget(buscar_field)
        
        # Lista de resultados
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.list import MDList, OneLineListItem
        scroll = ScrollView(size_hint_y=0.3)
        self.clientes_resultado = MDList()
        scroll.add_widget(self.clientes_resultado)
        content.add_widget(scroll)
        
        self.cliente_seleccionado = {'id': None, 'nombre': ''}
        cliente_label = MDLabel(text="Cliente: No seleccionado", size_hint_y=None, height=dp(30))
        content.add_widget(cliente_label)
        
        monto_field = MDTextField(hint_text="Monto", mode="rectangle")
        content.add_widget(monto_field)
        
        # Búsqueda en tiempo real
        buscar_field.bind(text=lambda instance, value: self.buscar_cliente_pago(value, cliente_label))
        
        # Botones de tipo de pago
        tipo_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        dialog = MDDialog(
            title="Registrar Pago",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="EFECTIVO",
                    on_release=lambda x: self.registrar_pago(dialog, None, monto_field.text, 'efectivo')
                ),
                MDRaisedButton(
                    text="DIGITAL",
                    on_release=lambda x: self.registrar_pago(dialog, None, monto_field.text, 'digital')
                )
            ]
        )
        dialog.open()
    
    def buscar_cliente_pago(self, termino, label):
        """Busca clientes para registrar pago."""
        if len(termino) < 2:
            self.clientes_resultado.clear_widgets()
            return
        
        app = App.get_running_app()
        success, data = app.api_request('GET', f'/api/clientes?search={termino}')
        
        self.clientes_resultado.clear_widgets()
        if success and isinstance(data, list):
            from kivymd.uix.list import OneLineListItem
            for cliente in data[:5]:  # Máximo 5 resultados
                item = OneLineListItem(
                    text=f"{cliente['nombre']} - {cliente.get('cedula', 'S/C')}",
                    on_release=lambda x, c=cliente, lbl=label: self.seleccionar_cliente_pago(c, lbl)
                )
                self.clientes_resultado.add_widget(item)
    
    def seleccionar_cliente_pago(self, cliente, label):
        """Selecciona un cliente para el pago."""
        self.cliente_seleccionado['id'] = cliente['id']
        self.cliente_seleccionado['nombre'] = cliente['nombre']
        label.text = f"Cliente: {cliente['nombre']}"
    
    def registrar_pago(self, dialog, cliente_id_placeholder, monto, tipo_pago):
        """Registra un pago."""
        cliente_id = self.cliente_seleccionado.get('id')
        
        if not cliente_id:
            self.show_dialog("Error", "Debes seleccionar un cliente")
            return
        
        try:
            monto = float(monto)
        except ValueError:
            self.show_dialog("Error", "Monto inválido")
            return
        
        app = App.get_running_app()
        success, data = app.api_request('POST', '/api/pagos', {
            'cliente_id': cliente_id,
            'monto': monto,
            'tipo_pago': tipo_pago
        })
        
        if success:
            dialog.dismiss()
            self.show_dialog("Éxito", "Pago registrado correctamente")
            self.show_resumen()
        else:
            self.show_dialog("Error", str(data))
    
    def show_filtros_pagos(self, *args):
        """Muestra diálogo de filtros para pagos."""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.list import MDList, OneLineListItem
        from kivy.uix.scrollview import ScrollView
        
        content = ScrollView(size_hint_y=None, height=dp(200))
        lista = MDList()
        
        filtros = [('Todos', None), ('Efectivo', 'efectivo'), ('Digital', 'digital')]
        
        for nombre, valor in filtros:
            item = OneLineListItem(
                text=nombre,
                on_release=lambda x, v=valor: self.apply_filter_pagos(v)
            )
            lista.add_widget(item)
        
        content.add_widget(lista)
        
        dialog = MDDialog(
            title="Filtrar Pagos",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CERRAR", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
        self.filter_dialog_pagos = dialog
    
    def apply_filter_pagos(self, tipo):
        """Aplica filtro de tipo de pago."""
        self.filtro_pagos['tipo'] = tipo
        if hasattr(self, 'filter_dialog_pagos'):
            self.filter_dialog_pagos.dismiss()
        self.show_historial()
    
    def show_historial(self, *args):
        """Muestra historial de pagos con opción de eliminar."""
        self.content_area.clear_widgets()
        
        app = App.get_running_app()
        
        # Aplicar filtros si existen
        url = '/api/pagos'
        if hasattr(self, 'filtro_pagos') and self.filtro_pagos.get('tipo'):
            # Necesitaríamos un endpoint que soporte filtro por tipo
            # Por ahora filtramos en el cliente
            pass
        
        success, data = app.api_request('GET', url)
        
        if success and isinstance(data, list):
            # Filtrar en cliente si es necesario
            if hasattr(self, 'filtro_pagos') and self.filtro_pagos.get('tipo'):
                data = [p for p in data if p.get('tipo_pago') == self.filtro_pagos['tipo']]
            
            from kivymd.uix.list import MDList, ThreeLineIconListItem
            from kivymd.uix.button import MDIconButton
            lista = MDList()
            
            for pago in data[:30]:  # Últimos 30 pagos
                item = ThreeLineIconListItem(
                    text=f"${pago.get('monto', 0):,.0f} - {pago.get('tipo_pago', 'N/A').upper()}",
                    secondary_text=f"Cliente: {pago.get('cliente_nombre', 'N/A')}",
                    tertiary_text=f"Fecha: {pago.get('fecha', 'N/A')}",
                    on_release=lambda x, p=pago: self.confirm_delete_pago(p)
                )
                lista.add_widget(item)
            
            if not data:
                from kivymd.uix.label import MDLabel
                self.content_area.add_widget(MDLabel(
                    text="No hay pagos registrados",
                    halign="center",
                    size_hint_y=None,
                    height=dp(100)
                ))
            else:
                self.content_area.add_widget(lista)
                
                # Agregar total
                total = sum(p.get('monto', 0) for p in data)
                from kivymd.uix.label import MDLabel
                self.content_area.add_widget(MDLabel(
                    text=f"\nTotal: ${total:,.0f}\n(Click en un pago para eliminarlo)",
                    halign="center",
                    size_hint_y=None,
                    height=dp(80)
                ))
    
    def show_dialog(self, title, text):
        """Muestra un diálogo."""
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
    
    def confirm_delete_pago(self, pago):
        """Confirma eliminación de un pago."""
        from kivymd.uix.dialog import MDDialog
        
        dialog = MDDialog(
            title="Eliminar Pago",
            text=f"¿Eliminar pago de ${pago.get('monto', 0):,.0f} ({pago.get('tipo_pago', 'N/A')})?",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="ELIMINAR",
                    md_bg_color=(0.6, 0.2, 0.2, 1),
                    on_release=lambda x: self.do_delete_pago(dialog, pago['id'])
                )
            ]
        )
        dialog.open()
    
    def do_delete_pago(self, dialog, pago_id):
        """Elimina el pago."""
        app = App.get_running_app()
        success, data = app.api_request('DELETE', f'/api/pagos/{pago_id}')
        
        dialog.dismiss()
        
        if success:
            self.show_historial()  # Recargar
            self.show_resumen()  # Actualizar resumen
        else:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text=f"No se pudo eliminar el pago: {data}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
    
    def go_back(self, *args):
        """Regresa a la pantalla anterior."""
        self.manager.current = 'home'
