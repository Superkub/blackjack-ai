from player import Player

# Dealer class follows the game rules
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer", chips=0)

    def decide(self):
        return "hit" if self.hands[0].total() < 17 else "stand"
