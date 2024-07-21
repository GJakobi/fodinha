import random
from .card import Card


class Shuffler:

    def __init__(self, jogador):
        self.deck = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        self.jogador = jogador

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop() if self.deck else None

    def reset_deck(self):
        self.deck = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
