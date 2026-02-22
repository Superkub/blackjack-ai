import random
from collections import namedtuple, Counter

# Represents a playing card with a rank and suit
Card = namedtuple("Card", ["rank", "suit"])

# Standard ranks and suits for a deck of cards
RANKS = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Will shot cards as values in blackjack, like picture cards will be valued at 10 and Ace will be 1 or 11 depending on the hand
def card_value(rank):
    if rank in ["J", "Q", "K"]:
        return 10
    if rank == "A":
        return 11
    return int(rank)

# Deck class will manage cards, drawing and shuffling
class Deck:
    def __init__(self, decks=1):
        self.decks = decks
        self.reset()

    # Shuffles the deck
    def reset(self):
        self.cards = [
            Card(rank, suit)
            for _ in range(self.decks)
            for suit in SUITS
            for rank in RANKS
        ]
        random.shuffle(self.cards)

    # This will draw a card and shuffle if the deck is empty
    def draw(self):
        if not self.cards:
            self.reset()
        return self.cards.pop()

    # Will show the remaining count of cards
    def distribution(self):
        return Counter(card.rank for card in self.cards)

    def __len__(self):
        return len(self.cards)
