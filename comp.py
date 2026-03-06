
card_cat = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    'T': -1, 'J': -1, 'Q': -1, 'K': -1, 'A' : -1
}

class Comp():
    def __init__(self, num_decks) -> None:
        self.cards_seen = []
        self.num_decks = num_decks

    def count_cards(self):

        running_count = sum(card_cat[c] for c in self.cards_seen)
        decks_remaining = self.num_decks - (len(self.cards_seen) / 52)

        if decks_remaining <= 0:
            return running_count

        return running_count / decks_remaining
        
    def suggest_action(self):
        true_count = self.count_cards()

        if true_count > 1:
            print(f"Deck is in your favour ({true_count:.2f}).")
        elif true_count < -1:
            print(f"Deck is NOT in your favour ({true_count:.2f}).")
        else:
            print("No significant edge.")
