# Manual de Usuario - Gestor de Préstamos

## Índice
1. [Acceso al Sistema](#acceso-al-sistema)
2. [Roles de Usuario](#roles-de-usuario)
3. [Funciones del Cobrador](#funciones-del-cobrador)
4. [Funciones del Administrador](#funciones-del-administrador)
5. [Gestión de Clientes](#gestión-de-clientes)
6. [Registro de Pagos](#registro-de-pagos)
7. [Control de Gastos](#control-de-gastos)
8. [Reportes y Resúmenes](#reportes-y-resúmenes)

## Acceso al Sistema

### Inicio de Sesión
1. Ejecutar la aplicación haciendo doble clic en `ejecutar.bat`
2. Introducir usuario y contraseña
3. Hacer clic en "Iniciar Sesión"

### Credenciales por Defecto
- **Administrador**: usuario `admin`, contraseña `admin123`
- **Cobradores de prueba**: `cobrador1/pass1`, `cobrador2/pass2`, `cobrador3/pass3`

> **⚠️ IMPORTANTE**: Cambiar las contraseñas por defecto en el primer uso.

## Roles de Usuario

### Cobrador
- Gestiona sus propios clientes
- Registra pagos y gastos
- Ve sus resúmenes semanales
- Configura su base semanal

### Administrador
- Supervisa todos los cobradores
- Gestiona usuarios del sistema
- Ve estadísticas globales
- Accede a todos los reportes

## Funciones del Cobrador

### 1. Configuración Inicial - Base Semanal
Al iniciar sesión por primera vez o comenzar una nueva semana:

1. Ir a **"Base Semanal"**
2. Ingresar el monto inicial con el que comenzará la semana
3. Hacer clic en **"Establecer Base"**

> La base semanal es fundamental para calcular correctamente las ganancias.

### 2. Gestión de Clientes

#### Agregar Nuevo Cliente
1. Ir a **"Gestión de Clientes"**
2. Hacer clic en **"Agregar Cliente"**
3. Completar la información:
   - **Nombre completo**
   - **Teléfono** (opcional)
   - **Dirección** (opcional)
   - **Monto del préstamo**
   - **Plazo** (30 o 40 días)
   - **Interés** (por defecto 20%, editable para montos > $500,000)

#### Información Automática
El sistema calcula automáticamente:
- **Cuota mínima**: $2,000 por cada $50,000 prestados
- **Seguro**: Equivalente a una cuota mínima
- **Monto total a pagar**: Préstamo + interés
- **Fecha de vencimiento**

#### Modificar Cliente
1. Seleccionar el cliente en la lista
2. Hacer clic en **"Editar"**
3. Modificar los datos necesarios
4. Guardar cambios

#### Eliminar Cliente
1. Seleccionar el cliente
2. Hacer clic en **"Eliminar"**
3. Confirmar la eliminación

> **Nota**: Solo se pueden eliminar clientes que no tengan pagos registrados.

### 3. Registro de Pagos

#### Registrar un Pago
1. Ir a **"Registro de Pagos"**
2. Seleccionar el cliente
3. Ingresar el **monto** del pago
4. Seleccionar el **tipo de pago**:
   - **Efectivo**: Dinero en físico
   - **Digital**: Transferencia, Nequi, Daviplata, etc.
5. Hacer clic en **"Registrar Pago"**

#### Información del Pago
El sistema muestra automáticamente:
- **Saldo anterior** del cliente
- **Nuevo saldo** después del pago
- **Estado del préstamo** (Al día, Pagado, Atrasado)
- **Historial de pagos**

### 4. Control de Gastos

#### Registrar un Gasto
1. Ir a **"Gastos"**
2. Ingresar la **descripción** del gasto
3. Ingresar el **monto**
4. Hacer clic en **"Registrar Gasto"**

#### Ejemplos de Gastos
- Gasolina para transporte
- Comidas durante el recorrido
- Llamadas telefónicas
- Fotocopias de documentos

### 5. Resumen Semanal

#### Ver Resumen
1. Ir a **"Resumen Semanal"**
2. El sistema muestra automáticamente:
   - **Base inicial** de la semana
   - **Total cobrado** (efectivo + digital)
   - **Total gastos**
   - **Total entregado** (dinero entregado a la empresa)
   - **Ganancia neta** (cobrado - gastos - entregado)

#### Entregar Dinero a la Empresa
1. En el resumen semanal
2. Ingresar el **monto a entregar**
3. Hacer clic en **"Registrar Entrega"**

### 6. Lista de Clientes

#### Consultar Estado de Clientes
1. Ir a **"Lista de Clientes"**
2. Ver información completa de cada cliente:
   - Datos personales
   - Información del préstamo
   - Estado actual
   - Saldo pendiente
   - Próximo pago

#### Filtros Disponibles
- **Todos los clientes**
- **Clientes al día**
- **Clientes atrasados**
- **Préstamos pagados**

## Funciones del Administrador

### 1. Panel de Supervisión

#### Monitorear Cobradores
1. Ir a **"Panel de Supervisión"**
2. Ver estadísticas de todos los cobradores:
   - Total cobrado en la semana
   - Número de clientes activos
   - Total gastado
   - Ganancia neta

### 2. Gestión de Usuarios

#### Crear Nuevo Usuario
1. Ir a **"Gestión de Usuarios"**
2. Hacer clic en **"Agregar Usuario"**
3. Completar información:
   - **Nombre de usuario** (único)
   - **Nombre completo**
   - **Contraseña**
   - **Rol** (Cobrador o Admin)

#### Modificar Usuario
1. Seleccionar usuario de la lista
2. Hacer clic en **"Editar"**
3. Modificar datos necesarios
4. Guardar cambios

#### Eliminar Usuario
1. Seleccionar usuario
2. Hacer clic en **"Eliminar"**
3. Confirmar eliminación

> **⚠️ ATENCIÓN**: Eliminar un usuario también eliminará todos sus clientes y registros asociados.

### 3. Cambio de Contraseña

#### Para Todos los Usuarios
1. Ir a **"Cambiar Contraseña"** (en el menú de usuario)
2. Ingresar **contraseña actual**
3. Ingresar **nueva contraseña**
4. **Confirmar** nueva contraseña
5. Hacer clic en **"Cambiar Contraseña"**

## Consejos y Mejores Prácticas

### Para Cobradores
1. **Establece tu base semanal** siempre al comenzar la semana
2. **Registra los pagos inmediatamente** para mantener información actualizada
3. **Documenta todos los gastos** para un control preciso
4. **Revisa el resumen semanal** antes de entregar dinero
5. **Mantén actualizada la información de contacto** de los clientes

### Para Administradores
1. **Cambia las contraseñas por defecto** inmediatamente
2. **Crea usuarios específicos** para cada cobrador
3. **Revisa regularmente** el panel de supervisión
4. **Realiza copias de seguridad** de la base de datos
5. **Capacita a los usuarios** en el uso del sistema

### Seguridad
1. **No compartas** credenciales de acceso
2. **Cierra la sesión** cuando termines de usar el sistema
3. **Reporta** cualquier problema o error inmediatamente
4. **Mantén actualizados** los datos de contacto

## Soporte Técnico

### Problemas Comunes
- **Error al iniciar**: Verificar instalación de Python y dependencias
- **Error de base de datos**: Verificar permisos de escritura en la carpeta
- **Problema de contraseña**: Contactar al administrador para restablecimiento

### Respaldo de Información
- El archivo `gestor_prestamos.db` contiene toda la información
- Realizar copias de seguridad periódicas
- Guardar en ubicación segura

---

**Versión del Manual**: 1.0  
**Fecha**: Noviembre 2024  
**Sistema**: Gestor de Préstamos v1.0