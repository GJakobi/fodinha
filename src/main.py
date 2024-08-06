import json
from .deck import Deck
from .card import Card
from .player import Player
from .network import setup_socket
from .utils import get_player_name, get_ports

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
    Card.set_gato(virada)
    
    for i in range(NUM_OF_PLAYERS):
        player = Player(i)
        player.hand = hands[i]
        players.append(player)
    
    return hands, virada
    

def main():    
    self_port, next_player_port = get_ports()
    if self_port is None or next_player_port is None:
        return

    host = "localhost"
    sock = setup_socket(self_port, host)
    
    my_player = Player(get_player_name())
    
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
                if my_player.is_alive() == False:
                    sock.sendto(data, (host, next_player_port))
                    continue
                has_bastao = True
            
            if has_bastao == True:
                # se o pacote ja tem as mãos, entao ja foi distribuida as cartas
                if "hands" in pacote:
                    message = json.dumps({"state": "BETTING", "bets": []})
                    sock.sendto(message.encode(), (host, next_player_port))     
                # se não, distribui as cartas             
                else:          
                    players = []    
                    hands, virada = deal_cards(players)
                    print(f"Virada: {virada}")
                    
                    my_player.receive_hand(hands[0])
                    
                    print(f"Minha mão: {my_player.show_hand()}")
                    
                    message = json.dumps({"state": "DEALING" ,"hands":[{"player": player.name, "hand": player.show_hand()} for player in players]})
                    
                    sock.sendto(message.encode(), (host, next_player_port))
                continue
            
        
            if my_player.is_alive() == False:
                sock.sendto(data, (host, next_player_port))
                continue
        
            my_hand = next(player_info["hand"] for player_info in pacote["hands"] if player_info["player"] == int(my_player.name))
            my_hand = [Card.from_string(card_str) for card_str in my_hand]
            my_player.receive_hand(my_hand)
            
            print(f"Minha mão: {my_player.show_hand()}")
            sock.sendto(data, (host, next_player_port))
            
        if pacote["state"] == "BETTING":
            if my_player.is_alive() == False:
                sock.sendto(data, (host, next_player_port))
                continue
            
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
            if my_player.is_alive() == False:
                print("Você perdeu todas as vidas")
                sock.sendto(data, (host, next_player_port))
                continue
            
            bets = pacote["bets"]
            
            if len(bets) == 1:
                print("Você venceu!")
                sock.close()
                return

            print("Apostas dos jogadores:")
            #TODO: mostrar bonitinho
            print(bets)
            if has_bastao == True:
                message = json.dumps({"state": "PLAYING", "cards": []})
                sock.sendto(message.encode(), (host, next_player_port))
                continue
            sock.sendto(data, (host, next_player_port))
            
        if pacote["state"] == "PLAYING":
            if my_player.is_alive() == False:
                print("Você perdeu todas as vidas")
                sock.sendto(data, (host, next_player_port))
                continue

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
            
            if my_player.is_alive() == False:
                sock.sendto(data, (host, next_player_port))
                continue
            
            # subtract the number of lifes, it's the difference between the bets and the number of wins
            my_bet = my_player.bet
            my_wins = next(card_info["wins"] for card_info in pacote["result"] if card_info["player"] == my_player.name)
            my_player.lives -= abs(my_bet - my_wins)
        
            print(f"Minhas vidas: {my_player.lives}")
            
            #reset everything
            Card.reset_gato()
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


if __name__ == "__main__":
    main()

