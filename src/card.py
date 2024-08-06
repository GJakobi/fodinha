class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['4', '5', '6', '7', 'Queen', 'Jack', 'King', 'Ace', '2', '3']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        return self.ranks.index(self.rank) < self.ranks.index(other.rank)

    def calculate_value(self):
        value = (self.suits.index(self.suit) + 1) * (self.ranks.index(self.rank) + 1)
        return value

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

