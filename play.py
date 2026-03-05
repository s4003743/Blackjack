import random
import time
from collections import deque
from rich import print


PLAYER_WEALTH = 10**4
BET_SIZE = 10**2

card_vals = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 10, 'Q': 10, 'K': 10
}


def generate_deck(num_decks=6):
    deck_vals = ['2', '3', '4', '5', '6', '7',
                 '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['♥️', '♠️', '♦️', '♣️']

    deck = [v + s for v in deck_vals for s in suits] * num_decks
    random.shuffle(deck)
    return deck


# -------------------------
# Hand Class
# -------------------------

class Hand:
    def __init__(self, bet):
        self.cards = []
        self.bet = bet

    def add_card(self, deck):
        self.cards.append(deck.pop())

    def value(self):
        total = 0
        aces = 0

        for card in self.cards:
            rank = card[0]

            if rank == 'A':
                total += 11
                aces += 1
            else:
                total += card_vals.get(rank, 10)

        # Convert aces from 11 to 1 if needed
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_busted(self):
        return self.value() > 21

    def can_split(self):
        return (
            len(self.cards) == 2 and
            self.cards[0][0] == self.cards[1][0]
        )

    def __str__(self):
        return f"{self.cards} ({self.value()})"


# -------------------------
# Game Logic
# -------------------------

def play():
    deck = deque(generate_deck())

    while len(deck) > 52:

        print("\n--- NEW GAME ---\n")

        # Create player + dealer hands
        player_hands = [Hand(BET_SIZE)]
        dealer_hand = Hand(0)

        # Initial deal
        for _ in range(2):
            player_hands[0].add_card(deck)
            dealer_hand.add_card(deck)

        print(f"Dealer showing: {dealer_hand.cards[0]}")

        # -------------------------
        # Handle Splits
        # -------------------------

        i = 0
        while i < len(player_hands):

            hand = player_hands[i]

            # Offer split if possible
            if hand.can_split():
                print(f"\nHand {i+1}: {hand}")
                split = input("Split? (y/n): ").lower()

                if split == 'y':
                    new_hand = Hand(BET_SIZE)

                    # Move second card to new hand
                    new_hand.cards.append(hand.cards.pop())

                    # Each hand gets one new card
                    hand.add_card(deck)
                    new_hand.add_card(deck)

                    player_hands.append(new_hand)

                    continue  # re-evaluate this hand

            i += 1

        # -------------------------
        # Play Each Player Hand
        # -------------------------

        for idx, hand in enumerate(player_hands):

            print(f"\n--- Playing Hand {idx+1} ---")

            while not hand.is_busted():

                print(hand)
                move = input("Hit or Stand (h/s): ").lower()

                if move == 'h':
                    hand.add_card(deck)
                else:
                    break

            if hand.is_busted():
                print("Busted!")

        # -------------------------
        # Dealer Plays
        # -------------------------

        print(f"\nDealer hand: {dealer_hand}")

        while dealer_hand.value() < 17:
            dealer_hand.add_card(deck)
            print(f"Dealer hits: {dealer_hand}")
            time.sleep(1)

        if dealer_hand.is_busted():
            print("Dealer busted!")

        dealer_score = dealer_hand.value()

        # -------------------------
        # Resolve Hands
        # -------------------------

        for idx, hand in enumerate(player_hands):

            player_score = hand.value()

            print(f"\nResult for Hand {idx+1}:")
            print(f"Player: {player_score} | Dealer: {dealer_score}")

            if hand.is_busted():
                print("Lose")
            elif dealer_hand.is_busted():
                print("Win")
            elif player_score > dealer_score:
                print("Win")
            elif player_score < dealer_score:
                print("Lose")
            else:
                print("Push")


if __name__ == "__main__":
    play()