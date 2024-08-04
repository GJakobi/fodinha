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
    next_player_port = int(input("Digite a porta do próximo: "))


    # Configurações
    host = 'localhost'
    
    # Criação do socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, self_port)
    sock.bind(addr)
    
    my_player = Player(sys.argv[1])
    
    has_bastao = is_dealer = False
    if(int(my_player.name) == 0):
        has_bastao = is_dealer = True
        
    players = []
    
    if is_dealer:
        print("Sou o dealer")
        deck = Deck()
        deck.shuffle()
        hands = deck.draw_hands(NUM_OF_PLAYERS)
        virada = deck.draw()
        print(f"Virada: {virada}")
        #TODO: colocar o gato
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
        
        if pacote["state"] == "DEALING":
            if has_bastao == True:
                print("Agora é a hora de fazer as apostas")
                my_player.askBet()
                message = json.dumps({"state": "BETTING", "bets": [{"player": my_player.name, "bet": my_player.bet}]})
                sock.sendto(message.encode(), (host, next_player_port))
                return
            
            
            my_hand = next(player_info["hand"] for player_info in pacote["hands"] if player_info["player"] == int(my_player.name))
            my_player.receive_hand(my_hand)
            
            print(f"Minha mão: {my_player.show_hand()}")
            sock.sendto(data, (host, next_player_port))
            
        if pacote["state"] == "BETTING":
            if has_bastao == True:
                # todos apostaram, manda as apostas para todo mundo
                print("Todos apostaram")
                #TODO: criar um pacote com as apostas, e enviar para todo mundo saber as apostas dos outros
            
            print("Agora é a hora de fazer as apostas")
            #TODO: pegar as maos existentes no "pacote", concatenar com a minha e enviar para o próximo
            my_player.askBet()
            
        if pacote["state"] == "INFORMATION":
            if has_bastao == True:
                print("Agora é a hora de jogar")
            
            
            print("Apostas dos jogadores:")
            #TODO: mostrar todas as apostas recebidas no pacote
            
        if pacote["state"] == "PLAYING":
            if has_bastao == True:
                print("Agora é a hora de computar os resultados")
                #TODO: computar o reusltado enviar pacote mostrando o resultado da rodada
                
                #TODO: se é a ultima carta, invés de jogar pro result, joga pro end of round
            
            print("Cartas jogadas:")
            #TODO: Mensagem da volta pelo anel, cada jogador que recebe a mensagem deve mostrar as cartas já jogadas, decidir qual carta jogar, adicionar carta na mensagem e reenviar a mensagem

        if pacote["state"] == "RESULT":
            if has_bastao == True:
                print("Agora é a hora de começar a próxima rodada")
            
            #TODO: atualizar a pontuação de cada jogador
        
        if pacote["state"] == "END_OF_ROUND":
            if has_bastao == True:
                # começar novo jogo, passar o bastao pra frente
                print("alo")
            
            print("Resultado da rodada:")
            # informar todos os jogadores sobre a nova pontuação

    sock.close()

if __name__ == "__main__":
    main()

