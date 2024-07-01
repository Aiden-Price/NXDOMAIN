# SID: 530502821

from sys import argv
import socket
import time

MIN_PORT = 1024
MAX_PORT = 65535

def is_valid_A_or_B(segment: str) -> bool:
    if not segment:
        return False
    for char in segment:
        if not (char.isalnum() or char == '-'):
            return False
    return True

def is_valid_C(segment: str) -> bool:
    if segment.startswith('.') or segment.endswith('.'):
        return False
    parts = segment.split('.')
    return all(is_valid_A_or_B(part) for part in parts)

def is_valid_hostname(hostname: str) -> bool:

    if len(hostname) == 0:
        return False
    
    parts = hostname.split('.')

    if len(parts) < 3:
        return False

    for x in parts:
        for c in x:
            if not (c.isalnum() or c == '-'):
                return False

    return True

def q_ser(server_port: int, query: str, timeout: float, server_type: str) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(timeout)
            client_socket.connect(("localhost", server_port))
            client_socket.sendall(query.encode())
            response = client_socket.recv(1024).decode().strip()
            if response == "NXDOMAIN":
                print("NXDOMAIN")
                return ""
            return response
    except (ConnectionRefusedError):
        print(f"FAILED TO CONNECT TO {server_type.upper()}")
        return ""
    except (TimeoutError, socket.timeout):
        return ""

def res(root_port: int, timeout: float) -> None:
    while True:
        try:
            user = input("")
            if not user:
                break

            if not is_valid_hostname(user):
                print("INVALID")
                continue

            start_time = time.time()

            root_response = q_ser(root_port, user.split('.')[-1] + "\n", timeout, "root")
            if time.time() - start_time > timeout:
                print("NXDOMAIN")
                continue

            if not root_response:
                continue

            tld_response = q_ser(int(root_response), user.split('.')[-2] + '.' + user.split('.')[-1] + "\n", timeout, "tld")
            if time.time() - start_time > timeout:
                print("NXDOMAIN")
                continue

            if not tld_response:
                continue

            auth_response = q_ser(int(tld_response), user + "\n", timeout, "auth")
            if time.time() - start_time > timeout:
                print("NXDOMAIN")
                continue

            if not auth_response:
                continue

            print(auth_response)

        except EOFError:
            break
        except Exception as e:
            break

def main(args: list[str]) -> None:
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        return

    try:
        root_port = int(args[0])
        timeout = float(args[1])
    except ValueError:
        print("FAILED TO CONNECT TO ROOT")
        return

    if not (MIN_PORT <= root_port <= MAX_PORT):
        print("INVALID ARGUMENTS")
        return

    res(root_port, timeout)

if __name__ == "__main__":
    main(argv[1:])

