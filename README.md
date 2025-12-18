# 📱 Gestor de Préstamos v2.0.0

[![Versión](https://img.shields.io/badge/versión-2.0.0-blue.svg)](https://github.com/Diego-Campo/Gestor-de-prestamos)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.2.0-green)](https://kivy.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-teal)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)
[![Android](https://img.shields.io/badge/Android-Ready-brightgreen)](https://www.android.com/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

Sistema profesional de gestión y control de préstamos **multi-plataforma** (Android y Windows) con API REST y base de datos PostgreSQL. Diseñado para cobradores y administradores que necesitan control total desde cualquier dispositivo.

---

## ✨ Novedades v2.0.0

🎉 **¡Gran actualización!** El sistema ha sido completamente rediseñado:

- 📱 **Android**: Ahora funciona en teléfonos y tablets
- 🌐 **API REST**: Arquitectura cliente-servidor moderna
- 🐘 **PostgreSQL**: Base de datos profesional escalable
- 🔒 **JWT Auth**: Autenticación segura con tokens
- 🎨 **UI Renovada**: Interfaz adaptada para móvil con Kivy/KivyMD

---

## 🚀 Características

### 💼 Gestión de Negocio
- 💰 **Préstamos**: Control total de montos, intereses y plazos
- 👥 **Clientes**: Registro completo con cédula, teléfono y dirección
- 📊 **Dashboard**: Resumen en tiempo real de cobros diarios
- 💳 **Pagos**: Registro de pagos efectivo y digital
- 📈 **Reportes**: Estadísticas detalladas por cobrador

### 🔐 Seguridad
- 🔑 **JWT Tokens**: Autenticación moderna y segura
- 🔒 **Bcrypt**: Contraseñas hasheadas con salt
- 👤 **Roles**: Sistema de permisos (Admin/Cobrador)
- 🛡️ **API Protegida**: Todos los endpoints autenticados

### 📱 Multi-plataforma
- 🤖 **Android**: APK compilado con Buildozer
- 🪟 **Windows**: Aplicación de escritorio
- 🌐 **API REST**: Backend unificado
- 📶 **Online**: Requiere conexión a internet

---

## 📋 Requisitos

### Para Servidor (Windows/Linux)
- Python 3.9+
- PostgreSQL 15+ (o Docker)
- 4 GB RAM mínimo
- Conexión a internet

### Para Android
- Android 5.0+ (API 21)
- 2 GB RAM mínimo
- 100 MB espacio
- Conexión WiFi/datos

---

## 🔧 Instalación Rápida

### 1️⃣ Clonar Repositorio
```bash
git clone https://github.com/Diego-Campo/Gestor-de-prestamos.git
cd Gestor-de-prestamos
```

### 2️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar PostgreSQL

**Opción A: Con Docker (Recomendado)**
```bash
python setup_database.py
```

**Opción B: PostgreSQL Local**
1. Instalar PostgreSQL 15+
2. Crear base de datos `gestor_prestamos`
3. Ejecutar `src/db/migrations/001_initial.sql`

### 4️⃣ Configurar Variables de Entorno
```bash
# Crear archivo .env
copy .env.example .env

# Editar .env con tus datos:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestor_prestamos
DB_USER=postgres
DB_PASSWORD=tu_password
JWT_SECRET=tu_secret_super_seguro
```

### 5️⃣ Iniciar Servidor API
```bash
python run_api.py
```

Servidor corriendo en: `http://localhost:8000`  
Documentación API: `http://localhost:8000/docs`

### 6️⃣ Iniciar Aplicación
```bash
# En otra terminal
python run_app.py
```

---

## 📱 Compilar para Android

### Requisitos
- Linux (Ubuntu 20.04+ recomendado)
- Buildozer instalado
- Android SDK/NDK (se descargan automáticamente)

### Compilar APK
```bash
# Instalar Buildozer
pip install buildozer

# Compilar APK debug
buildozer android debug

# APK generado en: bin/gestorprestamos-2.0.0-debug.apk
```

### Instalar en Android
```bash
# Via USB
adb install bin/gestorprestamos-2.0.0-debug.apk

# O transferir APK al teléfono manualmente
```

**⚠️ Importante**: Configura `API_URL` en el código para apuntar a tu servidor antes de compilar.

---

## 📖 Uso

### Primer Login
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Funciones Principales

#### 👤 Como Cobrador
1. Ver dashboard con resumen del día
2. Consultar lista de clientes activos
3. Registrar pagos (efectivo/digital)
4. Ver historial de pagos por cliente

#### 👨‍💼 Como Administrador
- Todo lo anterior +
- Crear/eliminar usuarios (cobradores)
- Ver estadísticas de todos los cobradores
- Gestionar configuración del sistema

---

## 📡 API REST

### Endpoints Principales

```http
POST   /api/auth/login          # Login
POST   /api/auth/register       # Registrar usuario
GET    /api/usuarios/me         # Usuario actual
GET    /api/clientes            # Lista de clientes
POST   /api/clientes            # Crear cliente
GET    /api/clientes/{id}       # Detalle de cliente
POST   /api/pagos               # Registrar pago
GET    /api/pagos/resumen/hoy   # Resumen del día
```

### Autenticación
```bash
# Obtener token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Usar token
curl http://localhost:8000/api/clientes \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

Ver documentación completa en: `http://localhost:8000/docs`

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────┐
│     APLICACIONES CLIENTE         │
├──────────────────────────────────┤
│  Android (Kivy) │ Windows (Kivy) │
└────────┬─────────────────────────┘
         │ HTTP/JSON
         ▼
┌──────────────────────────────────┐
│       API REST (FastAPI)         │
├──────────────────────────────────┤
│  • Autenticación JWT             │
│  • Endpoints CRUD                │
│  • Validación con Pydantic       │
└────────┬─────────────────────────┘
         │ psycopg2
         ▼
┌──────────────────────────────────┐
│      PostgreSQL Database         │
├──────────────────────────────────┤
│  • usuarios                      │
│  • clientes                      │
│  • pagos                         │
│  • bases_semanales               │
│  • gastos_semanales              │
└──────────────────────────────────┘
```

---

## 📂 Estructura del Proyecto

```
Gestor-de-prestamos/
├── main.py                 # Entry point aplicación Kivy
├── run_api.py             # Script para iniciar API
├── run_app.py             # Script para iniciar app
├── setup_database.py      # Setup de PostgreSQL
├── buildozer.spec         # Configuración Android
├── requirements.txt       # Dependencias Python
├── .env.example           # Template variables entorno
├── docker-compose.yml     # PostgreSQL con Docker
│
├── src/
│   ├── config.py          # Configuración general
│   ├── usuario.py         # Lógica de usuarios
│   ├── cliente.py         # Lógica de clientes
│   │
│   ├── db/                # Base de datos
│   │   ├── connection.py  # Pool de conexiones
│   │   ├── models.py      # Modelos de datos
│   │   └── migrations/    # Scripts SQL
│   │
│   ├── api/               # API REST
│   │   ├── server.py      # Servidor FastAPI
│   │   ├── middleware/    # JWT auth
│   │   └── routes/        # Endpoints
│   │       ├── auth.py
│   │       ├── usuarios.py
│   │       ├── clientes.py
│   │       └── pagos.py
│   │
│   └── ui_kivy/           # Interfaz Kivy
│       └── screens/       # Pantallas
│           ├── login_screen.py
│           ├── home_screen.py
│           ├── clientes_screen.py
│           └── pagos_screen.py
│
└── docs/                  # Documentación adicional
```

---

## 🛠️ Tecnologías

| Categoría | Tecnología | Versión |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.104+ |
| **Base de Datos** | PostgreSQL | 15+ |
| **Frontend** | Kivy/KivyMD | 2.2.0 / 1.1.1 |
| **Auth** | JWT | python-jose 3.3+ |
| **Password** | Bcrypt | 4.0+ |
| **HTTP Client** | Requests | 2.31+ |
| **ORM/Driver** | psycopg2 | 2.9+ |
| **Android Build** | Buildozer | latest |

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu rama: `git checkout -b feature/NuevaCaracteristica`
3. Commit tus cambios: `git commit -m 'Agregar NuevaCaracteristica'`
4. Push a la rama: `git push origin feature/NuevaCaracteristica`
5. Abre un Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Diego Campo**
- GitHub: [@Diego-Campo](https://github.com/Diego-Campo)
- Email: campoviverodiego@gmail.com

---

## 📞 Soporte

¿Problemas o preguntas?

- 🐛 [Reportar Bug](https://github.com/Diego-Campo/Gestor-de-prestamos/issues)
- 💬 [Discusiones](https://github.com/Diego-Campo/Gestor-de-prestamos/discussions)
- 📧 Email: campoviverodiego@gmail.com

---

## ⭐ Star History

Si este proyecto te ha sido útil, ¡dale una estrella! ⭐

---

**Hecho con ❤️ por Diego Campo**
