import sys
import os

def get_ports(config, index):
    if index not in config:
        print(f"Index {index} not found in config")
        return None, None
    self_port, host = config[index]
    next_index = (index + 1) % len(config)
    next_player_port, _ = config[next_index]
    return self_port, next_player_port, host

def get_player_name():
    if len(sys.argv) < 2:
        print("args missing")
        return None
    return sys.argv[1]

def read_config():
    config = {}
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.txt')
    with open(config_file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) != 3:
                continue
            index = int(parts[0])
            port = int(parts[1])
            host = parts[2]
            config[index] = (port, host)
    return config