class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bet = 0
        self.lives = 12

    def receive_hand(self, hand):
        self.hand = hand

    def play_card(self):
        return self.hand.pop(0) if self.hand else None

    def show_hand(self):
        return [str(card) for card in self.hand]
    
    def askBet(self):
        bet = int(input("Digite a aposta: "))
        self.bet = bet
        return bet

    def __repr__(self):
        return f"player({self.name}, hand: {self.show_hand()})"
