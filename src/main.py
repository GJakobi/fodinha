import socket
import json
from .deck import Deck
from .card import Card
from .player import Player
import sys

# Em cada mão do jogo

#     Carteador deve sortear as cartas e enviar para cada jogador as suas cartas
#     As cartas podem ser enviadas todas em uma mesma mensagem ou uma mensagem para cada jogador
#     Depois das cartas, cada jogador deve fazer as suas apostas (uma mensagem da a volta pelo anel completando as apostas)
#     Nova mensagem da a volta pelo anel informando e atualizando as apostas de cada jogador na tela
#     Depois das apostas, começa-se o jogo. 
#     Mensagem da volta pelo anel, cada jogador que recebe a mensagem deve mostrar as cartas já jogadas, decidir qual carta jogar, adicionar carta na mensagem e reenviar a mensagem
#     Depois da mensagem dar a volta no anel, o carteador deve computar o resultado da rodada, e enviar o resultado para todos os jogadores
#     Depois deve começar a próxima rodada
#     Ao terminar as cartas de cada mão. O carteador deve computar o resultado geral e a pontuação de cada jogador. 
#     Informar os jogadores sobre a nova pontuação
#     Passar o bastão para a frente, para que o próximo jogador seja o carteador


NUM_OF_PLAYERS = 4
BASTAO = "BASTAO"

def main():    
    if(len(sys.argv) < 2):
        print("args missing")
        return
    
    self_port = int(input("Digite a porta: "))

    # Configurações
    host = 'localhost'
    next_player_port = int(input("Digite a porta do próximo: "))

    # Criação do socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, self_port)
    sock.bind(addr)
    
    my_player = Player(sys.argv[1])
    
    has_bastao = is_first_dealer = False
    if(int(my_player.name) == 0):
        has_bastao = is_first_dealer = True
        
    players = []

    
    if is_first_dealer:
        print("Sou o dealer")
        deck = Deck()
        deck.shuffle()
        hands = deck.draw_hands(NUM_OF_PLAYERS)
        virada = deck.draw()
        print(f"Virada: {virada}")
        for i in range(NUM_OF_PLAYERS):
            player = Player(i)
            player.hand = hands[i]
            players.append(player)
            
        my_player.receive_hand(hands[0])
            
        # enviamos todas as cartas em uma mesma mensagem
        message = json.dumps({"state": "DEALING" ,"hands":[{"player": player.name, "hand": player.show_hand()} for player in players]})  
        
        sock.sendto(message.encode(), (host, next_player_port))    
      
    
    while True:
        print("Aguardando mensagem...")
        data, addr = sock.recvfrom(1024)
        pacote = json.loads(data.decode())

        print(pacote)
        
        if pacote["state"] == "DEALING":
            #TODO: se o dealer receber a mensagem, quer dizer que ele já deu as cartas
            # então deve começar a proxima fase do jogo
            
            
            my_hand = next(player_info["hand"] for player_info in pacote["hands"] if player_info["player"] == int(my_player.name))
            my_player.receive_hand(my_hand)
            
            print(f"Minha mão: {my_player.show_hand()}")
            #TODO: mandar mensagem para o proximo jogador
    

    sock.close()

if __name__ == "__main__":
    main()

