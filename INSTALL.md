# Gestor de Préstamos - Instalación y Configuración

## Instalación Rápida

### 1. Descargar Python (si no está instalado)
- Ir a https://www.python.org/downloads/
- Descargar Python 3.8 o superior
- Durante la instalación, marcar "Add Python to PATH"

### 2. Configuración del Proyecto
1. Descomprimir el archivo del proyecto
2. Abrir una terminal/PowerShell en la carpeta del proyecto
3. Ejecutar los siguientes comandos:

```bash
# Crear entorno virtual
python -m venv .venv

# Instalar dependencias
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### 3. Ejecución
- **Método más fácil**: Hacer doble clic en `ejecutar.bat`
- **Alternativo**: Abrir terminal y ejecutar `.\.venv\Scripts\python.exe app.py`

## Solución de Problemas Comunes

### Error: "No se puede ejecutar scripts"
Si aparece un error sobre políticas de ejecución:
1. Abrir PowerShell como administrador
2. Ejecutar: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
3. Presionar 'Y' para confirmar

### Error: "Python no se reconoce"
- Verificar que Python esté instalado y agregado al PATH
- Reiniciar la terminal después de instalar Python

### Error: "No module named 'PyQt6'"
- Ejecutar: `.\.venv\Scripts\pip.exe install -r requirements.txt`

### La aplicación no inicia
1. Verificar que todas las dependencias estén instaladas
2. Ejecutar desde terminal para ver mensajes de error
3. Asegurar que la base de datos tenga permisos de escritura

## Configuración Inicial

1. **Primera ejecución**: La aplicación creará automáticamente:
   - Base de datos SQLite (`gestor_prestamos.db`)
   - Usuario administrador por defecto

2. **Credenciales iniciales**:
   - Usuario: `admin`
   - Contraseña: `admin123`

3. **Recomendaciones de seguridad**:
   - Cambiar la contraseña del administrador inmediatamente
   - Crear usuarios específicos para cada cobrador
   - Realizar copias de seguridad periódicas de la base de datos

## Estructura de Archivos

```
gestor_prestamos/
├── .venv/                 # Entorno virtual (creado automáticamente)
├── src/                   # Código fuente de la aplicación
├── tests/                 # Pruebas y simulaciones
├── app.py                 # Archivo principal
├── ejecutar.bat           # Script de ejecución fácil
├── requirements.txt       # Lista de dependencias
├── README.md             # Documentación principal
├── INSTALL.md            # Este archivo
└── gestor_prestamos.db  # Base de datos (creada al ejecutar)
```

## Actualización

Para actualizar a una nueva versión:
1. Respaldar el archivo `gestor_prestamos.db`
2. Reemplazar todos los archivos excepto la base de datos
3. Ejecutar: `.\.venv\Scripts\pip.exe install -r requirements.txt --upgrade`
4. Ejecutar la aplicación normalmente