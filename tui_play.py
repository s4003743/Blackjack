from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Vertical
from game import BlackjackGame


def render_cards(cards):

    lines = ["", "", ""]

    for card in cards:

        rank = card[0]
        suit = card[1]

        lines[0] += "┌─────┐ "
        lines[1] += f"| {rank}{suit}  | "
        lines[2] += "└─────┘ "

    return "\n".join(lines)


class BlackjackUI(App):

    CSS = """
    Screen {
        background: darkgreen;
        align: center middle;
    }

    Button {
        margin: 1;
        width: 20;
    }

    Static {
        text-align: center;
    }
    """

    def __init__(self):

        super().__init__()

        self.game = BlackjackGame()

    def compose(self) -> ComposeResult:

        yield Vertical(

            Static(id="count"),
            Static(id="dealer"),
            Static(id="player"),
            Static(id="wealth"),

            Button("Hit", id="hit"),
            Button("Stand", id="stand"),
            Button("New Round", id="new"),
        )

    def on_mount(self):

        self.game.start_round()

        self.refresh_ui()

    def refresh_ui(self):

        dealer = self.query_one("#dealer", Static)
        player = self.query_one("#player", Static)
        wealth = self.query_one("#wealth", Static)
        count = self.query_one("#count", Static)

        dealer.update(
            f"\nDealer\n{render_cards(self.game.dealer_hand.cards)}"
        )

        player.update(
            f"\nPlayer\n{render_cards(self.game.player.hands[0].cards)}"
        )

        wealth.update(
            f"\nWealth: ${self.game.player.wealth}"
        )

        count.update(
            f"True Count: {self.game.comp.count_cards():.1f}"
        )

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "hit":

            self.game.hit()

        elif event.button.id == "stand":

            self.game.stand()

        elif event.button.id == "new":

            self.game.start_round()

        self.refresh_ui()


if __name__ == "__main__":
    BlackjackUI().run()