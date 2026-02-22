import pandas as pd
import matplotlib.pyplot as plt

from deck import Deck, card_value
from player import Hand, Player
from dealer import Dealer
from ai_player import AIPlayer


def probability_bust(hand, deck):
    t = hand.total()
    dist = deck.distribution()
    total_cards = len(deck)
    if total_cards == 0:
        return 0.0
    bust = 0
    for rank, count in dist.items():
        v = card_value(rank)
        if rank == "A":
            if t + 11 > 21 and t + 1 <= 21:
                continue
            busting = (t + 11 > 21)
        else:
            busting = (t + v > 21)
        if busting:
            bust += count
    return bust / total_cards


class Game:
    def __init__(self):
        self.deck = Deck(4)
        self.player = Player()
        self.dealer = Dealer()
        self.ai = AIPlayer()
        self.history = []

    def deal_initial(self, P, D):
        P.clear()
        D.clear()
        for _ in range(2):
            P.hands[0].add(self.deck.draw())
            D.hands[0].add(self.deck.draw())

    def settle(self, P, D, index):
        pt = P.hands[index].total()
        dt = D.hands[0].total()

        if P.hands[index].is_blackjack() and not D.hands[0].is_blackjack():
            P.win(index, 1.5)
        elif D.hands[0].is_blackjack() and not P.hands[index].is_blackjack():
            P.lose(index)
        elif P.hands[index].is_bust():
            P.lose(index)
        elif D.hands[0].is_bust():
            P.win(index)
        elif pt > dt:
            P.win(index)
        elif dt > pt:
            P.lose(index)
        else:
            P.push(index)

    def play_interactive(self):
        print("\n=== New game ===")
        self.deal_initial(self.player, self.dealer)

        # Ask for bet
        while True:
            print(f"You have {self.player.chips} chips.")
            bet_input = input("How much would you like to bet? ")

            if not bet_input.isdigit():
                print("Enter a number.")
                continue

            amount = int(bet_input)

            if amount <= 0:
                print("Bet must be greater than 0.")
                continue
            if amount > self.player.chips:
                print("You don't have enough chips.")
                continue

            self.player.place_bet(amount)
            break

        # Player actions
        for i in range(len(self.player.hands)):
            while True:
                print(f"\nDealer has: {self.dealer.hands[0].cards[0]}")
                print(f"Chance for bust: {probability_bust(self.player.hands[i], self.deck):.2%}")

                move = self.player.decide(i)

                if move == "hit":
                    self.player.hands[i].add(self.deck.draw())
                    if self.player.hands[i].is_bust():
                        break

                elif move == "stand":
                    break

                elif move == "double":
                    if self.player.chips >= self.player.bets[i]:
                        self.player.place_bet(self.player.bets[i], index=i)
                        self.player.hands[i].add(self.deck.draw())
                    else:
                        print("not enough chips to double")
                    break

                elif move == "surrender":
                    refund = self.player.bets[i] // 2
                    self.player.chips += refund
                    self.player.bets[i] = 0
                    print(f"surrender hand {i+1} get back {refund} chips.")
                    break

                elif move == "split":
                    hand = self.player.hands[i]

                    if hand.can_split() and self.player.chips >= self.player.bets[i]:
                        second_card = hand.cards.pop()
                        new_hand = Hand()
                        new_hand.add(second_card)

                        self.player.hands.append(new_hand)

                        # new bet equals the original bet
                        self.player.bets.append(0)
                        self.player.place_bet(self.player.bets[i], index=len(self.player.hands) - 1)

                        hand.add(self.deck.draw())
                        new_hand.add(self.deck.draw())

                        print(f"split hand {i+1}.")
                    else:
                        print("can't split hand")

        # Dealer turn
        print("\nDealer plays...")
        print("Dealer hand:", self.dealer.hands[0])
        while self.dealer.decide() == "hit":
            self.dealer.hands[0].add(self.deck.draw())
            print("Dealer withdraws ->", self.dealer.hands[0])

        # Settle all player hands
        for i in range(len(self.player.hands)):
            if self.player.bets[i] == 0:
                continue
            self.settle(self.player, self.dealer, i)

        print("\nround over.")
        print("Finally dealer-hand:", self.dealer.hands[0])
        for i, h in enumerate(self.player.hands):
            print(f"player hand {i+1}: {h}")
        print("player chips:", self.player.chips)

    def simulate_ai(self, rounds=100):
        self.history = []
        self.ai.chips = 100

        for r in range(1, rounds + 1):
            self.deal_initial(self.ai, self.dealer)

            bet = 10
            if self.ai.chips < bet:
                bet = self.ai.chips
            self.ai.place_bet(bet)

            while True:
                if self.ai.hands[0].is_blackjack():
                    break
                move = self.ai.decide(0)
                if move == "hit":
                    self.ai.hands[0].add(self.deck.draw())
                    if self.ai.hands[0].is_bust():
                        break
                else:
                    break

            while self.dealer.decide() == "hit":
                self.dealer.hands[0].add(self.deck.draw())

            before = self.ai.chips
            self.settle(self.ai, self.dealer, 0)
            after = self.ai.chips

            if after > before:
                result = "win"
            elif after < before:
                result = "loss"
            else:
                result = "push"

            self.history.append(
                {"round": r, "result": result, "chips": self.ai.chips}
            )

        df = pd.DataFrame(self.history)
        df.to_pickle("ai_history.pkl")
        return df

    def plot_ai(self):
        try:
            df = pd.read_pickle("ai_history.pkl")
        except FileNotFoundError:
            if not self.history:
                print("No AI Data. Run AI-simulation (menu choice 2).")
                return
            df = pd.DataFrame(self.history)

        result_counts = df["result"].value_counts()

        plt.figure()
        result_counts.plot(kind="bar")
        plt.title("AI vs dealer – splitting results")
        plt.xlabel("Result")
        plt.ylabel("amount of rounds")

        plt.figure()
        plt.plot(df["round"], df["chips"])
        plt.title("AI-chips over time")
        plt.xlabel("Rounds")
        plt.ylabel("Chips")

        plt.show()