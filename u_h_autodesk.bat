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
copy "%hosts_file%" "%hosts_file%.bak"

REM Crea un archivo temporal para la nueva versión del archivo hosts
set "temp_file=%temp%\hosts_temp"
> "%temp_file%" (
    for /f "tokens=*" %%A in ('type "%hosts_file%"') do (
        set "line=%%A"
        echo !line! | findstr /i "AUTODESKSERVER" >nul
        if not errorlevel 1 (
            REM Reemplaza la línea que contiene AUTODESKSERVER con un solo espacio
            echo %ip_address% AUTODESKSERVER
        ) else (
            REM Copia la línea tal cual si no coincide
            echo %%A
        )
    )
)

REM Sobrescribe el archivo hosts con el archivo temporal
copy /y "%temp_file%" "%hosts_file%"

:end
REM Limpia archivos temporales
del ping_result.txt
del "%temp_file%"

echo Operacion completada.
