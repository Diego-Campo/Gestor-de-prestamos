# Changelog - Gestor de Préstamos

Todas las modificaciones notables de este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-11

### Añadido
- Sistema completo de gestión de préstamos y cobros
- Interfaz gráfica moderna con PyQt6
- Sistema multiusuario con roles (Admin/Cobrador)
- Gestión completa de clientes y préstamos
- Registro de pagos (efectivo y digital)
- Control de gastos operativos
- Cálculo automático de cuotas y intereses
- Resumen semanal automatizado
- Panel de supervisión para administradores
- Base de datos SQLite integrada
- Sistema de autenticación seguro con bcrypt
- Script de instalación y ejecución simplificada
- Documentación completa para usuarios y desarrolladores

### Características Principales
- **Gestión de Usuarios**: Creación, edición y eliminación de usuarios
- **Gestión de Clientes**: Registro completo de información y préstamos
- **Cálculo Automático**: Cuotas, intereses y fechas de vencimiento
- **Registro de Pagos**: Seguimiento detallado de todos los pagos
- **Control de Gastos**: Registro y seguimiento de gastos operativos
- **Reportes**: Resúmenes semanales y estadísticas generales
- **Seguridad**: Autenticación robusta y control de acceso por roles
- **Base de Datos**: Almacenamiento persistente con SQLite
- **Interfaz Intuitiva**: Navegación sencilla y diseño moderno

### Configuración por Defecto
- Usuario administrador: `admin/admin123`
- Usuarios de prueba: `cobrador1/pass1`, `cobrador2/pass2`, `cobrador3/pass3`
- Interés por defecto: 20%
- Plazos disponibles: 30 y 40 días
- Cuota mínima: $2,000 por cada $50,000 prestados

### Archivos Incluidos
- `app.py` - Punto de entrada principal
- `ejecutar.bat` - Script de ejecución simplificada
- `requirements.txt` - Dependencias del proyecto
- `README.md` - Documentación principal
- `INSTALL.md` - Guía de instalación
- `MANUAL_USUARIO.md` - Manual completo de usuario
- `LICENSE` - Licencia MIT
- `CHANGELOG.md` - Este archivo de cambios

### Estructura del Proyecto
```
gestor_prestamos/
├── src/                   # Código fuente
│   ├── ui/               # Interfaz de usuario
│   ├── database.py       # Gestión de base de datos
│   ├── usuario.py        # Lógica de usuarios
│   └── cliente.py        # Lógica de clientes
├── tests/                # Pruebas y simulaciones
├── .venv/               # Entorno virtual Python
└── documentación/       # Archivos de documentación
```

### Dependencias
- PyQt6 >= 6.5.0
- bcrypt >= 4.0.0
- python-dotenv >= 1.0.0

### Notas de Desarrollo
- Desarrollado en Python 3.8+
- Base de datos SQLite para portabilidad
- Interfaz gráfica con PyQt6
- Arquitectura modular para fácil mantenimiento
- Código documentado y siguiendo buenas prácticas

### Compatibilidad
- Windows 10/11
- Python 3.8 o superior
- Arquitecturas x86 y x64

## [Próximas Versiones]

### Planificado para v1.1.0
- [ ] Exportación de reportes a Excel/PDF
- [ ] Gráficos y estadísticas avanzadas
- [ ] Notificaciones de vencimientos
- [ ] Respaldo automático de base de datos
- [ ] Modo oscuro para la interfaz

### Consideraciones Futuras
- [ ] API REST para integración externa
- [ ] Aplicación móvil complementaria
- [ ] Integración con servicios de pago digital
- [ ] Reportes personalizables
- [ ] Sistema de notificaciones por email/SMS

---

**Formato del Changelog**
- `Añadido` para nuevas funcionalidades
- `Cambiado` para cambios en funcionalidades existentes
- `Depreciado` para funcionalidades que serán removidas
- `Removido` para funcionalidades removidas
- `Arreglado` para corrección de errores
- `Seguridad` para vulnerabilidades corregidas