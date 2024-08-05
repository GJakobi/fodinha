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

    def set_gato(self, gato_index):
        self.ranks.append(self.ranks.pop(gato_index))
        print(self.ranks)
        
    # function to calculate the value of the card, based on its suit and rank
    # the index of the suit in the suits list is multiplied by the index of the rank in the ranks list.
    def calculate_value(self):
        value = (self.suits.index(self.suit) + 1) * (self.ranks.index(self.rank) + 1)
        return value
        
    @classmethod
    def from_string(cls, card_str):
        rank, suit = card_str.split(" of ")
        return cls(suit, rank)
