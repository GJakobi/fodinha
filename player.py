import socket
import time
import json

porta1 = int(input("Digite a porta: "))

# Configurações
host = 'localhost'

porta2 = int(input("Digite a porta do próximo: "))

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr1 = (host, porta1)
sock.bind(addr1)

proximoJogador = (host, porta2)

# Definir estrutura de pacote, contendo o estado do jogo, a carta jogada, e o destino final
pacote = {
    "estado": "Jogando",
    "carta": None,
    "destino": None
}

# Enviar uma mensagem inicial para o próximo jogador
if porta1 == 5001:
    carta = input("Digite a carta a ser jogada: ")
    sent = False
    while not sent:
        try:
            # enviar o pacote, com a carta e o destino via JSON
            pacote["carta"] = carta
            pacote["destino"] = proximoJogador
            sock.sendto(json.dumps(pacote).encode(), proximoJogador)
            sent = True
        except socket.error:
            time.sleep(1)

# Loop principal
while True:
    data, addr = sock.recvfrom(1024)
    pacote = json.loads(data.decode())

    # printar carta recebida
    print("Carta recebida: ", pacote["carta"])

    if pacote["estado"] == "Encerrar":
        break

    # Enviar a mensagem de volta para o próximo jogador
    carta = input("Digite a carta: ")
    pacote["carta"] = carta
    pacote["destino"] = proximoJogador
    sock.sendto(json.dumps(pacote).encode(), proximoJogador)

sock.close()
