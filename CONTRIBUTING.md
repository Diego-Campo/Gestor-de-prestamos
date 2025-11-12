# Guía de Contribución - Gestor de Préstamos

¡Gracias por tu interés en contribuir al proyecto Gestor de Préstamos! Esta guía te ayudará a entender cómo puedes participar en el desarrollo del proyecto.

## Tabla de Contenidos
1. [Código de Conducta](#código-de-conducta)
2. [Cómo Contribuir](#cómo-contribuir)
3. [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
4. [Estándares de Codificación](#estándares-de-codificación)
5. [Proceso de Pull Request](#proceso-de-pull-request)
6. [Reporte de Errores](#reporte-de-errores)
7. [Sugerir Mejoras](#sugerir-mejoras)

## Código de Conducta

### Nuestro Compromiso
Nos comprometemos a hacer de la participación en nuestro proyecto una experiencia libre de acoso para todos, independientemente de la edad, tamaño corporal, discapacidad, etnia, identidad y expresión de género, nivel de experiencia, nacionalidad, apariencia personal, raza, religión o identidad y orientación sexual.

### Estándares
Ejemplos de comportamiento que contribuyen a crear un ambiente positivo:
- Usar un lenguaje acogedor e inclusivo
- Ser respetuoso con los diferentes puntos de vista y experiencias
- Aceptar críticas constructivas con gracia
- Enfocarse en lo que es mejor para la comunidad
- Mostrar empatía hacia otros miembros de la comunidad

## Cómo Contribuir

### Tipos de Contribuciones
Buscamos ayuda en las siguientes áreas:

#### 🐛 Reportar Errores
- Encontrar y reportar bugs
- Proporcionar información detallada para reproducir errores
- Sugerir correcciones

#### 💡 Sugerir Funcionalidades
- Proponer nuevas características
- Mejorar funcionalidades existentes
- Optimizar rendimiento

#### 📝 Documentación
- Mejorar la documentación existente
- Traducir documentación
- Crear tutoriales o ejemplos

#### 🧪 Pruebas
- Escribir nuevas pruebas
- Mejorar la cobertura de pruebas
- Automatizar procesos de testing

#### 🎨 Interfaz de Usuario
- Mejorar diseño visual
- Optimizar experiencia de usuario
- Crear nuevos temas o estilos

## Configuración del Entorno de Desarrollo

### Requisitos Previos
- Python 3.8 o superior
- Git
- Editor de código (recomendado: VS Code)

### Pasos de Configuración

1. **Fork del Repositorio**
   ```bash
   # Hacer fork en GitHub y luego clonar
   git clone https://github.com/TU_USUARIO/Gestor-de-prestamos.git
   cd Gestor-de-prestamos
   ```

2. **Configurar Entorno Virtual**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Instalar Dependencias de Desarrollo**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy  # Herramientas de desarrollo
   ```

4. **Configurar Git**
   ```bash
   git remote add upstream https://github.com/Diego-Campo/Gestor-de-prestamos.git
   git config user.name "Tu Nombre"
   git config user.email "tu.email@ejemplo.com"
   ```

### Estructura del Proyecto para Desarrollo

```
gestor_prestamos/
├── src/                    # Código fuente principal
│   ├── ui/                # Interfaz de usuario
│   ├── models/            # Modelos de datos
│   ├── services/          # Lógica de negocio
│   └── utils/             # Utilidades
├── tests/                 # Pruebas automatizadas
│   ├── unit/             # Pruebas unitarias
│   ├── integration/      # Pruebas de integración
│   └── fixtures/         # Datos de prueba
├── docs/                  # Documentación
├── scripts/               # Scripts de utilidad
└── requirements/          # Archivos de dependencias
    ├── base.txt          # Dependencias base
    ├── dev.txt           # Dependencias de desarrollo
    └── test.txt          # Dependencias de pruebas
```

## Estándares de Codificación

### Estilo de Código Python
Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/) con algunas adaptaciones:

#### Formato
- **Longitud de línea**: máximo 88 caracteres
- **Indentación**: 4 espacios (no tabs)
- **Encoding**: UTF-8

#### Nombrado
```python
# Variables y funciones: snake_case
usuario_nombre = "Juan"
def calcular_interes():
    pass

# Clases: PascalCase
class ClienteManager:
    pass

# Constantes: UPPER_CASE
INTERES_DEFECTO = 0.20
```

#### Documentación
```python
def calcular_cuota(monto: float, interes: float, plazo: int) -> float:
    """
    Calcula la cuota de un préstamo.
    
    Args:
        monto: Monto del préstamo
        interes: Tasa de interés decimal
        plazo: Plazo en días
    
    Returns:
        float: Valor de la cuota calculada
        
    Raises:
        ValueError: Si algún parámetro es inválido
    """
    pass
```

### Herramientas de Calidad de Código

#### Formateo Automático
```bash
# Black para formateo de código
black src/ tests/

# isort para ordenar imports
isort src/ tests/
```

#### Linting
```bash
# flake8 para verificar estilo
flake8 src/ tests/

# mypy para verificación de tipos
mypy src/
```

#### Pruebas
```bash
# pytest para ejecutar pruebas
pytest tests/

# Con cobertura
pytest --cov=src tests/
```

## Proceso de Pull Request

### 1. Preparación
1. Asegúrate de que tu fork esté actualizado
2. Crea una nueva rama para tu feature/fix
3. Nombra la rama descriptivamente

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/corregir-error-calculo
```

### 2. Desarrollo
1. Realiza tus cambios siguiendo los estándares
2. Escribe o actualiza pruebas
3. Actualiza documentación si es necesario
4. Verifica que todas las pruebas pasen

```bash
# Ejecutar todas las verificaciones
black src/ tests/
flake8 src/ tests/
mypy src/
pytest tests/
```

### 3. Commit
Usa mensajes de commit descriptivos:

```bash
git commit -m "feat: agregar cálculo de interés personalizado

- Implementar lógica para intereses variables
- Agregar validación de parámetros
- Incluir pruebas unitarias
- Actualizar documentación"
```

#### Tipos de Commit
- `feat:` nueva funcionalidad
- `fix:` corrección de error
- `docs:` cambios en documentación
- `style:` formateo, sin cambios de lógica
- `refactor:` refactorización de código
- `test:` agregar o corregir pruebas
- `chore:` mantenimiento, dependencias

### 4. Pull Request
1. Push de tu rama al fork
2. Crear Pull Request en GitHub
3. Completar template de PR
4. Esperar revisión

#### Template de Pull Request
```markdown
## Descripción
Descripción breve de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix (cambio que corrige un error)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que afectaría funcionalidad existente)
- [ ] Documentación

## Pruebas
- [ ] Las pruebas existentes pasan
- [ ] Se agregaron nuevas pruebas para los cambios
- [ ] Se probó manualmente la funcionalidad

## Checklist
- [ ] El código sigue las guías de estilo del proyecto
- [ ] Se realizó self-review del código
- [ ] Se comentó el código en áreas de difícil comprensión
- [ ] Se actualizó la documentación correspondiente
```

## Reporte de Errores

### Antes de Reportar
1. Busca en issues existentes
2. Verifica que sea reproducible
3. Prueba con la última versión

### Información a Incluir
```markdown
**Descripción del Error**
Descripción clara y concisa del problema.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Ver error

**Comportamiento Esperado**
Lo que esperabas que sucediera.

**Screenshots**
Si es aplicable, agrega screenshots.

**Información del Sistema:**
 - OS: [ej. Windows 10]
 - Python: [ej. 3.9.0]
 - Versión: [ej. 1.0.0]

**Contexto Adicional**
Cualquier otra información relevante.
```

## Sugerir Mejoras

### Template para Nuevas Funcionalidades
```markdown
**¿Tu solicitud está relacionada con un problema?**
Descripción clara del problema.

**Describe la solución que te gustaría**
Descripción clara de lo que quieres que suceda.

**Describe alternativas que hayas considerado**
Otras soluciones o funcionalidades consideradas.

**Contexto adicional**
Screenshots, mockups, etc.
```

## Reconocimientos

### Contribuidores
Todos los contribuidores serán reconocidos en:
- Archivo AUTHORS.md
- Release notes
- Documentación del proyecto

### Tipos de Reconocimiento
- 🐛 Bug reports
- 💡 Ideas & Suggestions
- 💻 Code contributions
- 📖 Documentation
- 🎨 Design
- ✅ Testing

## Recursos Adicionales

### Documentación
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

### Herramientas Recomendadas
- **Editor**: VS Code con extensiones Python
- **Git Client**: GitHub Desktop o SourceTree
- **Database**: DB Browser for SQLite

---

¡Gracias por contribuir a Gestor de Préstamos! 🎉