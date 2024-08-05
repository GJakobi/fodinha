class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['4', '5', '6', '7', '8', '9', '10',
             'Queen', 'Jack', 'King', 'Ace', '2', '3']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        return self.ranks.index(self.rank) < self.ranks.index(other.rank)

    def set_gato(cls, gato_index):
        cls.ranks.append(cls.ranks.pop(gato_index))
        print(cls.ranks)
        
    @classmethod
    def from_string(cls, card_str):
        rank, suit = card_str.split(" of ")
        return cls(suit, rank)
