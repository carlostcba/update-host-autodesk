# Ejecución de Script BAT al Iniciar Windows 10 con Privilegios de Administrador

Este documento describe cómo configurar un script BAT para que se ejecute con privilegios de administrador al iniciar Windows 10 utilizando el Programador de Tareas de Windows. El script realiza las siguientes acciones:

1. Realiza un ping a `autodesk.lasalleflorida.edu.ar` y guarda la salida en un archivo temporal.
2. Extrae la dirección IP de la salida del ping.
3. Verifica que se haya obtenido una dirección IP.
4. Muestra la dirección IP obtenida.
5. Realiza una copia de seguridad del archivo `hosts`.
6. Reemplaza una IP específica en el archivo `hosts`.
7. Limpia los archivos temporales generados durante la ejecución.

# Instrucciones para Ejecutar un Script BAT como Administrador al Iniciar Windows 10

Para que tu script BAT se ejecute como administrador al iniciar Windows 10, puedes seguir estos pasos:

## Crear una Tarea Programada en el Programador de Tareas de Windows

Esta es la manera más confiable de asegurarse de que el script se ejecute con privilegios de administrador al iniciar el sistema.

### Pasos Detallados

1. **Guardar tu script BAT en una ubicación segura**:
   - Por ejemplo, `C:\Scripts\u_h_autodesk.bat`.

2. **Crear una Tarea Programada**:
   - Abre el Programador de Tareas. Puedes buscar "Programador de Tareas" en el menú Inicio.
   - En el panel derecho, selecciona "Crear tarea".

3. **Configuración General**:
   - En la pestaña "General", asigna un nombre a la tarea, por ejemplo, "Ejecutar Script al Inicio".
   - Marca la casilla "Ejecutar con los privilegios más altos".

4. **Configuración de Disparadores**:
   - Ve a la pestaña "Desencadenadores" y haz clic en "Nuevo".
   - En el menú "Iniciar la tarea", selecciona "Al iniciar sesión" o "Al iniciar" dependiendo de cuándo quieres que se ejecute.
   - Configura cualquier otro detalle necesario y haz clic en "Aceptar".

5. **Configuración de Acciones**:
   - Ve a la pestaña "Acciones" y haz clic en "Nuevo".
   - En "Acción", selecciona "Iniciar un programa".
   - En "Programa o script", navega hasta la ubicación de tu script BAT, por ejemplo, `C:\Scripts\u_h_autodesk.bat`.
   - Haz clic en "Aceptar".

6. **Configuración de Condiciones y Configuración**:
   - Ve a las pestañas "Condiciones" y "Configuración" y ajusta cualquier otra opción según tus necesidades. Por ejemplo, puedes desmarcar "Iniciar la tarea solo si el equipo está en corriente alterna" si deseas que se ejecute siempre.

7. **Guardar la tarea**:
   - Haz clic en "Aceptar" para crear la tarea.

### Ejemplo de cómo se vería

- **General**:
  - Nombre: `Ejecutar Script al Inicio`
  - Usuario: `SYSTEM` (o tu usuario específico)
  - `Ejecutar con los privilegios más altos` marcado.

- **Desencadenadores**:
  - `Al iniciar` o `Al iniciar sesión`

- **Acciones**:
  - `Iniciar un programa`
  - Programa/script: `C:\Scripts\u_h_autodesk.bat`

### Comprobación

Para asegurarte de que funciona correctamente:
- Reinicia tu computadora.
- Verifica que tu script BAT se ha ejecutado correctamente y que ha realizado las acciones esperadas (por ejemplo, modificó el archivo `hosts`).

Este método utiliza el Programador de Tareas para asegurar que el script se ejecute con privilegios de administrador sin necesidad de intervención manual cada vez que inicias el sistema.

