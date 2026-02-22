from blackjack import Game

def main():
    g = Game()
    while True:
        print("""
1. Play
2. AI simulation
3. Plot AI results
4. Quit
""")
        c = input("Choice: ")
        if c == "1":
            g.play_interactive()
        elif c == "2":
            n = input("Amount of rounds: ")
            n = int(n) if n.isdigit() else 100
            df = g.simulate_ai(n)
            print(df["result"].value_counts(normalize=True))
        elif c == "3":
            g.plot_ai()
        elif c == "4":
            break

if __name__ == "__main__":
    main()