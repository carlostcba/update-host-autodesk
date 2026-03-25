import os
import sys
import socket
import shutil
import ctypes
import subprocess
import time
from datetime import datetime

HOST_TO_RESOLVE = "autodesk.lasalleflorida.edu.ar"
TARGET_TAG = "AUTODESKSERVER"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
INSTALL_DIR = r"C:\ProgramData\AutodeskHostConnector"
EXE_NAME = "update_host.exe"
LOG_FILE = os.path.join(INSTALL_DIR, "update_host.log")
TARGET_PATH = os.path.join(INSTALL_DIR, EXE_NAME)
TASK_NAME = "AutodeskHostConnector"

def log_message(message):
    """Escribe un mensaje en el archivo de log."""
    os.makedirs(INSTALL_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")
    except Exception as e:
        print(f"Error escribiendo en el log: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        return True
    log_message("No somos administrador, intentando elevar privilegios...")
    # Re-run the program with admin rights
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return True
    except Exception as e:
        log_message(f"Error al intentar elevar privilegios: {e}")
        return False

def deploy_self():
    """Copia el ejecutable a una ruta permanente y crea la tarea programada."""
    log_message("Iniciando despliegue/verificación de instalación...")
    
    if not is_admin():
        run_as_admin()
        sys.exit(0)

    try:
        os.makedirs(INSTALL_DIR, exist_ok=True)
        
        current_exe = sys.executable
        if getattr(sys, 'frozen', False):
            # Solo realizamos el despliegue si estamos corriendo como .exe congelado
            if current_exe.lower() != TARGET_PATH.lower():
                log_message(f"Copiando ejecutable actual a {TARGET_PATH}")
                shutil.copy2(current_exe, TARGET_PATH)
        else:
            log_message("Corriendo como script .py, saltando copia de ejecutable.")

        # Verificar si la tarea ya existe
        check_cmd = f'schtasks /query /tn "{TASK_NAME}"'
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            log_message("Creando tarea programada...")
            # /sc onstart /rl highest /ru SYSTEM permite ejecución al arrancar el equipo (sin usuario)
            cmd = f'schtasks /create /f /tn "{TASK_NAME}" /tr "{TARGET_PATH}" /sc onstart /rl highest /ru SYSTEM'
            subprocess.run(cmd, shell=True, capture_output=True)
        else:
            log_message("La tarea programada ya existe.")
        
        return True
    except Exception as e:
        log_message(f"Error en deploy_self: {e}")
        return False

def update_hosts(ip_address):
    log_message(f"Actualizando archivo hosts con la IP: {ip_address}")
    try:
        # Backup hosts file
        shutil.copy2(HOSTS_PATH, HOSTS_PATH + ".bak")
        
        with open(HOSTS_PATH, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        found = False
        for line in lines:
            if TARGET_TAG in line:
                new_lines.append(f"{ip_address} {TARGET_TAG}\n")
                found = True
            else:
                new_lines.append(line)
        
        if not found:
            new_lines.append(f"\n{ip_address} {TARGET_TAG}\n")
            
        with open(HOSTS_PATH, 'w') as f:
            f.writelines(new_lines)
            
        log_message("Archivo hosts actualizado correctamente.")
        return True
    except Exception as e:
        log_message(f"Error actualizando archivo hosts: {e}")
        return False

def resolve_ip_with_retry(host, retries=10, delay=10):
    log_message(f"Intentando resolver {host}...")
    for i in range(retries):
        try:
            ip = socket.gethostbyname(host)
            log_message(f"Resolución exitosa en el intento {i+1}: {ip}")
            return ip
        except socket.gaierror:
            log_message(f"Intento {i+1} fallido. Reintentando en {delay} segundos...")
            time.sleep(delay)
    log_message(f"No se pudo resolver {host} después de {retries} intentos.")
    return None

def main():
    log_message("--- Inicio de ejecución ---")
    
    # 1. Verificar si estamos en la ruta de instalación
    current_exe = sys.executable
    is_installed = current_exe.lower() == TARGET_PATH.lower()

    if not is_installed:
        if deploy_self():
            log_message("Despliegue completado. Saliendo de este proceso.")
            sys.exit(0)
    
    # 2. Lógica principal (Actualizar Hosts)
    ip_address = resolve_ip_with_retry(HOST_TO_RESOLVE)
    
    if ip_address:
        if is_admin() or is_installed:
            update_hosts(ip_address)
        else:
            log_message("No somos admin ni proceso instalado. Intentando elevación...")
            run_as_admin()
    else:
        log_message("Saltando actualización de hosts por falta de resolución IP.")

    log_message("--- Fin de ejecución ---")

if __name__ == "__main__":
    main()
