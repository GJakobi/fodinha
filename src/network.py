import socket
import json

def setup_socket(self_port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, self_port)
    sock.bind(addr)
    return sock