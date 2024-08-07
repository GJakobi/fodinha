import random
from .card import Card

NUMBER_OF_CARDS = 3

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop() if self.deck else None
    
    # N is the number of cards to draw
    def draw_hand(self, n):
        return [self.draw() for _ in range(n)]
       
    def draw_hands(self, n):
        return [self.draw_hand(NUMBER_OF_CARDS) for _ in range(n)]
        
    def reset_deck(self):
        self.deck = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
