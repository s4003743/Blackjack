# game.py
import random
from collections import deque
from player import Player
from comp import Comp

PLAYER_WEALTH = 10000
BET_SIZE = 100
NUM_DECKS = 6

card_vals = {
    '2':2,'3':2,'4':4,'5':5,'6':6,
    '7':7,'8':8,'9':9,
    'T':10,'J':10,'Q':10,'K':10
}

def generate_deck(num_decks=NUM_DECKS):
    vals = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['♥','♠','♦','♣']
    deck = [v+s for v in vals for s in suits] * num_decks
    random.shuffle(deck)
    return deque(deck)

class Hand:
    def __init__(self, bet):
        self.cards=[]
        self.bet=bet
        self.doubled_down = False

    def add_card(self, deck, comp):
        card = deck.pop()
        self.cards.append(card)

    def value(self):
        total=0
        aces=0
        for c in self.cards:
            r=c[0]
            if r=='A':
                total+=11
                aces+=1
            else:
                total+=card_vals.get(r,10)
        while total>21 and aces>0:
            total-=10
            aces-=1
        return total

    def is_busted(self):
        return self.value()>21

    def can_split(self):
        return len(self.cards)==2 and self.cards[0][0]==self.cards[1][0]

    def __str__(self):
        return f"{self.cards} ({self.value()})"

class BlackjackGame:
    def __init__(self):
        self.deck = generate_deck()
        self.player = Player(PLAYER_WEALTH)
        self.comp = Comp(len(self.deck)//52)
        self.dealer_hand = Hand(0)
        self.round_active = True

    def start_round(self):
        if len(self.deck)<52:
            self.deck=generate_deck()
            self.comp=Comp(len(self.deck)//52)

        self.player.hands = [Hand(BET_SIZE)]
        self.player.place_bet(BET_SIZE)
        self.dealer_hand = Hand(0)
        self.round_active = True

        for _ in range(2):
            self.player.hands[0].add_card(self.deck, self.comp)
            self.dealer_hand.add_card(self.deck, self.comp)

    def hit(self, hand_idx=0):
        hand = self.player.hands[hand_idx]
        if not hand.is_busted():
            hand.add_card(self.deck, self.comp)

    def stand(self):
        self.round_active = False
        while self.dealer_hand.value() < 17:
            self.dealer_hand.add_card(self.deck, self.comp)
        dealer_score = self.dealer_hand.value()
        self.player.resolve_hand(dealer_score, self.dealer_hand)

    def double(self, hand_idx=0):
        hand = self.player.hands[hand_idx]
        if len(hand.cards)==2:
            self.player.place_bet(hand.bet)
            hand.bet *=2
            hand.doubled_down = True
            hand.add_card(self.deck, self.comp)
            self.stand()