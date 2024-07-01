"""
SID: 50302821 
"""
from sys import argv
import socket

def load(config_file):
    config = {}
    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
            config['port'] = int(lines[0].strip())
            if not 1024 <= config['port'] <= 65535:
                raise ValueError("Invalid port range in configuration")
            
            for line in lines[1:]:
                section = line.strip().split(',')
                if len(section) == 2:
                    domain = section[0]
                    port = int(section[1])
                    if not is_valid_domain(domain):
                        raise ValueError(f"Invalid domain in configuration: {domain}")
                    if not 1024 <= port <= 65535:
                        raise ValueError("Invalid port range in configuration")

                    config[domain] = port
                    
    except Exception as e:
        print("INVALID CONFIGURATION")
        exit(1)

    return config

def is_valid_domain(domain: str) -> bool:
    if domain.startswith(".") or domain.endswith("."):
        return False
    labels = domain.split('.')
    for label in labels:
        if not label:
            return False 
        if label.startswith('-') or label.endswith('-'):
            return False  
        for char in label:
            if not char.isalnum() and char != '-':
                return False  
    return True

def add(config, data, socket_user):
    sections = data.split()
    if len(sections) == 3 and sections[0] == "!ADD":
        h_name = sections[1]
        port = int(sections[2])
        if 1024 <= port <= 65535:
            if h_name in config and config[h_name] == port:
                return  
            config[h_name] = port
        else:
            print("Port must be in the range [1024, 65535].")
            socket_user.send("INVALID PORT\n".encode("utf-8"))
          
def dele(config, data):
    sections = data.split()
    if len(sections) == 2 and sections[0] == "!DEL":
        h_name = sections[1]
        if h_name in config:
            del config[h_name]

def res(host, port, config, socket_user):
    if host in config:
        x = config[host]
        response = f"resolve {host} to {x}"
        response_server = f"{x}\n"
        print(response)
        socket_user.send(response_server.encode("utf-8"))
    else:
        response = f"resolve {host} to NXDOMAIN"
        response_server = f"NXDOMAIN\n"
        print(response)
        socket_user.send(response_server.encode("utf-8"))

def main(args: list[str]) -> None:
    if len(args) != 1:
        print("INVALID ARGUMENTS")
        return 

    config_file = args[0]
    config = load(config_file)
    message_incomplete = ""
    server_address = ('localhost', config['port'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        server_socket.bind(server_address)
        server_socket.listen(1)
        _, assigned_port = server_socket.getsockname()
        
        while True:
            try:
                try:
                    socket_user, addr = server_socket.accept()
                except socket.error as e:
                    print(f"Error accepting connection: {str(e)}")
                    continue
    
                with socket_user:
                    while True:
                        info = socket_user.recv(config['port']).decode("utf-8")
                        
                        if not info:
                            break

                        msg = (message_incomplete + info).split('\n') 
                        message_incomplete = msg.pop()

                        for message in msg:
                            if message:
                                if message.startswith('!'):
                                    if message.startswith('!ADD'):
                                        add(config, message, socket_user)
                                    elif message.startswith('!DEL'):
                                        dele(config, message)
                                    elif message == '!EXIT':
                                        return
                                    else:
                                        print("INVALID")
                                else:
                                    res(message, assigned_port, config, socket_user)
            except Exception as e:
                print("ERROR:", str(e))
        client_socket.close()
if __name__ == "__main__":
    main(argv[1:])
