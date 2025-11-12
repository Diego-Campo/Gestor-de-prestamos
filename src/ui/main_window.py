"""
Módulo principal de la interfaz gráfica de usuario.

Este módulo contiene las clases principales que manejan la interfaz gráfica:
- LoginWindow: Ventana de inicio de sesión
- RegisterDialog: Diálogo de registro de usuarios
- MainWindow: Ventana principal de la aplicación
- MainApp: Widget principal que contiene todas las páginas
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QLineEdit, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QComboBox,
                             QSpinBox, QDoubleSpinBox, QFormLayout, QGroupBox,
                             QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from .pages import (BasePage, ClientePage, PagoPage, GastoPage, ResumenPage, 
                    ClientesPage, UsuariosPage, SupervisorPage)
import os
import sys

class LoginWindow(QWidget):
    loginSuccessful = pyqtSignal(int)  # Señal para indicar inicio de sesión exitoso

    def __init__(self, usuario_manager):
        super().__init__()
        self.usuario_manager = usuario_manager
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        # Logo o título
        title = QLabel("GESTOR DE PRÉSTAMOS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        # Formulario
        form = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form.addRow("Usuario:", self.username_input)
        form.addRow("Contraseña:", self.password_input)
        
        layout.addLayout(form)

        # Botones
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.clicked.connect(self.login)
        self.register_btn = QPushButton("Registrarse")
        self.register_btn.clicked.connect(self.show_register)
        
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        usuario_id = self.usuario_manager.validar_usuario(username, password)
        if usuario_id:
            self.loginSuccessful.emit(usuario_id)
            self.username_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def show_register(self):
        dialog = RegisterDialog(self.usuario_manager, self)
        dialog.exec()

from PyQt6.QtWidgets import QDialog

class RegisterDialog(QDialog):
    def __init__(self, usuario_manager, parent=None):
        super().__init__(parent)
        self.usuario_manager = usuario_manager
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("Registro de Usuario")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.nombre_input = QLineEdit()
        
        form.addRow("Usuario:", self.username_input)
        form.addRow("Contraseña:", self.password_input)
        form.addRow("Nombre completo:", self.nombre_input)
        
        layout.addLayout(form)

        register_btn = QPushButton("Registrar")
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        nombre = self.nombre_input.text()

        if not all([username, password, nombre]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if self.usuario_manager.crear_usuario(username, password, nombre):
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
            self.accept()  # Cierra el diálogo con éxito
        else:
            QMessageBox.warning(self, "Error", "El nombre de usuario ya existe")

class MainWindow(QMainWindow):
    def __init__(self, db, usuario_manager, cliente_manager):
        super().__init__()
        self.db = db
        self.usuario_manager = usuario_manager
        self.cliente_manager = cliente_manager
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Gestor de Préstamos")
        self.setMinimumSize(800, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)

        # Stack de widgets
        self.stack = QStackedWidget()
        
        # Ventana de login
        self.login_window = LoginWindow(self.usuario_manager)
        self.login_window.loginSuccessful.connect(self.on_login_successful)
        
        # Ventana principal de la aplicación
        self.main_app = MainApp(self.db, self.usuario_manager, self.cliente_manager)
        self.main_app.logoutRequested.connect(self.on_logout_requested)  # Conectar señal de logout
        
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.main_app)
        
        layout.addWidget(self.stack)

    def on_login_successful(self, usuario_id):
        self.usuario_id = usuario_id
        self.main_app.set_usuario(usuario_id)
        self.stack.setCurrentIndex(1)
    
    def on_logout_requested(self):
        """Maneja la solicitud de cerrar sesión."""
        self.usuario_id = None
        self.stack.setCurrentIndex(0)  # Volver a la pantalla de login

class MainApp(QWidget):
    logoutRequested = pyqtSignal()  # Señal para solicitar cierre de sesión
    
    def __init__(self, db, usuario_manager, cliente_manager):
        super().__init__()
        self.db = db
        self.usuario_manager = usuario_manager
        self.cliente_manager = cliente_manager
        self.usuario_id = None
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout()
        
        # Panel izquierdo (menú)
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        
        # Botones para cobradores
        self.btn_base = QPushButton("Registrar Base")
        self.btn_cliente = QPushButton("Nuevo Cliente")
        self.btn_pago = QPushButton("Registrar Pago")
        self.btn_gasto = QPushButton("Registrar Gasto")
        self.btn_resumen = QPushButton("Ver Resumen")
        self.btn_clientes = QPushButton("Ver Clientes")
        
        # Botones administrativos
        self.btn_supervisor = QPushButton("Panel de Supervisión")
        self.btn_usuarios = QPushButton("Gestionar Usuarios")
        
        # Botón de cerrar sesión
        self.btn_logout = QPushButton("Cerrar Sesión")
        
        menu_layout.addWidget(self.btn_base)
        menu_layout.addWidget(self.btn_cliente)
        menu_layout.addWidget(self.btn_pago)
        menu_layout.addWidget(self.btn_gasto)
        menu_layout.addWidget(self.btn_resumen)
        menu_layout.addWidget(self.btn_clientes)
        
        # Separador visual
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        menu_layout.addWidget(separator)
        
        # Botones administrativos (solo visibles para admin)
        menu_layout.addWidget(self.btn_supervisor)
        menu_layout.addWidget(self.btn_usuarios)
        
        menu_layout.addStretch()
        menu_layout.addWidget(self.btn_logout)  # Botón de cerrar sesión al final
        
        menu_widget.setLayout(menu_layout)
        layout.addWidget(menu_widget)

        # Panel derecho (contenido)
        self.content = QStackedWidget()
        
        # Páginas de contenido
        self.base_page = BasePage(self.usuario_manager)
        self.cliente_page = ClientePage(self.cliente_manager)
        self.pago_page = PagoPage(self.cliente_manager)
        self.gasto_page = GastoPage(self.usuario_manager)
        self.resumen_page = ResumenPage(self.usuario_manager)
        self.clientes_page = ClientesPage(self.cliente_manager)
        self.supervisor_page = SupervisorPage(self.usuario_manager, self.cliente_manager)
        self.usuarios_page = UsuariosPage(self.usuario_manager)
        
        self.content.addWidget(self.base_page)
        self.content.addWidget(self.cliente_page)
        self.content.addWidget(self.pago_page)
        self.content.addWidget(self.gasto_page)
        self.content.addWidget(self.resumen_page)
        self.content.addWidget(self.clientes_page)
        self.content.addWidget(self.supervisor_page)
        self.content.addWidget(self.usuarios_page)
        
        layout.addWidget(self.content)
        
        self.setLayout(layout)
        
        # Conexiones
        self.btn_base.clicked.connect(lambda: self.show_page(0))
        self.btn_cliente.clicked.connect(lambda: self.show_page(1))
        self.btn_pago.clicked.connect(lambda: self.show_page(2))
        self.btn_gasto.clicked.connect(lambda: self.show_page(3))
        self.btn_resumen.clicked.connect(lambda: self.show_page(4))
        self.btn_clientes.clicked.connect(lambda: self.show_page(5))
        self.btn_supervisor.clicked.connect(lambda: self.show_page(6))
        self.btn_usuarios.clicked.connect(lambda: self.show_page(7))

    def show_page(self, index):
        self.content.setCurrentIndex(index)
        if index == 4:  # Resumen
            self.resumen_page.actualizar_resumen()
        elif index == 5:  # Clientes
            self.clientes_page.cargar_clientes()

    def set_usuario(self, usuario_id):
        self.usuario_id = usuario_id
        
        # Actualizar ID en todas las páginas
        self.base_page.usuario_id = usuario_id
        self.cliente_page.usuario_id = usuario_id
        self.pago_page.usuario_id = usuario_id
        self.gasto_page.usuario_id = usuario_id
        self.resumen_page.usuario_id = usuario_id
        self.clientes_page.usuario_id = usuario_id
        self.supervisor_page.usuario_id = usuario_id
        self.usuarios_page.usuario_id = usuario_id
        
        # Verificar si es administrador
        es_admin = self.usuario_manager.es_administrador(usuario_id)
        
        # Ocultar todas las opciones primero
        self.btn_base.hide()
        self.btn_cliente.hide()
        self.btn_pago.hide()
        self.btn_gasto.hide()
        self.btn_resumen.hide()
        self.btn_clientes.hide()
        self.btn_supervisor.hide()
        self.btn_usuarios.hide()
        
        # Mostrar solo las opciones correspondientes al rol
        if es_admin:
            self.btn_supervisor.show()
            self.btn_usuarios.show()
            # Mostrar página de supervisor por defecto
            self.show_page(6)  # Índice de la página de supervisor
        else:
            self.btn_base.show()
            self.btn_cliente.show()
            self.btn_pago.show()
            self.btn_gasto.show()
            self.btn_resumen.show()
            self.btn_clientes.show()
            # Mostrar página de base por defecto
            self.show_page(0)  # Índice de la página de base
        
        # Configurar botón de cerrar sesión
        self.btn_logout.clicked.connect(self.cerrar_sesion)
        
    def cerrar_sesion(self):
        """
        Cierra la sesión del usuario actual y vuelve a la pantalla de login.
        """
        respuesta = QMessageBox.question(
            self,
            "Confirmar cierre de sesión",
            "¿Está seguro de que desea cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            self.usuario_id = None
            # Limpiar los IDs de usuario de todas las páginas
            self.base_page.usuario_id = None
            self.cliente_page.usuario_id = None
            self.pago_page.usuario_id = None
            self.gasto_page.usuario_id = None
            self.resumen_page.usuario_id = None
            self.clientes_page.usuario_id = None
            self.supervisor_page.usuario_id = None
            self.usuarios_page.usuario_id = None
            # Emitir señal para volver a login
            self.logoutRequested.emit()