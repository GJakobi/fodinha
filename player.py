import socket
import time

porta1 = int(input("Digite a porta: "))

# Configurações
host = 'localhost'


porta2 = int(input("Digite a porta do proximo: "))


# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr1 = (host, porta1)
sock.bind(addr1)

proximoJogador = (host, porta2)


# Enviar uma mensagem inicial para o próximo jogador
if porta1 == 5001:
    msg = input("Jogador, insira uma mensagem para o próximo jogador: ")
    sent = False
    while not sent:
        try:
            sock.sendto(msg.encode(), proximoJogador)
            sent = True
        except socket.error:
            time.sleep(1)

# Loop principal
while True:
    data, addr = sock.recvfrom(1024)
    print(f"{addr} diz: {data.decode()}")

    if data.decode() == "Encerrar":
        break

    # Enviar a mensagem de volta para o jogador 2
    msg = input("Digite uma mensagem: ")
    sock.sendto(msg.encode(), proximoJogador)

sock.close()