from deck import card_value

# Hand class is used to represent the hand of the Player, dealer or AI player
class Hand:
    def __init__(self):
        self.cards = []
        self.locked = False  # Makes the choice too double down or surrender

    # Adds card to hand
    def add(self, card):
        self.cards.append(card)

    # Makes the best Blackjack total with the ace adjustment
    def total(self):
        t = 0
        aces = 0
        for c in self.cards:
            if c.rank == "A":
                aces += 1
                t += 11
            elif c.rank in ["J", "Q", "K"]:
                t += 10
            else:
                t += int(c.rank)
        while t > 21 and aces:
            t -= 10
            aces -= 1
        return t

    # True if u get 21/blackjack on the first two cards
    def is_blackjack(self):
        return len(self.cards) == 2 and self.total() == 21

    # True if the total goes over 21
    def is_bust(self):
        return self.total() > 21

    # True if two cards can be split
    def can_split(self):
        return len(self.cards) == 2 and card_value(self.cards[0].rank) == card_value(self.cards[1].rank)

    def __repr__(self):
        return f"{[f'{c.rank}-{c.suit[0]}' for c in self.cards]} ({self.total()})"


# Player base class with bets, chips and hand
class Player:
    def __init__(self, name="Player", chips=100):
        self.name = name
        self.hands = [Hand()]
        self.chips = chips
        self.bets = [0]

    # Resets for a new round
    def clear(self):
        self.hands = [Hand()]
        self.bets = [0]

    # Can place a bet
    def place_bet(self, amount, index=0):
        amount = min(amount, self.chips)
        self.bets[index] = amount
        self.chips -= amount #withdraws chips

    # Win outcome
    def win(self, index, multiplier=1):
        self.chips += self.bets[index] + int(self.bets[index] * multiplier)
        self.bets[index] = 0

    # Loss outcome
    def lose(self, index):
        self.bets[index] = 0

    # push/draw outcome
    def push(self, index):
        self.chips += self.bets[index]
        self.bets[index] = 0

    # Asks player for a move
    def decide(self, hand_index):
        while True:
            print(f"\nHand {hand_index+1}: {self.hands[hand_index]}")
            moves = ["(H)it", "(S)tand", "(D)ouble", "Su(r)render"]
            if self.hands[hand_index].can_split() and self.chips >= self.bets[hand_index]:
                moves.append("Sp(l)it")
            print(" | ".join(moves))
            c = input("Choice: ").lower()
            if c in ("h", "hit"):
                return "hit"
            if c in ("s", "stand"):
                return "stand"
            if c in ("d", "double"):
                return "double"
            if c in ("r", "surrender"):
                return "surrender"
            if c in ("l", "split") and self.hands[hand_index].can_split():
                return "split"
