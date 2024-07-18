class Player:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.hand = []

    def receive_card(self, card):
        self.hand.append(card)

    def play_card(self):
        return self.hand.pop(0) if self.hand else None

    def show_hand(self):
        return [str(card) for card in self.hand]

    def __repr__(self):
        return f"Player({self.name}, Hand: {self.show_hand()})"
