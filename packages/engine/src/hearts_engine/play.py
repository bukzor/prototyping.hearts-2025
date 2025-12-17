"""Hearts game engine - playing phase."""

from .card import Card
from .card import Suit
from .card import Trick
from .main import ActionResult
from .rules import trick_winner
from .rules import valid_plays
from .state import GameState
from .state import Phase


def apply_play(state: GameState, card: Card) -> ActionResult:
    """Apply a card play."""
    if state.phase != Phase.PLAYING:
        return ActionResult(
            ok=False, error="Not in playing phase", new_state=None
        )

    player = state.current_player
    hand = state.hands[player]

    if card not in hand:
        return ActionResult(ok=False, error="Card not in hand", new_state=None)

    valid = valid_plays(state)
    if card not in valid:
        return ActionResult(
            ok=False, error=f"Invalid play: {card}", new_state=None
        )

    new_state = state.copy()
    new_state.hands[player].remove(card)
    new_state.trick[player] = card

    if card.suit == Suit.HEARTS:
        new_state.hearts_broken = True

    if len(new_state.trick) == 4:
        complete_trick(new_state)
    else:
        new_state.current_player = (player + 1) % 4  # type: ignore[assignment]

    return ActionResult(ok=True, error=None, new_state=new_state)


def complete_trick(state: GameState) -> None:
    """Complete a trick and determine winner."""
    from .round import complete_round

    winner = trick_winner(state.trick, state.lead_player)
    state.tricks_won[winner].append(state.trick)
    state.trick = Trick()
    state.lead_player = winner
    state.current_player = winner

    if all(len(h) == 0 for h in state.hands):
        complete_round(state)
