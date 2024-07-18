
class Card:
    suits = ['Hearts', 'Coins', 'Clubs', 'Spades']
    ranks = ['4', '5', '6', '7', '8', '9', '10',
             'Queen', 'Jack', 'King', 'Ace', '2', '3']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        return self.ranks.index(self.rank) < self.ranks.index(other.rank)

    def set_gato(cls, rank):
        index = cls.ranks.index(rank)
        cls.ranks = cls.ranks[index + 1:] + cls.ranks[:index + 1]
