from player import Player

# AI Player strategy will be to hit on everything except over 17
class AIPlayer(Player):
    def __init__(self, chips=100):
        super().__init__("AI", chips)

    def decide(self, hand_index):
        return "hit" if self.hands[hand_index].total() < 17 else "stand"
