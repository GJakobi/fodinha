class Card:
    suits = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
    ranks = ['4', '5', '6', '7', 'Queen', 'Jack', 'King', 'Ace', '2', '3']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        if self.ranks.index(self.rank) != self.ranks.index(other.rank):
            return self.ranks.index(self.rank) < self.ranks.index(other.rank)
        else:
            return self.suits.index(self.suit) < self.suits.index(other.suit)

    @classmethod
    def set_gato(cls, virada):
        virada_index = cls.ranks.index(virada.rank)
        if virada_index == 9:
            cls.ranks.append(cls.ranks.pop(0))
        else:
            cls.ranks.append(cls.ranks.pop(virada_index + 1))
        print(cls.ranks)

    @classmethod
    def reset_gato(cls):
        cls.ranks = ['4', '5', '6', '7', 'Queen', 'Jack', 'King', 'Ace', '2', '3']
        
    @classmethod
    def from_string(cls, card_str):
        rank, suit = card_str.split(" of ")
        return cls(suit, rank)

