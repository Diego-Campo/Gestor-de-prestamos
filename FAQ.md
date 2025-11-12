# Preguntas Frecuentes - Gestor de Préstamos

## Índice
1. [Instalación y Configuración](#instalación-y-configuración)
2. [Uso General](#uso-general)
3. [Gestión de Usuarios](#gestión-de-usuarios)
4. [Gestión de Clientes](#gestión-de-clientes)
5. [Pagos y Cálculos](#pagos-y-cálculos)
6. [Reportes y Resúmenes](#reportes-y-resúmenes)
7. [Solución de Problemas](#solución-de-problemas)
8. [Seguridad](#seguridad)

## Instalación y Configuración

### ❓ ¿Qué necesito para instalar la aplicación?
**Respuesta:** Necesitas:
- Windows 10 o superior
- Python 3.8 o superior (se instala automáticamente si usas el instalador)
- Al menos 100 MB de espacio libre en disco
- Permisos de administrador para la instalación inicial

### ❓ ¿Cómo instalo la aplicación?
**Respuesta:** Tienes dos opciones:
1. **Fácil**: Descargar el archivo ejecutable y hacer doble clic en `ejecutar.bat`
2. **Manual**: Seguir la guía en `INSTALL.md` para instalación con Python

### ❓ ¿La aplicación funciona sin internet?
**Respuesta:** Sí, la aplicación funciona completamente offline. No requiere conexión a internet.

### ❓ ¿Dónde se guardan mis datos?
**Respuesta:** Los datos se guardan en un archivo llamado `gestor_prestamos.db` en la misma carpeta de la aplicación.

## Uso General

### ❓ ¿Cuáles son las credenciales por defecto?
**Respuesta:** 
- **Administrador**: usuario `admin`, contraseña `admin123`
- **Cobradores de prueba**: `cobrador1/pass1`, `cobrador2/pass2`, `cobrador3/pass3`

⚠️ **Importante**: Cambia estas contraseñas en el primer uso.

### ❓ ¿Puedo usar la aplicación en varios computadores?
**Respuesta:** Sí, pero debes copiar el archivo `gestor_prestamos.db` entre los computadores para mantener la sincronización de datos.

### ❓ ¿Cómo hago respaldo de mis datos?
**Respuesta:** Copia el archivo `gestor_prestamos.db` a una ubicación segura (USB, nube, etc.). Este archivo contiene toda tu información.

### ❓ ¿La aplicación se actualiza automáticamente?
**Respuesta:** No, las actualizaciones son manuales. Cuando haya una nueva versión, debes descargarla y reemplazar los archivos, manteniendo tu base de datos.

## Gestión de Usuarios

### ❓ ¿Cuántos usuarios puedo crear?
**Respuesta:** No hay límite específico de usuarios, pero se recomienda crear solo los necesarios para mantener la seguridad.

### ❓ ¿Puedo eliminar el usuario administrador?
**Respuesta:** No, debe existir al menos un usuario administrador. Si quieres cambiar quién es el admin, crea otro usuario admin primero.

### ❓ ¿Qué pasa si olvido mi contraseña?
**Respuesta:** Solo un administrador puede cambiar contraseñas. Si olvidas la contraseña de admin, necesitarás ayuda técnica.

### ❓ ¿Puedo cambiar el nombre de usuario después de crearlo?
**Respuesta:** No, el nombre de usuario no se puede cambiar. Si necesitas cambiarlo, debes crear un nuevo usuario.

## Gestión de Clientes

### ❓ ¿Cuál es el monto mínimo para un préstamo?
**Respuesta:** No hay monto mínimo establecido, pero el sistema está optimizado para préstamos desde $50,000.

### ❓ ¿Puedo modificar el interés después de crear el préstamo?
**Respuesta:** No, el interés no se puede modificar una vez creado el préstamo. Esto es para mantener la integridad de los cálculos.

### ❓ ¿Qué plazos están disponibles?
**Respuesta:** Los plazos disponibles son 30 y 40 días. Estos se configuran en el sistema por defecto.

### ❓ ¿Puedo eliminar un cliente?
**Respuesta:** Solo puedes eliminar clientes que no tengan pagos registrados. Si ya tiene pagos, no se puede eliminar para mantener el historial.

### ❓ ¿Cómo se calcula la cuota mínima?
**Respuesta:** $2,000 por cada $50,000 prestados. Ejemplo: para $100,000 la cuota mínima es $4,000.

### ❓ ¿Qué es el seguro y cómo se calcula?
**Respuesta:** El seguro es igual al valor de una cuota mínima y se cobra una sola vez al momento del préstamo.

## Pagos y Cálculos

### ❓ ¿Cuál es la diferencia entre pago efectivo y digital?
**Respuesta:** 
- **Efectivo**: Dinero físico que debes entregar a la empresa
- **Digital**: Transferencias, Nequi, Daviplata, etc. que van directo a la empresa

### ❓ ¿Puedo registrar pagos parciales?
**Respuesta:** Sí, puedes registrar cualquier monto de pago. El sistema actualizará automáticamente el saldo pendiente.

### ❓ ¿Cómo funciona el cálculo de intereses?
**Respuesta:** El interés es fijo sobre el monto total del préstamo (por defecto 20%). Se calcula una sola vez, no es compuesto.

### ❓ ¿Qué pasa si un cliente paga más de lo que debe?
**Respuesta:** El sistema mostrará saldo negativo, indicando que el cliente tiene crédito a favor.

### ❓ ¿Puedo eliminar un pago registrado por error?
**Respuesta:** Actualmente no hay función para eliminar pagos. Contacta al administrador del sistema para ayuda.

## Reportes y Resúmenes

### ❓ ¿Qué es la base semanal y por qué es importante?
**Respuesta:** Es el dinero con el que inicias la semana. Es crucial para calcular correctamente tus ganancias reales.

### ❓ ¿Cuándo debo registrar la entrega de dinero?
**Respuesta:** Cada vez que entregues dinero efectivo cobrado a la empresa. Esto actualiza tu resumen semanal.

### ❓ ¿Puedo ver resúmenes de semanas anteriores?
**Respuesta:** Actualmente solo puedes ver el resumen de la semana actual. Los históricos se mantienen en la base de datos para referencia futura.

### ❓ ¿Cómo se calculan las ganancias?
**Respuesta:** Ganancias = Total Cobrado - Gastos - Dinero Entregado + Base Inicial

## Solución de Problemas

### ❓ La aplicación no inicia, ¿qué hago?
**Respuesta:** 
1. Verifica que Python esté instalado
2. Asegúrate de que el archivo `gestor_prestamos.db` tenga permisos de escritura
3. Ejecuta desde terminal para ver mensajes de error
4. Reinstala las dependencias con: `.\.venv\Scripts\pip.exe install -r requirements.txt`

### ❓ Error: "No se puede ejecutar scripts" en Windows
**Respuesta:** 
1. Abre PowerShell como administrador
2. Ejecuta: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
3. Presiona 'Y' para confirmar

### ❓ Error: "No module named 'PyQt6'"
**Respuesta:** Las dependencias no están instaladas. Ejecuta:
```bash
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### ❓ La aplicación se congela o va muy lenta
**Respuesta:** 
1. Cierra otros programas que consuman memoria
2. Reinicia la aplicación
3. Si persiste, puede ser que la base de datos sea muy grande - contacta soporte técnico

### ❓ Perdí mi base de datos, ¿puedo recuperarla?
**Respuesta:** Solo si tienes un respaldo. Por eso es importante hacer copias regulares del archivo `gestor_prestamos.db`.

### ❓ Error: "Database is locked"
**Respuesta:** 
1. Cierra completamente la aplicación
2. Verifica que no haya otras instancias corriendo
3. Reinicia y vuelve a intentar

## Seguridad

### ❓ ¿Qué tan seguras están mis contraseñas?
**Respuesta:** Las contraseñas se encriptan con bcrypt, un método muy seguro. Nunca se almacenan en texto plano.

### ❓ ¿Puedo usar la aplicación en una red compartida?
**Respuesta:** No se recomienda. La aplicación está diseñada para uso individual. Múltiples usuarios simultáneos pueden causar conflictos.

### ❓ ¿Alguien puede ver mis datos si accede a mi computador?
**Respuesta:** Si alguien tiene acceso físico a tu computador y conoce tu usuario/contraseña del sistema, puede ver los datos. Mantén tu computador seguro.

### ❓ ¿Debo cerrar sesión al terminar?
**Respuesta:** Sí, siempre cierra la aplicación cuando termines, especialmente en computadores compartidos.

### ❓ ¿Puedo cambiar las configuraciones de seguridad?
**Respuesta:** Las configuraciones básicas de seguridad están en el código. Para cambios avanzados, necesitas conocimientos técnicos.

## Funcionalidades Específicas

### ❓ ¿Puedo imprimir reportes?
**Respuesta:** Actualmente no hay función de impresión integrada. Puedes usar la función de screenshot o copiar la información manualmente.

### ❓ ¿La aplicación funciona en Mac o Linux?
**Respuesta:** Está desarrollada principalmente para Windows, pero técnicamente puede funcionar en Mac/Linux con Python instalado.

### ❓ ¿Puedo exportar datos a Excel?
**Respuesta:** Esta función no está disponible en la versión actual, pero está planificada para versiones futuras.

### ❓ ¿Hay límite de clientes por cobrador?
**Respuesta:** No hay límite técnico, pero por rendimiento se recomienda no exceder 1000 clientes por cobrador.

### ❓ ¿Puedo personalizar los plazos de préstamo?
**Respuesta:** Los plazos están fijos en 30 y 40 días. Para cambios, necesitas modificar la configuración del sistema.

## Soporte y Ayuda

### ❓ ¿Dónde puedo obtener ayuda adicional?
**Respuesta:** 
1. Consulta el `MANUAL_USUARIO.md` para instrucciones detalladas
2. Revisa el `DEVELOPER_GUIDE.md` para información técnica
3. Contacta al administrador del sistema de tu organización

### ❓ ¿Hay actualizaciones planeadas?
**Respuesta:** Sí, revisa el `CHANGELOG.md` para ver las funcionalidades planeadas para próximas versiones.

### ❓ ¿Puedo sugerir mejoras?
**Respuesta:** Sí, las sugerencias son bienvenidas. Consulta `CONTRIBUTING.md` para el proceso de contribución.

### ❓ ¿La aplicación es gratuita?
**Respuesta:** Sí, la aplicación se distribuye bajo licencia MIT (ver archivo `LICENSE`).

---

**¿No encontraste tu pregunta?** Consulta la documentación completa o contacta al soporte técnico de tu organización.