# ui.py
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Horizontal, Vertical
from game import BlackjackGame
import asyncio

def render_cards(cards, hide_second=False):
    """Render ASCII cards"""
    lines = ["", "", "", "", ""]
    for i, c in enumerate(cards):
        rank, suit = c[0], c[1]
        if hide_second and i == 1:
            r = '?'
            s = '?'
        else:
            r = rank
            s = suit
        lines[0] += "┌───────┐ "
        lines[1] += f"│{r:<2}     │ "
        lines[2] += f"│   {s}   │ "
        lines[3] += f"│     {r:>2}│ "
        lines[4] += "└───────┘ "
    return "\n".join(lines)

class BlackjackUI(App):
    CSS = """
    Screen {
        background: darkgreen;
        align: center middle;
    }
    Button {
        margin: 1;
        width: 14;
    }
    Static {
        text-align: center;
    }
    """

    def __init__(self):
        super().__init__()
        self.game = BlackjackGame()
        self.current_hand = 0

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(id="count"),
            Static(id="dealer"),
            Static(id="player"),
            Static(id="wealth"),
            Horizontal(
                Button("Hit", id="hit"),
                Button("Stand", id="stand"),
                Button("Double", id="double"),
                Button("New Round", id="new"),
            )
        )

    def on_mount(self):
        self.game.start_round()
        self.refresh_ui()

    def refresh_ui(self):
        dealer = self.query_one("#dealer", Static)
        player = self.query_one("#player", Static)
        wealth = self.query_one("#wealth", Static)
        count = self.query_one("#count", Static)

        hide = self.game.round_active
        dealer.update(f"Dealer\n{render_cards(self.game.dealer_hand.cards, hide_second=hide)}")

        player_str = ""
        for i, hand in enumerate(self.game.player.hands):
            player_str += f"Hand {i+1} (bet ${hand.bet})\n"
            player_str += f"{render_cards(hand.cards)}\n"
        player.update(player_str)

        wealth.update(f"Wealth: ${self.game.player.wealth}")
        count.update(f"True Count: {self.game.comp.count_cards():.1f}")

    async def deal_animation(self, hand_idx=0):
        """Animate a hit for a hand"""
        self.game.hit(hand_idx)
        self.refresh_ui()
        await asyncio.sleep(0.2)

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "hit":
            await self.deal_animation(self.current_hand)
        elif event.button.id == "stand":
            self.game.stand()
        elif event.button.id == "double":
            self.game.double(self.current_hand)
        elif event.button.id == "new":
            self.game.start_round()
            self.current_hand = 0
        self.refresh_ui()

if __name__ == "__main__":
    BlackjackUI().run()