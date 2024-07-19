import socket
import time
import json
from .shuffler import Shuffler
from .card import Card
from .player import Player

def distribuir_cartas(sock, shuffler, jogadores, num_cartas):
    shuffler.shuffle()

    for _ in range(num_cartas):
        for jogador in jogadores:
            carta = shuffler.draw()
            jogador.receive_card(carta)
            pacote = {
                "estado": "Dando Carta",
                "carta": str(carta),
                "destino": jogador.name
            }
            sock.sendto(json.dumps(pacote).encode(), jogador.address)
            data, addr = sock.recvfrom(1024)
            pacote = json.loads(data.decode())
            print(f"Carta {carta} entregue ao jogador {addr}")

            print(jogador.hand)

    vira = shuffler.draw()
    print(f"A carta vira é: {vira}")
    gato_index = Card.ranks.index(vira.rank) + 1
    print(f"O gato está na posição {gato_index}")
    Card.set_gato(Card, gato_index)


def enviar_mensagem_inicial(sock, proximoJogador):
    carta = input("Digite a carta a ser jogada: ")
    sent = False
    pacote = {
        "estado": "Jogando",
        "carta": carta,
        "destino": proximoJogador.name
    }
    while not sent:
        try:
            # enviar o pacote, com a carta e o destino via JSON
            sock.sendto(json.dumps(pacote).encode(), proximoJogador.address)
            sent = True
        except socket.error:
            time.sleep(1)


def main():
    porta1 = int(input("Digite a porta: "))

    # Configurações
    host = 'localhost'
    porta2 = int(input("Digite a porta do próximo: "))

    # Criação do socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr1 = (host, porta1)
    sock.bind(addr1)

    jogadores = [
        Player("Jogador1", addr1),
        Player("Jogador2", (host, porta2))
    ]

    proximoJogador = jogadores[1]  # O próximo jogador para começar é o segundo na lista

    # Inicializar o shuffler e embaralhar o baralho uma vez
    shuffler = Shuffler()

    # Distribuir as cartas inicialmente
    distribuir_cartas(sock, shuffler, jogadores, 3)

    # Enviar uma mensagem inicial para o próximo jogador se for o jogador 1
    if porta1 == 5001:
        enviar_mensagem_inicial(sock, proximoJogador)

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
        proximoJogador = jogadores[(jogadores.index(proximoJogador) + 1) % 2]  # Próximo jogador na lista circular
        pacote["destino"] = proximoJogador.name
        sock.sendto(json.dumps(pacote).encode(), proximoJogador.address)

    sock.close()


if __name__ == "__main__":
    main()

