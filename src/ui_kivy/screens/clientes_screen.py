"""
Pantalla de clientes
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.app import App


class ClientesScreen(MDScreen):
    """Pantalla de lista de clientes."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self):
        """Se ejecuta al entrar a la pantalla."""
        self.clear_widgets()
        self.build_ui()
        self.load_clientes()
    
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
        header.add_widget(MDLabel(text="CLIENTES", font_style="H6"))
        layout.add_widget(header)
        
        # Barra de búsqueda y acciones
        search_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        from kivymd.uix.textfield import MDTextField
        self.search_field = MDTextField(
            hint_text="Buscar cliente...",
            mode="rectangle",
            size_hint_x=0.5
        )
        self.search_field.bind(text=self.on_search)
        search_box.add_widget(self.search_field)
        
        filter_btn = MDIconButton(
            icon="filter",
            on_release=self.show_filters
        )
        search_box.add_widget(filter_btn)
        
        add_btn = MDRaisedButton(
            text="+ NUEVO",
            size_hint_x=0.3,
            on_release=self.show_add_cliente
        )
        search_box.add_widget(add_btn)
        layout.add_widget(search_box)
        
        # Variable para filtros
        self.filtro_actual = {'estado': None}
        
        # Lista de clientes
        scroll = ScrollView()
        self.clientes_list = MDList()
        scroll.add_widget(self.clientes_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_clientes(self):
        """Carga la lista de clientes."""
        app = App.get_running_app()
        
        # Construir URL con filtros
        url = '/api/clientes'
        params = []
        if hasattr(self, 'filtro_actual') and self.filtro_actual.get('estado'):
            params.append(f"estado={self.filtro_actual['estado']}")
        
        if params:
            url += '?' + '&'.join(params)
        
        success, data = app.api_request('GET', url)
        
        self.clientes_list.clear_widgets()
        
        if success and isinstance(data, list):
            for cliente in data:
                item = OneLineListItem(
                    text=f"{cliente['nombre']} - ${cliente['monto_prestado']:,.0f}",
                    on_release=lambda x, c=cliente: self.show_cliente_detail(c)
                )
                self.clientes_list.add_widget(item)
            
            if not data:
                self.clientes_list.add_widget(
                    OneLineListItem(text="No hay clientes registrados")
                )
        else:
            self.clientes_list.add_widget(
                OneLineListItem(text="Error cargando clientes")
            )
    
    def show_filters(self, *args):
        """Muestra diálogo de filtros."""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.list import MDList, OneLineListItem
        from kivy.uix.scrollview import ScrollView
        
        content = ScrollView(size_hint_y=None, height=dp(200))
        lista = MDList()
        
        estados = [('Todos', None), ('Activos', 'activo'), ('Pagados', 'pagado'), ('Atrasados', 'atrasado')]
        
        for nombre, valor in estados:
            item = OneLineListItem(
                text=nombre,
                on_release=lambda x, v=valor: self.apply_filter(v)
            )
            lista.add_widget(item)
        
        content.add_widget(lista)
        
        dialog = MDDialog(
            title="Filtrar Clientes",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CERRAR", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
        self.filter_dialog = dialog
    
    def apply_filter(self, estado):
        """Aplica el filtro seleccionado."""
        self.filtro_actual['estado'] = estado
        if hasattr(self, 'filter_dialog'):
            self.filter_dialog.dismiss()
        self.load_clientes()
    
    def on_search(self, instance, value):
        """Filtra clientes al escribir."""
        if not value:
            self.load_clientes()
            return
        
        app = App.get_running_app()
        success, data = app.api_request('GET', f'/api/clientes?search={value}')
        
        self.clientes_list.clear_widgets()
        if success and isinstance(data, list):
            for cliente in data:
                item = OneLineListItem(
                    text=f"{cliente['nombre']} - ${cliente['monto_prestado']:,.0f}",
                    on_release=lambda x, c=cliente: self.show_cliente_detail(c)
                )
                self.clientes_list.add_widget(item)
    
    def show_add_cliente(self, *args):
        """Muestra diálogo para agregar cliente."""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        from kivymd.uix.menu import MDDropdownMenu
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(450))
        
        nombre_field = MDTextField(hint_text="Nombre completo", mode="rectangle")
        cedula_field = MDTextField(hint_text="Cédula", mode="rectangle")
        telefono_field = MDTextField(hint_text="Teléfono", mode="rectangle")
        monto_field = MDTextField(hint_text="Monto del préstamo", mode="rectangle")
        
        content.add_widget(nombre_field)
        content.add_widget(cedula_field)
        content.add_widget(telefono_field)
        content.add_widget(monto_field)
        
        # Selector de tipo plazo
        plazo_seleccionado = {'tipo': 'semanal'}
        
        plazo_label = MDLabel(text="Tipo de plazo: Semanal", size_hint_y=None, height=dp(30))
        content.add_widget(plazo_label)
        
        # Botones de radio para tipo de plazo
        plazos_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        
        from kivymd.uix.button import MDFlatButton
        for plazo in ['diario', 'semanal', 'quincenal', 'mensual']:
            btn = MDFlatButton(
                text=plazo.capitalize(),
                on_release=lambda x, p=plazo, lbl=plazo_label, sel=plazo_seleccionado: self.select_plazo(p, lbl, sel)
            )
            plazos_box.add_widget(btn)
        
        content.add_widget(plazos_box)
        
        dialog = MDDialog(
            title="Nuevo Cliente",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="GUARDAR",
                    on_release=lambda x: self.do_add_cliente(
                        dialog, nombre_field.text, cedula_field.text,
                        telefono_field.text, monto_field.text, plazo_seleccionado['tipo']
                    )
                )
            ]
        )
        dialog.open()
    
    def select_plazo(self, plazo, label, plazo_dict):
        """Actualiza el tipo de plazo seleccionado."""
        plazo_dict['tipo'] = plazo
        label.text = f"Tipo de plazo: {plazo.capitalize()}"
    
    def do_add_cliente(self, dialog, nombre, cedula, telefono, monto, tipo_plazo):
        """Guarda un nuevo cliente."""
        if not all([nombre, cedula, telefono, monto]):
            return
        
        try:
            monto = float(monto)
        except ValueError:
            return
        
        app = App.get_running_app()
        success, data = app.api_request('POST', '/api/clientes', {
            'nombre': nombre,
            'cedula': cedula,
            'telefono': telefono,
            'monto': monto,
            'tipo_plazo': tipo_plazo
        })
        
        if success:
            dialog.dismiss()
            self.load_clientes()
    
    def show_cliente_detail(self, cliente):
        """Muestra los detalles de un cliente."""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        
        # Obtener detalles completos con cálculos desde la API
        app = App.get_running_app()
        success, data = app.api_request('GET', f'/api/clientes/{cliente["id"]}')
        
        if not success:
            MDDialog(
                title="Error",
                text="No se pudieron cargar los detalles del cliente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        # Calcular valores
        monto = data.get('monto_prestado', 0)
        interes = monto * data.get('tasa_interes', 0.20)
        seguro = data.get('seguro', 0)
        total_a_pagar = data.get('total_a_pagar', monto + interes)
        total_pagado = data.get('total_pagado', 0)
        saldo = data.get('saldo_pendiente', total_a_pagar - total_pagado)
        
        detail_text = f"""
Nombre: {data['nombre']}
Cédula: {data.get('cedula', 'N/A')}
Teléfono: {data.get('telefono', 'N/A')}
Tipo: {data.get('tipo_plazo', 'N/A').capitalize()}

Monto Prestado: ${monto:,.0f}
Interés ({data.get('tasa_interes', 0.20)*100:.0f}%): ${interes:,.0f}
Seguro (Descontado): ${seguro:,.0f}
━━━━━━━━━━━━━━━━━━━━
Total a Pagar: ${total_a_pagar:,.0f}

Total Pagado: ${total_pagado:,.0f}
Saldo Pendiente: ${saldo:,.0f}

Estado: {data.get('estado', 'activo').upper()}
"""
        
        dialog_buttons = [
            MDFlatButton(text="CERRAR", on_release=lambda x: x.parent.parent.parent.parent.dismiss()),
            MDRaisedButton(
                text="VER PAGOS",
                on_release=lambda x: self.show_historial_pagos(data['id'])
            ),
            MDRaisedButton(
                text="EDITAR",
                md_bg_color=(0.2, 0.4, 0.6, 1),
                on_release=lambda x: self.show_edit_cliente(data)
            ),
            MDRaisedButton(
                text="ELIMINAR",
                md_bg_color=(0.6, 0.2, 0.2, 1),
                on_release=lambda x: self.confirm_delete_cliente(data)
            )
        ]
        
        MDDialog(
            title="Detalles del Cliente",
            text=detail_text,
            buttons=dialog_buttons
        ).open()
    
    def show_edit_cliente(self, cliente):
        """Muestra diálogo para editar cliente."""
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(200))
        
        nombre_field = MDTextField(hint_text="Nombre", mode="rectangle", text=cliente.get('nombre', ''))
        cedula_field = MDTextField(hint_text="Cédula", mode="rectangle", text=cliente.get('cedula', ''))
        telefono_field = MDTextField(hint_text="Teléfono", mode="rectangle", text=cliente.get('telefono', ''))
        
        content.add_widget(nombre_field)
        content.add_widget(cedula_field)
        content.add_widget(telefono_field)
        
        dialog = MDDialog(
            title="Editar Cliente",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="GUARDAR",
                    on_release=lambda x: self.do_edit_cliente(
                        dialog, cliente['id'], nombre_field.text, cedula_field.text, telefono_field.text
                    )
                )
            ]
        )
        dialog.open()
    
    def do_edit_cliente(self, dialog, cliente_id, nombre, cedula, telefono):
        """Actualiza los datos del cliente."""
        if not all([nombre, cedula, telefono]):
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="Todos los campos son obligatorios",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        app = App.get_running_app()
        # Obtener datos completos del cliente para mantener los demás campos
        success, cliente = app.api_request('GET', f'/api/clientes/{cliente_id}')
        
        if not success:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text="No se pudo cargar el cliente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        # Actualizar solo nombre, cédula y teléfono
        success, data = app.api_request('PUT', f'/api/clientes/{cliente_id}', {
            'nombre': nombre,
            'cedula': cedula,
            'telefono': telefono,
            'monto_prestado': cliente['monto_prestado'],
            'fecha_prestamo': cliente['fecha_prestamo'],
            'tipo_plazo': cliente['tipo_plazo'],
            'tasa_interes': cliente['tasa_interes'],
            'seguro': cliente['seguro'],
            'cuota_minima': cliente['cuota_minima'],
            'dias_plazo': cliente['dias_plazo']
        })
        
        if success:
            dialog.dismiss()
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Éxito",
                text="Cliente actualizado correctamente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            self.load_clientes()
        else:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text=f"No se pudo actualizar: {data}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
    
    def confirm_delete_cliente(self, cliente):
        """Confirma eliminación de cliente."""
        from kivymd.uix.dialog import MDDialog
        
        # Verificar si tiene saldo pendiente
        saldo = cliente.get('saldo_pendiente', 0)
        
        if saldo > 0:
            MDDialog(
                title="No se puede eliminar",
                text=f"El cliente tiene un saldo pendiente de ${saldo:,.0f}. Solo se pueden eliminar clientes sin deuda.",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            return
        
        dialog = MDDialog(
            title="Confirmar Eliminación",
            text=f"¿Estás seguro de eliminar a {cliente['nombre']}?\n\nEsta acción marcará al cliente como inactivo.",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="ELIMINAR",
                    md_bg_color=(0.6, 0.2, 0.2, 1),
                    on_release=lambda x: self.do_delete_cliente(dialog, cliente['id'])
                )
            ]
        )
        dialog.open()
    
    def do_delete_cliente(self, dialog, cliente_id):
        """Elimina (inactiva) el cliente."""
        app = App.get_running_app()
        success, data = app.api_request('DELETE', f'/api/clientes/{cliente_id}')
        
        dialog.dismiss()
        
        if success:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Éxito",
                text="Cliente eliminado correctamente",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
            self.load_clientes()
        else:
            from kivymd.uix.dialog import MDDialog
            MDDialog(
                title="Error",
                text=f"No se pudo eliminar: {data}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
            ).open()
    
    def show_historial_pagos(self, cliente_id):
        """Muestra historial de pagos del cliente."""
        app = App.get_running_app()
        success, data = app.api_request('GET', f'/api/pagos/cliente/{cliente_id}')
        
        if success and isinstance(data, list):
            total_pagado = sum(p.get('monto', 0) for p in data)
            historial_text = f"Total Pagado: ${total_pagado:,.0f}\n\n" + "\n".join([
                f"{p.get('fecha', 'N/A')}: ${p.get('monto', 0):,.0f} ({p.get('tipo_pago', 'N/A')})"
                for p in data[:20]  # Últimos 20 pagos
            ])
            if len(data) == 0:
                historial_text = "Sin pagos registrados"
            elif len(data) > 20:
                historial_text += f"\n\n... y {len(data) - 20} pagos más"
        else:
            historial_text = "Error cargando historial"
        
        from kivymd.uix.dialog import MDDialog
        MDDialog(
            title="Historial de Pagos",
            text=historial_text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.parent.dismiss())]
        ).open()
    
    def go_back(self, *args):
        """Regresa a la pantalla anterior."""
        self.manager.current = 'home'
