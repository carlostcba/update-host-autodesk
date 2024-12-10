import os
import shutil
import subprocess
import re
import ctypes
import sys

def is_admin():
    """Verifica si el script se está ejecutando con permisos de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    """Reinicia el script con permisos de administrador."""
    if not is_admin():
        print("El script necesita ejecutarse como administrador. Reiniciando...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        sys.exit()

def ping_host():
    """Realiza un ping y devuelve la IP si se encuentra."""
    host = "autodesk.lasalleflorida.edu.ar"
    result = subprocess.run(["ping", "-n", "1", "-4", host], capture_output=True, text=True)
    match = re.search(r"\[(\d+\.\d+\.\d+\.\d+)\]", result.stdout)
    if match:
        return match.group(1)
    else:
        print("No se pudo obtener la dirección IP.")
        sys.exit()

def backup_hosts_file(hosts_file):
    """Crea una copia de seguridad del archivo hosts."""
    backup_file = f"{hosts_file}.bak"
    shutil.copy(hosts_file, backup_file)
    print(f"Copia de seguridad creada: {backup_file}")

def update_hosts_file(hosts_file, ip_address):
    """Actualiza la IP de AUTODESKSERVER en el archivo hosts."""
    temp_file = os.path.join(os.getenv("TEMP"), "hosts_temp")
    with open(hosts_file, "r") as file, open(temp_file, "w") as temp:
        for line in file:
            if "AUTODESKSERVER" in line:
                temp.write(f"{ip_address} AUTODESKSERVER\n")
            else:
                temp.write(line)
    shutil.move(temp_file, hosts_file)
    print("Archivo hosts actualizado correctamente.")

def main():
    restart_as_admin()  # Asegura que el script tenga permisos de administrador
    ip_address = ping_host()
    print(f"Dirección IP obtenida: {ip_address}")
    
    hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
    backup_hosts_file(hosts_file)
    update_hosts_file(hosts_file, ip_address)
    print("Operación completada.")

if __name__ == "__main__":
    main()
