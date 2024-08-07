import socket

def setup_socket(self_port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, self_port)
    print(f"Binding to {addr}")
    sock.bind(addr)
    return sock
