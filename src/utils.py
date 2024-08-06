import sys

def get_ports():
    if len(sys.argv) < 2:
        print("args missing")
        return None, None
    self_port = int(input("Digite a porta: "))
    next_player_port = int(input("Digite a porta do próximo: "))
    return self_port, next_player_port

def get_player_name():
    if len(sys.argv) < 2:
        print("args missing")
        return None
    return sys.argv[1]
