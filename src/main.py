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

NUM_OF_PLAYERS = 2
BASTAO = "BASTAO"

def upsert_bet(bets, player, bet):
    for i in range(len(bets)):
        if bets[i]["player"] == player:
            bets[i]["bet"] = bet
            return bets
    bets.append({"player": player, "bet": bet})
    return bets

def upsert_card(cards, player, card):
    for i in range(len(cards)):
        if cards[i]["player"] == player:
            cards[i]["card"] = card
            return cards
    cards.append({"player": player, "card": card, "wins": 0})
    return cards

def deal_cards(players):
    deck = Deck()
    deck.shuffle()
    hands = deck.draw_hands(NUM_OF_PLAYERS)
    virada = deck.draw()
    
    for i in range(NUM_OF_PLAYERS):
        player = Player(i)
        player.hand = hands[i]
        players.append(player)
    
    return hands, virada
    

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
    
    has_bastao = False
    if(int(my_player.name) == 0):
        has_bastao = True
        
    players = []
    if has_bastao:
        print("Sou o dealer")
        hands, virada = deal_cards(players)
        print(f"Virada: {virada}")
        #TODO: colocar o gato
            
        my_player.receive_hand(hands[0])
        
        print(f"Minha mão: {my_player.show_hand()}")
            
        # enviamos todas as cartas em uma mesma mensagem
        message = json.dumps({"state": "DEALING" ,"hands":[{"player": player.name, "hand": player.show_hand()} for player in players]})  
        
        sock.sendto(message.encode(), (host, next_player_port))    
      
    
    while True:
        data, addr = sock.recvfrom(1024)
        pacote = json.loads(data.decode())
        
        if pacote["state"] == "DEALING":
            if "token" in pacote:
                has_bastao = True
            
            if has_bastao == True:
                # se o pacote ja tem as mãos, entao ja foi distribuida as cartas
                if "hands" in pacote:
                    message = json.dumps({"state": "BETTING", "bets": []})
                    sock.sendto(message.encode(), (host, next_player_port))     
                # se não, distribui as cartas             
                else:               
                    hands, virada = deal_cards(players)
                    print(f"Virada: {virada}")
                    
                    my_player.receive_hand(hands[0])
                    
                    print(f"Minha mão: {my_player.show_hand()}")
                    
                    message = json.dumps({"state": "DEALING" ,"hands":[{"player": player.name, "hand": player.show_hand()} for player in players]})
                    
                    sock.sendto(message.encode(), (host, next_player_port))
                continue
            
        
            my_hand = next(player_info["hand"] for player_info in pacote["hands"] if player_info["player"] == int(my_player.name))
            my_hand = [Card.from_string(card_str) for card_str in my_hand]
            my_player.receive_hand(my_hand)
            
            print(f"Minha mão: {my_player.show_hand()}")
            sock.sendto(data, (host, next_player_port))
            
        if pacote["state"] == "BETTING":
            if has_bastao == True:
                my_player.ask_bet()
                bets = pacote["bets"]
                bets = upsert_bet(bets, my_player.name, my_player.bet)
                message = json.dumps({"state": "BETS_INFORMATION", "bets": bets})
                sock.sendto(message.encode(), (host, next_player_port))
                continue
            
            print("Agora é a hora de fazer as apostas")
            my_player.ask_bet()
            bets = pacote["bets"]
            bets = upsert_bet(bets, my_player.name, my_player.bet)
            message = json.dumps({"state": "BETTING", "bets": bets})
            sock.sendto(message.encode(), (host, next_player_port))
            
        if pacote["state"] == "BETS_INFORMATION":
            print("Apostas dos jogadores:")
            bets = pacote["bets"]
            #TODO: mostrar bonitinho
            print(bets)
            if has_bastao == True:
                message = json.dumps({"state": "PLAYING", "cards": []})
                sock.sendto(message.encode(), (host, next_player_port))
                continue
            sock.sendto(data, (host, next_player_port))
            
        if pacote["state"] == "PLAYING":
            cards_played = pacote["cards"]
            
            if len(cards_played) > 0:
                print(f"Cartas jogadas: {cards_played}")
                
            card_played = my_player.ask_play()
            print(f"Carta jogada: {card_played}")
            
            if has_bastao == True:                
                cards_played = upsert_card(cards_played, my_player.name, str(card_played))
                
                print("Agora é a hora de computar os resultados")
                all_cards = []
                for card_info in cards_played:
                    player = card_info["player"]
                    card = Card.from_string(card_info["card"])
                    all_cards.append((player, card))
                    
                all_cards.sort(key=lambda x: x[1].calculate_value())
                                
                player_won = all_cards[-1][0]      
                
                #increment number of wins of the player that won the round
                for card_info in cards_played:
                    if card_info["player"] == player_won:
                        card_info["wins"] += 1          
                
                if len(my_player.hand) == 0:
                    message = json.dumps({"state": "END_OF_ROUND", "result": cards_played})
                    sock.sendto(message.encode(), (host, next_player_port))
                    continue
                
                message = json.dumps({"state": "RESULT", "result": cards_played, "last_win": player_won})
                sock.sendto(message.encode(), (host, next_player_port))
                continue
            
            cards_played = upsert_card(cards_played, my_player.name, str(card_played))
            message = json.dumps({"state": "PLAYING", "cards": cards_played})
            sock.sendto(message.encode(), (host, next_player_port))
            

        if pacote["state"] == "RESULT":
            result = pacote["last_win"]
            print(f"Resultado da rodada: Jogador {result} ganhou")
            if has_bastao == True:
                print("Agora é a hora de começar a próxima rodada")
                cards_played = pacote["result"]
                message = json.dumps({"state": "PLAYING", "cards": cards_played})
                sock.sendto(message.encode(), (host, next_player_port))
                continue            
            sock.sendto(data, (host, next_player_port))
        
        if pacote["state"] == "END_OF_ROUND":
            print("Resultado da rodada:")
            print(pacote["result"])
            
            # subtract the number of lifes, it's the difference between the bets and the number of wins
            my_bet = my_player.bet
            my_wins = next(card_info["wins"] for card_info in pacote["result"] if card_info["player"] == my_player.name)
            my_player.lives -= my_bet - my_wins
        
            print(f"Minhas vidas: {my_player.lives}")
            
            #reset everything
            my_player.bet = 0
            my_player.hand = []
                        
            if has_bastao == True:
                # começar novo jogo, passar o bastao pra frente
                print("Fim da rodada")
                has_bastao = False
                
                message = json.dumps({"state": "DEALING", "token": BASTAO})
                sock.sendto(message.encode(), (host, next_player_port))
                continue
            sock.sendto(data, (host, next_player_port))

    sock.close()

if __name__ == "__main__":
    main()

