import os
import sys
import socket
import shutil
import ctypes
import subprocess

HOST_TO_RESOLVE = "autodesk.lasalleflorida.edu.ar"
TARGET_TAG = "AUTODESKSERVER"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
INSTALL_DIR = r"C:\ProgramData\AutodeskHostConnector"
EXE_NAME = "update_host.exe"
TARGET_PATH = os.path.join(INSTALL_DIR, EXE_NAME)
TASK_NAME = "AutodeskHostConnector"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        return True
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    return False

def deploy_self():
    """Copia el ejecutable a una ruta permanente y crea la tarea programada."""
    if not is_admin():
        if not run_as_admin():
            sys.exit(0)
        return False # Just return, the elevated process will take over

    try:
        if not os.path.exists(INSTALL_DIR):
            os.makedirs(INSTALL_DIR)
        
        current_exe = sys.executable
        if getattr(sys, 'frozen', False):
            # Solo realizamos el despliegue si estamos corriendo como .exe congelado
            if current_exe.lower() != TARGET_PATH.lower():
                shutil.copy2(current_exe, TARGET_PATH)
        else:
            # Si estamos en desarrollo (.py), no nos auto-desplegamos
            return True

        # Crear tarea programada con schtasks
        # /sc onstart /rl highest /ru SYSTEM permite ejecución al arrancar el equipo (sin usuario)
        cmd = f'schtasks /create /f /tn "{TASK_NAME}" /tr "{TARGET_PATH}" /sc onstart /rl highest /ru SYSTEM'
        subprocess.run(cmd, shell=True, capture_output=True)
        
        # Ejecutar la tarea inmediatamente por primera vez
        subprocess.run(f'schtasks /run /tn "{TASK_NAME}"', shell=True, capture_output=True)
        
        return True
    except Exception as e:
        # En una aplicación real, se podría loguear el error
        return False

def update_hosts(ip_address):
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
            
        return True
    except Exception as e:
        return False

def main():
    # 1. Verificar si estamos en la ruta de instalación
    current_exe = sys.executable
    is_installed = current_exe.lower() == TARGET_PATH.lower()

    if not is_installed:
        # Proceder al despliegue
        if deploy_self():
            # Si se desplegó con éxito, este proceso ya inició al clon en SYSTEM, podemos cerrar
            sys.exit(0)
    
    # 2. Lógica principal (Actualizar Hosts)
    try:
        ip_address = socket.gethostbyname(HOST_TO_RESOLVE)
    except:
        return

    # Si estamos instalados o somos admin, procedemos
    if is_admin() or is_installed:
        update_hosts(ip_address)
    else:
        # Si de alguna forma no somos admin y no estamos instalados, pedimos elevación
        run_as_admin()

if __name__ == "__main__":
    main()
