import socket
import json
from .shuffler import Shuffler
from .card import Card
from .player import Player

def distribuir_cartas(sock, shuffler, jogadores, num_cartas):
    print("\nIniciando distribuição de cartas...")
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
            print(f"\nEnviando carta {carta} para {jogador.name}")
            sock.sendto(json.dumps(pacote).encode(), jogador.address)
            if jogador != shuffler.jogador:
                data, addr = sock.recvfrom(1024)
                pacote = json.loads(data.decode())
                print(f"Carta {carta} entregue ao jogador {addr}")
            print(jogador.hand)

    carta_vira(sock, jogadores, shuffler)

def carta_vira(sock, jogadores, shuffler):
    vira = shuffler.draw()
    print(f"\nA carta vira é: {vira}")
    
    if vira.rank == "3":
        gato_index = 0
    else:
        gato_index = Card.ranks.index(vira.rank) + 1

    Card.set_gato(Card, gato_index)

    pacote = {
        "estado": "Vira",
        "carta" : str(vira)
    }

    for jogador in jogadores:
        sock.sendto(json.dumps(pacote).encode(), jogador.address)
        print(f"Enviando carta vira {vira} para {jogador.name}")


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
        Player("Jogador2", (host, porta2)),
    ]

    shuffler = Shuffler(jogadores[0])

    if porta1 == 5001:
        print(f"Enviando handshake para {jogadores[1].address}")
        sock.sendto(json.dumps({"estado": "Handshake"}).encode(), jogadores[1].address)


        data, addr = sock.recvfrom(1024)
        pacote = json.loads(data.decode())
        if pacote.get("estado") == "Handshake":
            print(f"Conexão estabelecida com {addr}")

            distribuir_cartas(sock, shuffler, jogadores, 3)
    else:
        print(f"Aguardando handshake na porta {porta1}")
        data, addr = sock.recvfrom(1024)
        pacote = json.loads(data.decode())

        if pacote.get("estado") == "Handshake":
            print(f"Conexão estabelecida com {addr}")

            sock.sendto(json.dumps({"estado": "Handshake"}).encode(), addr)


    # Loop principal
    while True:
        print("Aguardando mensagem...")
        data, addr = sock.recvfrom(1024)
        pacote = json.loads(data.decode())

        if pacote["estado"] == "Dando Carta":
            print("Carta recebida: ", pacote["carta"])

        elif pacote["estado"] == "Vira":
            print("A carta vira é: ", pacote["carta"])

        elif pacote["estado"] == "Encerrar":
            print("Encerrando conexão...")

            break

    sock.close()

if __name__ == "__main__":
    main()

