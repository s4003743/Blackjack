
class Player():
    def __init__(self, wealth) -> None:
        self.wealth = wealth
        self.hands = []

    def place_bet(self, amount):
        self.wealth -= amount

    def resolve_hand(self, dealer_score, dealer_hand):
        for idx, hand in enumerate(self.hands):

            player_score = hand.value()

            print(f"\nResult for Hand {idx+1}:")
            print(f"Player: {player_score} | Dealer: {dealer_score}")

            if len(hand.cards) == 2 and player_score == 21 and dealer_score != 21:
                self.wealth += int(hand.bet * 2.5)
                print("Blackjack!")
                continue

            if hand.is_busted():
                print("Lose")
            elif dealer_hand.is_busted():
                self.wealth += hand.bet * 2
                print("Win")
            elif player_score > dealer_score:
                self.wealth += hand.bet * 2
                print("Win")
            elif player_score < dealer_score:
                print("Lose")
            else:
                self.wealth += hand.bet
                print("Push")