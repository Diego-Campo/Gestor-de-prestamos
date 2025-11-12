from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QMessageBox, QTableWidget,
                             QTableWidgetItem, QComboBox, QSpinBox, QDoubleSpinBox,
                             QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt

class BasePage(QWidget):
    def __init__(self, usuario_manager):
        super().__init__()
        self.usuario_manager = usuario_manager
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Registrar Base Semanal")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout()
        self.monto_input = QDoubleSpinBox()
        self.monto_input.setRange(0, 1000000000)
        self.monto_input.setDecimals(0)
        self.monto_input.setSuffix(" COP")
        form.addRow("Monto:", self.monto_input)
        
        layout.addLayout(form)

        self.registrar_btn = QPushButton("Registrar Base")
        self.registrar_btn.clicked.connect(self.registrar_base)
        layout.addWidget(self.registrar_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def registrar_base(self):
        if self.usuario_id is None:
            return
        
        monto = self.monto_input.value()
        if monto <= 0:
            QMessageBox.warning(self, "Error", "El monto debe ser mayor a 0")
            return

        self.usuario_manager.registrar_base_semanal(self.usuario_id, monto)
        QMessageBox.information(self, "Éxito", "Base registrada correctamente")
        self.monto_input.setValue(0)

class ClientePage(QWidget):
    def __init__(self, cliente_manager):
        super().__init__()
        self.cliente_manager = cliente_manager
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Registrar Nuevo Cliente")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Formulario
        form = QFormLayout()
        
        self.nombre_input = QLineEdit()
        self.cedula_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.monto_input = QDoubleSpinBox()
        self.monto_input.setRange(0, 1000000000)
        self.monto_input.setDecimals(0)
        self.monto_input.setSuffix(" COP")
        
        self.plazo_combo = QComboBox()
        self.plazo_combo.addItems(["Diario", "Semanal", "Quincenal", "Mensual"])
        
        self.tasa_input = QDoubleSpinBox()
        self.tasa_input.setRange(0, 100)
        self.tasa_input.setValue(20)
        self.tasa_input.setSuffix(" %")
        self.tasa_input.setEnabled(False)
        
        form.addRow("Nombre:", self.nombre_input)
        form.addRow("Cédula:", self.cedula_input)
        form.addRow("Teléfono:", self.telefono_input)
        form.addRow("Monto:", self.monto_input)
        form.addRow("Plazo:", self.plazo_combo)
        form.addRow("Tasa de interés:", self.tasa_input)
        
        layout.addLayout(form)

        # Resumen
        self.resumen_group = QGroupBox("Resumen del préstamo")
        resumen_layout = QFormLayout()
        self.cuota_label = QLabel("0 COP")
        self.seguro_label = QLabel("0 COP")
        self.monto_real_label = QLabel("0 COP")
        
        resumen_layout.addRow("Cuota mínima:", self.cuota_label)
        resumen_layout.addRow("Seguro:", self.seguro_label)
        resumen_layout.addRow("Monto a entregar:", self.monto_real_label)
        
        self.resumen_group.setLayout(resumen_layout)
        layout.addWidget(self.resumen_group)

        # Botón registrar
        self.registrar_btn = QPushButton("Registrar Cliente")
        self.registrar_btn.clicked.connect(self.registrar_cliente)
        layout.addWidget(self.registrar_btn)
        
        layout.addStretch()
        self.setLayout(layout)

        # Conexiones
        self.monto_input.valueChanged.connect(self.actualizar_resumen)
        self.monto_input.valueChanged.connect(self.check_monto)

    def check_monto(self, valor):
        self.tasa_input.setEnabled(valor > 500000)
        if valor <= 500000:
            self.tasa_input.setValue(20)

    def actualizar_resumen(self):
        monto = self.monto_input.value()
        if monto > 0:
            cuota_minima = (monto // 50000) * 2000 if monto >= 50000 else 2000
            self.cuota_label.setText(f"{cuota_minima:,.0f} COP")
            self.seguro_label.setText(f"{cuota_minima:,.0f} COP")
            self.monto_real_label.setText(f"{(monto - cuota_minima):,.0f} COP")

    def registrar_cliente(self):
        if self.usuario_id is None:
            return
            
        nombre = self.nombre_input.text()
        cedula = self.cedula_input.text()
        telefono = self.telefono_input.text()
        monto = self.monto_input.value()
        plazos = {
            "Diario": "diario",
            "Semanal": "semanal",
            "Quincenal": "quincenal",
            "Mensual": "mensual"
        }
        tipo_plazo = plazos[self.plazo_combo.currentText()]
        tasa_interes = self.tasa_input.value() / 100

        if not all([nombre, cedula, telefono]) or monto <= 0:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        self.cliente_manager.registrar_cliente(
            self.usuario_id, nombre, cedula, telefono, monto, tipo_plazo, tasa_interes
        )
        
        QMessageBox.information(self, "Éxito", "Cliente registrado correctamente")
        self.limpiar_campos()

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.cedula_input.clear()
        self.telefono_input.clear()
        self.monto_input.setValue(0)
        self.plazo_combo.setCurrentIndex(0)
        self.tasa_input.setValue(20)

class PagoPage(QWidget):
    def __init__(self, cliente_manager):
        super().__init__()
        self.cliente_manager = cliente_manager
        self.usuario_id = None
        self.todos_clientes = []  # Lista para almacenar todos los clientes
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Registrar Pago")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Filtro de búsqueda
        busqueda_layout = QHBoxLayout()
        busqueda_layout.addWidget(QLabel("Buscar cliente:"))
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Escriba el nombre del cliente...")
        self.busqueda_input.textChanged.connect(self.filtrar_clientes)
        busqueda_layout.addWidget(self.busqueda_input)
        layout.addLayout(busqueda_layout)

        # Selección de cliente
        self.cliente_combo = QComboBox()
        layout.addWidget(QLabel("Cliente:"))
        layout.addWidget(self.cliente_combo)

        # Monto
        form = QFormLayout()
        self.monto_input = QDoubleSpinBox()
        self.monto_input.setRange(0, 1000000000)
        self.monto_input.setDecimals(0)
        self.monto_input.setSuffix(" COP")
        
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Efectivo", "Digital"])
        
        form.addRow("Monto:", self.monto_input)
        form.addRow("Tipo de pago:", self.tipo_combo)
        
        layout.addLayout(form)

        self.registrar_btn = QPushButton("Registrar Pago")
        self.registrar_btn.clicked.connect(self.registrar_pago)
        layout.addWidget(self.registrar_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.cargar_clientes()

    def cargar_clientes(self):
        if self.usuario_id is None:
            return
            
        self.cliente_combo.clear()
        self.todos_clientes = self.cliente_manager.obtener_clientes(self.usuario_id)
        for cliente in self.todos_clientes:
            self.cliente_combo.addItem(f"{cliente[1]} - CC: {cliente[2]}", cliente[0])

    def filtrar_clientes(self):
        """Filtra los clientes según el texto de búsqueda."""
        if self.usuario_id is None:
            return
        
        texto_busqueda = self.busqueda_input.text().lower()
        self.cliente_combo.clear()
        
        for cliente in self.todos_clientes:
            nombre = cliente[1].lower()
            cedula = cliente[2]
            # Buscar por nombre o cédula
            if texto_busqueda in nombre or texto_busqueda in cedula:
                self.cliente_combo.addItem(f"{cliente[1]} - CC: {cliente[2]}", cliente[0])

    def registrar_pago(self):
        if self.cliente_combo.currentData() is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente")
            return

        monto = self.monto_input.value()
        if monto <= 0:
            QMessageBox.warning(self, "Error", "El monto debe ser mayor a 0")
            return

        cliente_id = self.cliente_combo.currentData()
        tipo_pago = "efectivo" if self.tipo_combo.currentText() == "Efectivo" else "digital"

        self.cliente_manager.registrar_pago(cliente_id, monto, tipo_pago)
        QMessageBox.information(self, "Éxito", "Pago registrado correctamente")
        self.monto_input.setValue(0)

class GastoPage(QWidget):
    def __init__(self, usuario_manager):
        super().__init__()
        self.usuario_manager = usuario_manager
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Registrar Gasto")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout()
        
        self.monto_input = QDoubleSpinBox()
        self.monto_input.setRange(0, 1000000000)
        self.monto_input.setDecimals(0)
        self.monto_input.setSuffix(" COP")
        
        self.descripcion_input = QLineEdit()
        
        form.addRow("Monto:", self.monto_input)
        form.addRow("Descripción:", self.descripcion_input)
        
        layout.addLayout(form)

        self.registrar_btn = QPushButton("Registrar Gasto")
        self.registrar_btn.clicked.connect(self.registrar_gasto)
        layout.addWidget(self.registrar_btn)
        
        layout.addStretch()
        self.setLayout(layout)

    def registrar_gasto(self):
        if self.usuario_id is None:
            return
            
        monto = self.monto_input.value()
        descripcion = self.descripcion_input.text()

        if monto <= 0 or not descripcion:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        self.usuario_manager.registrar_gasto(self.usuario_id, monto, descripcion)
        QMessageBox.information(self, "Éxito", "Gasto registrado correctamente")
        
        self.monto_input.setValue(0)
        self.descripcion_input.clear()

class SupervisorPage(QWidget):
    def __init__(self, usuario_manager, cliente_manager):
        super().__init__()
        self.usuario_manager = usuario_manager
        self.cliente_manager = cliente_manager
        self.db = usuario_manager.db  # Obtener referencia a la base de datos
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Panel de Supervisión")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # ComboBox para seleccionar cobrador
        self.cobrador_combo = QComboBox()
        layout.addWidget(QLabel("Seleccionar Cobrador:"))
        layout.addWidget(self.cobrador_combo)

        # Información del cobrador
        self.info_group = QGroupBox("Información del Cobrador")
        info_layout = QFormLayout()
        
        self.clientes_label = QLabel("0")
        self.prestado_label = QLabel("0 COP")
        self.cobrado_label = QLabel("0 COP")
        self.gastos_label = QLabel("0 COP")
        
        info_layout.addRow("Clientes activos:", self.clientes_label)
        info_layout.addRow("Prestado hoy:", self.prestado_label)
        info_layout.addRow("Cobrado hoy:", self.cobrado_label)
        info_layout.addRow("Gastos hoy:", self.gastos_label)
        
        self.info_group.setLayout(info_layout)
        layout.addWidget(self.info_group)

        # Tabla de historial
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Fecha", "Prestado", "Cobrado", "Gastos", "Balance"
        ])
        layout.addWidget(self.tabla)

        layout.addStretch()
        self.setLayout(layout)

        # Conexiones
        self.cobrador_combo.currentIndexChanged.connect(self.actualizar_info_cobrador)

    def showEvent(self, event):
        super().showEvent(event)
        self.cargar_cobradores()

    def cargar_cobradores(self):
        self.cobrador_combo.clear()
        self.db.cursor.execute('''
            SELECT id, nombre, username 
            FROM usuarios 
            WHERE es_admin = 0
        ''')
        cobradores = self.db.cursor.fetchall()
        for cobrador in cobradores:
            self.cobrador_combo.addItem(
                f"{cobrador[1]} ({cobrador[2]})", 
                cobrador[0]
            )

    def actualizar_info_cobrador(self):
        cobrador_id = self.cobrador_combo.currentData()
        if not cobrador_id:
            return

        # Actualizar información actual
        actividad = self.usuario_manager.obtener_actividad_cobrador(cobrador_id)
        self.clientes_label.setText(str(actividad['clientes_activos']))
        self.prestado_label.setText(f"{actividad['prestado_hoy']:,.0f} COP")
        self.cobrado_label.setText(f"{actividad['cobrado_hoy']:,.0f} COP")
        self.gastos_label.setText(f"{actividad['gastos_hoy']:,.0f} COP")

        # Actualizar historial
        historial = self.usuario_manager.obtener_historial_cobrador(cobrador_id)
        self.tabla.setRowCount(len(historial))
        
        for i, dia in enumerate(historial):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(dia['fecha'])))
            self.tabla.setItem(i, 1, QTableWidgetItem(f"{dia['prestado_hoy']:,.0f}"))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"{dia['cobrado_hoy']:,.0f}"))
            self.tabla.setItem(i, 3, QTableWidgetItem(f"{dia['gastos_hoy']:,.0f}"))
            balance = dia['cobrado_hoy'] - dia['prestado_hoy'] - dia['gastos_hoy']
            self.tabla.setItem(i, 4, QTableWidgetItem(f"{balance:,.0f}"))

        self.tabla.resizeColumnsToContents()

class UsuariosPage(QWidget):
    def __init__(self, usuario_manager):
        super().__init__()
        self.usuario_manager = usuario_manager
        self.db = usuario_manager.db
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Gestión de Usuarios")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tabla de usuarios
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Usuario", "Nombre", "Acciones"
        ])
        layout.addWidget(self.tabla)
        
        # Ajustar el estilo de la tabla
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setShowGrid(True)
        
        layout.addStretch()
        self.setLayout(layout)

    def crear_boton_eliminar(self, row, usuario_id):
        """
        Crea un botón de eliminar para una fila específica.
        """
        widget = QWidget()
        layout = QHBoxLayout()
        eliminar_btn = QPushButton("Eliminar")
        # No permitir eliminar el propio usuario
        eliminar_btn.setEnabled(usuario_id != self.usuario_id)
        eliminar_btn.clicked.connect(lambda: self.eliminar_usuario(usuario_id))
        layout.addWidget(eliminar_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget

    def eliminar_usuario(self, usuario_id):
        """
        Maneja la eliminación de un usuario.
        """
        # Verificar que sea administrador
        if not self.usuario_manager.es_administrador(self.usuario_id):
            QMessageBox.warning(self, "Error", "Solo los administradores pueden eliminar usuarios")
            return
            
        # Verificar que no sea el usuario actual
        if usuario_id == self.usuario_id:
            QMessageBox.warning(self, "Error", "No puede eliminar su propio usuario")
            return
            
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este usuario? Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            if self.usuario_manager.eliminar_usuario(self.usuario_id, usuario_id):
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                self.cargar_usuarios()
            else:
                QMessageBox.warning(self, "Error", "No se puede eliminar el usuario")

    def cargar_usuarios(self):
        # Obtener todos los usuarios
        self.db.cursor.execute('SELECT id, username, nombre FROM usuarios')
        usuarios = self.db.cursor.fetchall()
        
        self.tabla.setRowCount(len(usuarios))
        for i, usuario in enumerate(usuarios):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(usuario[0])))  # ID
            self.tabla.setItem(i, 1, QTableWidgetItem(usuario[1]))  # Username
            self.tabla.setItem(i, 2, QTableWidgetItem(usuario[2]))  # Nombre
            
            # Agregar botón de eliminar
            self.tabla.setCellWidget(i, 3, self.crear_boton_eliminar(i, usuario[0]))

        self.tabla.resizeColumnsToContents()

    def showEvent(self, event):
        super().showEvent(event)
        self.cargar_usuarios()

class ResumenPage(QWidget):
    def __init__(self, usuario_manager):
        super().__init__()
        self.usuario_manager = usuario_manager
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Resumen Semanal")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.resumen_group = QGroupBox()
        resumen_layout = QFormLayout()
        
        self.base_label = QLabel("0 COP")
        self.cobrado_label = QLabel("0 COP")
        self.prestado_label = QLabel("0 COP")
        self.seguros_label = QLabel("0 COP")
        self.gastos_label = QLabel("0 COP")
        self.efectivo_label = QLabel("0 COP")
        self.digital_label = QLabel("0 COP")
        self.balance_label = QLabel("0 COP")
        
        resumen_layout.addRow("Base semanal:", self.base_label)
        resumen_layout.addRow("Total cobrado:", self.cobrado_label)
        resumen_layout.addRow("Total prestado:", self.prestado_label)
        resumen_layout.addRow("Total seguros:", self.seguros_label)
        resumen_layout.addRow("Total gastos:", self.gastos_label)
        resumen_layout.addRow("Pagos en efectivo:", self.efectivo_label)
        resumen_layout.addRow("Pagos digitales:", self.digital_label)
        resumen_layout.addRow("Balance final:", self.balance_label)
        
        self.resumen_group.setLayout(resumen_layout)
        layout.addWidget(self.resumen_group)
        
        layout.addStretch()
        self.setLayout(layout)

    def actualizar_resumen(self):
        if self.usuario_id is None:
            return
            
        resumen = self.usuario_manager.obtener_resumen_semanal(self.usuario_id)
        
        self.base_label.setText(f"{resumen['base']:,.0f} COP")
        self.cobrado_label.setText(f"{resumen['cobrado']:,.0f} COP")
        self.prestado_label.setText(f"{resumen['prestado']:,.0f} COP")
        self.seguros_label.setText(f"{resumen['seguros']:,.0f} COP")
        self.gastos_label.setText(f"{resumen['gastos']:,.0f} COP")
        self.efectivo_label.setText(f"{resumen['efectivo']:,.0f} COP")
        self.digital_label.setText(f"{resumen['digital']:,.0f} COP")
        
        balance = resumen['base'] + resumen['cobrado'] + resumen['seguros'] - resumen['prestado'] - resumen['gastos']
        self.balance_label.setText(f"{balance:,.0f} COP")

class ClientesPage(QWidget):
    def __init__(self, cliente_manager):
        super().__init__()
        self.cliente_manager = cliente_manager
        self.usuario_id = None
        self.todos_clientes = []  # Lista para almacenar todos los clientes
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Lista de Clientes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Filtro de búsqueda
        busqueda_layout = QHBoxLayout()
        busqueda_layout.addWidget(QLabel("Buscar:"))
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Buscar por nombre o cédula...")
        self.busqueda_input.textChanged.connect(self.filtrar_tabla)
        busqueda_layout.addWidget(self.busqueda_input)
        
        # Botón para limpiar búsqueda
        self.limpiar_btn = QPushButton("Limpiar")
        self.limpiar_btn.clicked.connect(self.limpiar_busqueda)
        busqueda_layout.addWidget(self.limpiar_btn)
        
        layout.addLayout(busqueda_layout)

        # Tabla de clientes
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(12)  # Agregamos una columna para acciones
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Cédula", "Teléfono", "Monto prestado", 
            "Fecha préstamo", "Plazo", "Tasa interés", "Seguro",
            "Cuota mínima", "Balance", "Estado", "Acciones"
        ])
        layout.addWidget(self.tabla)
        
        # Ajustar el estilo de la tabla para mejor visualización
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setShowGrid(True)
        self.tabla.setSortingEnabled(True)
        
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.cargar_clientes()

    def crear_boton_eliminar(self, row, cliente_id, balance):
        """
        Crea un botón de eliminar para una fila específica.
        """
        widget = QWidget()
        layout = QHBoxLayout()
        eliminar_btn = QPushButton("Eliminar")
        eliminar_btn.setEnabled(balance <= 0)
        eliminar_btn.clicked.connect(lambda: self.eliminar_cliente(cliente_id))
        layout.addWidget(eliminar_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget

    def eliminar_cliente(self, cliente_id):
        """
        Maneja la eliminación de un cliente.
        """
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este cliente? Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            if self.cliente_manager.eliminar_cliente(cliente_id):
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                self.cargar_clientes()  # Recargar la tabla
            else:
                QMessageBox.warning(self, "Error", "No se puede eliminar el cliente porque aún tiene un balance pendiente")

    def cargar_clientes(self):
        if self.usuario_id is None:
            return
            
        clientes = self.cliente_manager.obtener_clientes(self.usuario_id)
        self.todos_clientes = clientes  # Guardar todos los clientes para filtrado
        self.mostrar_clientes(clientes)
    
    def mostrar_clientes(self, clientes):
        """Muestra los clientes en la tabla."""
        self.tabla.setRowCount(len(clientes))
        
        for i, cliente in enumerate(clientes):
            # Calcular el balance actual del cliente
            balance = self.cliente_manager.calcular_balance(cliente[0])
            
            # Llenar la tabla con los datos del cliente
            self.tabla.setItem(i, 0, QTableWidgetItem(cliente[1]))  # Nombre
            self.tabla.setItem(i, 1, QTableWidgetItem(cliente[2]))  # Cédula
            self.tabla.setItem(i, 2, QTableWidgetItem(cliente[3]))  # Teléfono
            self.tabla.setItem(i, 3, QTableWidgetItem(f"{cliente[4]:,.0f}"))  # Monto prestado
            self.tabla.setItem(i, 4, QTableWidgetItem(str(cliente[5])))  # Fecha
            self.tabla.setItem(i, 5, QTableWidgetItem(cliente[6]))  # Plazo
            self.tabla.setItem(i, 6, QTableWidgetItem(f"{cliente[7]*100:.1f}%"))  # Tasa interés
            self.tabla.setItem(i, 7, QTableWidgetItem(f"{cliente[8]:,.0f}"))  # Seguro
            self.tabla.setItem(i, 8, QTableWidgetItem(f"{cliente[9]:,.0f}"))  # Cuota mínima
            self.tabla.setItem(i, 9, QTableWidgetItem(f"{balance:,.0f}"))  # Balance
            self.tabla.setItem(i, 10, QTableWidgetItem("Activo"))  # Estado
            
            # Agregar botón de eliminar
            self.tabla.setCellWidget(i, 11, self.crear_boton_eliminar(i, cliente[0], balance))

        self.tabla.resizeColumnsToContents()
    
    def filtrar_tabla(self):
        """Filtra la tabla de clientes según el texto de búsqueda."""
        texto_busqueda = self.busqueda_input.text().lower()
        
        if not texto_busqueda:
            # Si no hay texto de búsqueda, mostrar todos
            self.mostrar_clientes(self.todos_clientes)
            return
        
        # Filtrar clientes
        clientes_filtrados = []
        for cliente in self.todos_clientes:
            nombre = cliente[1].lower()
            cedula = cliente[2]
            # Buscar en nombre o cédula
            if texto_busqueda in nombre or texto_busqueda in cedula:
                clientes_filtrados.append(cliente)
        
        self.mostrar_clientes(clientes_filtrados)
    
    def limpiar_busqueda(self):
        """Limpia el campo de búsqueda y muestra todos los clientes."""
        self.busqueda_input.clear()
        self.mostrar_clientes(self.todos_clientes)