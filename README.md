# Agente de Actualización de Host Autodesk

Este proyecto reemplaza el antiguo script `.bat` por un agente de Python compilado (`.exe`) que se encarga de actualizar el archivo `hosts` con la IP del servidor de Autodesk de forma totalmente automática y silenciosa.

## Características

- **Auto-Desplegable**: El mismo ejecutable se encarga de su propia instalación la primera vez que se corre.
- **Resiliencia de Red**: Si falla la resolución del host al inicio (ej. la red no está lista), el agente reintentará automáticamente **hasta 10 veces cada 10 segundos** antes de desistir.
- **Registro Detallado (Logs)**: Todas las acciones se registran en un archivo de log para facilitar el diagnóstico.
- **Persistencia Robusta**: Se configura como una Tarea Programada de Windows que se activa **al iniciar el sistema (onstart)**, sin depender de que un usuario inicie sesión.
- **Privilegios Elevados**: Se ejecuta bajo la cuenta `SYSTEM`, lo que le otorga permisos totales para modificar el archivo `hosts`.

## Instalación (Paso Único)

1. Copia el archivo **`dist\update_host.exe`** en la PC destino.
2. Ejecútalo como Administrador.
3. El programa realizará lo siguiente:
   - Se copiará a la ubicación permanente: `C:\ProgramData\AutodeskHostConnector\update_host.exe`.
   - Creará/Verificará la tarea programada "AutodeskHostConnector".
   - Generará el primer registro en el log y actualizará el archivo hosts.

## Funcionamiento Técnico

El agente realiza las siguientes tareas en cada arranque:
1. Intenta resolver la IP de `autodesk.lasalleflorida.edu.ar` (con hasta 10 reintentos).
2. Realiza una copia de seguridad de `C:\Windows\System32\drivers\etc\hosts` como `hosts.bak`.
3. Busca la etiqueta `AUTODESKSERVER` y actualiza la línea. Si no existe, la añade.
4. Registra el éxito o error de cada paso en el archivo de log.

## Diagnóstico y Verificación

- **Log de Ejecución**: Consulta `C:\ProgramData\AutodeskHostConnector\update_host.log` para ver el historial de actualizaciones.
- **Archivo Hosts**: Verifica la línea `AUTODESKSERVER` en `C:\Windows\System32\drivers\etc\hosts`.
- **Tarea Programada**: Busca `AutodeskHostConnector` en el Programador de Tareas.

## Generación del Ejecutable

Para generar el archivo `.exe` a partir del script de Python, sigue estos pasos (requiere Python instalado):

1. Instala las dependencias necesarias:
   ```powershell
   pip install -r requirements.txt
   ```

2. Ejecuta el comando de compilación:
   ```powershell
   pyinstaller --noconfirm --onefile --windowed --uac-admin --name "update_host" "update_host.py"
   ```

Los parámetros utilizados son:
- `--onefile`: Empaqueta todo en un único archivo ejecutable.
- `--windowed`: Evita que se abra una ventana de consola al ejecutarlo.
- `--uac-admin`: Solicita privilegios de administrador al iniciarse manualmente.
- `--name "update_host"`: Define el nombre del archivo de salida.

---
*Desarrollado para optimizar el despliegue y mantenimiento de los hosts de Autodesk en entornos gestionados.*
