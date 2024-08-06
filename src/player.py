class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bet = 0
        self.lives = 1

    def receive_hand(self, hand):
        self.hand = hand

    def show_hand(self):
        return [str(card) for card in self.hand]
    
    def ask_bet(self):
        bet = int(input("Digite a aposta: "))
        self.bet = bet
        return bet
    
    def find_card(self, suit, rank):
        for card in self.hand:
            if card.suit == suit and card.rank == rank:
                return card
        return None 
    
    def is_alive(self):
        return self.lives > 0
    
    def ask_play(self):
        print(f"Minha mão: {self.show_hand()}")
        suit = input("Digite o naipe: ")
        rank = input("Digite a carta: ")
        card = self.find_card(suit, rank)
        if card is None:
            print("Carta não encontrada")
            return self.ask_play()
        self.hand.remove(card)
        return card

    def __repr__(self):
        return f"player({self.name}, hand: {self.show_hand()})"
