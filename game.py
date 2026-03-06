from collections import deque
import random
from player import Player
from comp import Comp
from play import Hand

PLAYER_WEALTH = 10**4
BET_SIZE = 10**2


def generate_deck(num_decks=6):
    deck_vals = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['♥️', '♠️', '♦️', '♣️']

    deck = [v+s for v in deck_vals for s in suits] * num_decks
    random.shuffle(deck)
    return deck


class BlackjackGame:

    def __init__(self):
        self.deck = deque(generate_deck())
        self.player = Player(PLAYER_WEALTH)
        self.comp = Comp(len(self.deck)//52)

        self.dealer_hand = Hand(0)
        self.current_hand = 0

    def start_round(self):

        self.player.hands = [Hand(BET_SIZE)]
        self.player.place_bet(BET_SIZE)

        self.dealer_hand = Hand(0)

        for _ in range(2):
            self.player.hands[0].add_card(self.deck)
            self.dealer_hand.add_card(self.deck)

        self.current_hand = 0

    def hit(self):

        hand = self.player.hands[self.current_hand]
        hand.add_card(self.deck)

        if hand.is_busted():
            self.next_hand()

    def stand(self):
        self.next_hand()

    def next_hand(self):

        self.current_hand += 1

        if self.current_hand >= len(self.player.hands):
            self.dealer_turn()

    def dealer_turn(self):

        while self.dealer_hand.value() < 17:
            self.dealer_hand.add_card(self.deck)

        dealer_score = self.dealer_hand.value()
        self.player.resolve_hand(dealer_score, self.dealer_hand)

        self.record_cards()

    def record_cards(self):

        for card in self.dealer_hand.cards:
            self.comp.cards_seen.append(card[0])

        for hand in self.player.hands:
            for card in hand.cards:
                self.comp.cards_seen.append(card[0])