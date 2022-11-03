import winreg
import socket
import urllib.request, json

CPU_INFO_KEY = r"HARDWARE\DESCRIPTION\System\\CentralProcessor\\0"
GPU_INFO_FOLDER = "SOFTWARE\\Microsoft\\DirectX"

def connect_to_registry():
    try:
        reg_connection = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    except OSError:
        return
    return reg_connection

def get_cpu_info(reg_conn):
    try:
        reg_open = winreg.OpenKey(reg_conn, CPU_INFO_KEY)
        processor_name = winreg.QueryValueEx(reg_open, "ProcessorNameString")
        return processor_name[0]
    except OSError:
        return "Unknown"
        
def get_gpu_info(reg_conn):
    try:
        GPU_DEFAULT_NAME = "Microsoft Basic Render Driver"
        GPU_NAME = ""
        reg_open = winreg.OpenKey(reg_conn, GPU_INFO_FOLDER)
        for index in range(4):
            reg_subkey = winreg.EnumKey(reg_open, index)
            subkey = winreg.OpenKey(reg_open, reg_subkey)
            subkey_description = winreg.QueryValueEx(subkey, "Description")
            if subkey_description[0] != GPU_DEFAULT_NAME:
                GPU_NAME = subkey_description[0]
                break
            else:
                GPU_NAME = GPU_DEFAULT_NAME
        return GPU_NAME
    except OSError:
        return "Unknown"

def get_device_name():
    return socket.gethostname()
        
def get_external_ip_address():
    try:
        data = json.loads(urllib.request.urlopen("http://ip.jsontest.com").read())
        return data["ip"]
    except Exception:
        return "0.0.0.0" # Bad Internet, No Worky
    
def get_all_and_format():
    # Format
    # RYZEN 5900x AMD       IP ADDRESS: 250.356.532
    # GeFORCE RTX 3080      DEVICE NAME: YUZU
    regconn = connect_to_registry()
    sys_gpu = get_gpu_info(regconn) 
    sys_cpu = get_cpu_info(regconn)
    sys_ip = get_external_ip_address()
    sys_hostname = get_device_name()
    
    bigger_string = max(sys_gpu, sys_cpu, key=len)
    smaller_string = min(sys_cpu, sys_gpu, key=len) # Extra work but lazy
    
    space_diff = len(bigger_string) - len(smaller_string)
    smaller_string += ' '*(space_diff + 4)
    bigger_string += ' '*4
    
    sysinfo = f"{smaller_string}{sys_hostname}\n{bigger_string}{sys_ip}"
    return sysinfo