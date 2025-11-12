# Guía para Subir el Proyecto a GitHub

Esta guía te ayudará a subir tu proyecto **Gestor de Préstamos** a GitHub.

## Pasos para Subir a GitHub

### 1. Crear el Repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** en la esquina superior derecha
3. Selecciona **"New repository"**
4. Configura el repositorio:
   - **Repository name**: `Gestor-de-prestamos`
   - **Description**: `Sistema de Gestión y Control de Préstamos`
   - **Visibility**: Público o Privado (tu elección)
   - **NO** marques "Initialize this repository with a README" (ya tienes uno)
5. Haz clic en **"Create repository"**

### 2. Inicializar Git en tu Proyecto

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: Gestor de Préstamos v1.0.0"

# Renombrar la rama principal a 'main'
git branch -M main

# Agregar el repositorio remoto
git remote add origin https://github.com/Diego-Campo/Gestor-de-prestamos.git

# Subir los archivos
git push -u origin main
```

### 3. Verificar que Todo Está en Orden

Después de subir, verifica en GitHub que:
- ✅ Todos los archivos están presentes
- ✅ El README.md se muestra correctamente
- ✅ Los badges funcionan
- ✅ La documentación está accesible

### 4. Configurar Temas Adicionales (Opcional)

#### Agregar Temas al Repositorio
En GitHub, ve a **Settings** > **About** y agrega estos temas:
- `python`
- `pyqt6`
- `sqlite`
- `loan-management`
- `debt-collection`
- `financial-management`
- `windows-application`

#### Crear Releases
1. Ve a **Releases** > **Create a new release**
2. Tag: `v1.0.0`
3. Title: `Gestor de Préstamos v1.0.0`
4. Descripción: Copia del CHANGELOG.md
5. Adjunta archivos si tienes un ejecutable

## Comandos Git Útiles para el Futuro

### Actualizar Cambios
```powershell
git add .
git commit -m "Descripción del cambio"
git push
```

### Ver Estado
```powershell
git status
```

### Ver Historial
```powershell
git log --oneline
```

### Crear una Nueva Rama
```powershell
git checkout -b nombre-de-la-rama
```

### Sincronizar con el Repositorio
```powershell
git pull
```

## Archivos que NO se Subirán (están en .gitignore)

- `.venv/` - Entorno virtual
- `*.db` - Bases de datos
- `*.log` - Archivos de log
- `__pycache__/` - Archivos de caché de Python
- Otros archivos temporales

## Problemas Comunes

### Error: "Repository already exists"
Si el repositorio ya existe, usa:
```powershell
git remote set-url origin https://github.com/Diego-Campo/Gestor-de-prestamos.git
```

### Error de Autenticación
GitHub ya no permite autenticación con contraseña. Necesitas:
1. Generar un **Personal Access Token** en GitHub
2. Usarlo como contraseña cuando Git te lo pida

Para generar el token:
1. GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate new token
3. Selecciona los permisos necesarios (repo)
4. Copia y guarda el token (solo se muestra una vez)

## Siguiente Paso: Promocionar tu Proyecto

Después de subir, considera:
- ✅ Agregar capturas de pantalla
- ✅ Crear un video demo
- ✅ Escribir un blog post sobre el proyecto
- ✅ Compartir en redes sociales

---

**¿Necesitas ayuda?** Consulta la [documentación oficial de GitHub](https://docs.github.com/es)
