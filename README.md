# Agente de Actualización de Host Autodesk (Plug & Play)

Este proyecto reemplaza el antiguo script `.bat` por un agente de Python compilado (`.exe`) que se encarga de actualizar el archivo `hosts` con la IP del servidor de Autodesk de forma totalmente automática y silenciosa.

## Características

- **Auto-Desplegable**: El mismo ejecutable se encarga de su propia instalación la primera vez que se corre.
- **Persistencia Robusta**: Se configura como una Tarea Programada de Windows que se activa **al iniciar el sistema (onstart)**, sin depender de que un usuario inicie sesión.
- **Privilegios Elevados**: Se ejecuta bajo la cuenta `SYSTEM`, lo que le otorga permisos totales para modificar el archivo `hosts` sin mostrar avisos de UAC al usuario.
- **Modo Silencioso**: Funciona en segundo plano sin ventana de consola.

## Instalación (Paso Único)

Diseñado para ser utilizado por personal de IT de nivel 1 o para ser incluido en imágenes clonadas:

1. Copia el archivo **`dist\update_host.exe`** en la PC destino.
2. Ejecútalo **una sola vez** como Administrador.
3. El programa realizará lo siguiente:
   - Se copiará a la ubicación permanente: `C:\ProgramData\AutodeskHostConnector\update_host.exe`.
   - Creará la tarea programada "AutodeskHostConnector".
   - Se ejecutará por primera vez para actualizar el host.

## Funcionamiento Técnico

El agente realiza las siguientes tareas en cada arranque:
1. Resuelve la dirección IP de `autodesk.lasalleflorida.edu.ar`.
2. Realiza una copia de seguridad de `C:\Windows\System32\drivers\etc\hosts` como `hosts.bak`.
3. Busca la etiqueta `AUTODESKSERVER` en el archivo `hosts` y actualiza la línea con la nueva IP. Si no existe, la añade al final.

## Verificación

Para confirmar que el agente está operativo:
- **Archivo Hosts**: Abre `C:\Windows\System32\drivers\etc\hosts` y verifica la línea de `AUTODESKSERVER`.
- **Tarea Programada**: Abre el "Programador de Tareas" de Windows y busca la tarea `AutodeskHostConnector`. Debe estar configurada para ejecutarse "Al iniciar el sistema" con "Privilegios más altos".

---
*Desarrollado para optimizar el despliegue y mantenimiento de los hosts de Autodesk.*
