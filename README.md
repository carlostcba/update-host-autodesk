# Ejecución de Script BAT al Iniciar Windows 10 con Privilegios de Administrador

Este documento describe cómo configurar un script BAT para que se ejecute con privilegios de administrador al iniciar Windows 10 utilizando el Programador de Tareas de Windows. El script realiza las siguientes acciones:

1. Realiza un ping a `autodesk.lasalleflorida.edu.ar` y guarda la salida en un archivo temporal.
2. Extrae la dirección IP de la salida del ping.
3. Verifica que se haya obtenido una dirección IP.
4. Muestra la dirección IP obtenida.
5. Realiza una copia de seguridad del archivo `hosts`.
6. Reemplaza una IP específica en el archivo `hosts`.
7. Limpia los archivos temporales generados durante la ejecución.

## Contenido del Script

```batch
@echo off
setlocal enabledelayedexpansion

REM Realiza el ping y guarda la salida en un archivo temporal
ping -n 1 -4 autodesk.lasalleflorida.edu.ar > ping_result.txt

REM Extrae la dirección IP de la salida del ping
set "ip_address="
for /f "tokens=2 delims=[]" %%A in ('findstr /i "Haciendo ping" ping_result.txt') do (
    set "ip_address=%%A"
)

REM Verifica que se haya obtenido una dirección IP
if not defined ip_address (
    echo No se pudo obtener la direccion IP.
    goto end
)

REM Muestra la IP obtenida
echo Direccion IP obtenida: %ip_address%

REM Ruta al archivo hosts
set "hosts_file=%SystemRoot%\System32\drivers\etc\hosts"

REM Realiza una copia de seguridad del archivo hosts
copy %hosts_file% %hosts_file%.bak

REM Reemplaza la IP en el archivo hosts
set "temp_file=%temp%\hosts_temp"
(for /f "tokens=1,2* delims= " %%A in (%hosts_file%) do (
    if /i "%%B"=="AUTODESKSERVER" (
        echo %ip_address% %%B %%C
    ) else (
        echo %%A %%B %%C
    )
)) > %temp_file%

REM Sobrescribe el archivo hosts con el archivo temporal
copy /y %temp_file% %hosts_file%

:end
REM Limpia archivos temporales
del ping_result.txt
del %temp_file%

echo Operacion completada.
pause
