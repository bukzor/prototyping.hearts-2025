"""Hearts game engine - playing phase."""

from hearts_engine.card import Card
from hearts_engine.card import Play
from hearts_engine.card import Suit
from hearts_engine.engine.main import ActionResult
from hearts_engine.rules import trick_winner
from hearts_engine.rules import valid_plays
from hearts_engine.state import GameState
from hearts_engine.state import Phase


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
    new_state.trick.append(Play(player=player, card=card))

    if card.suit == Suit.HEARTS:
        new_state.hearts_broken = True

    if len(new_state.trick) == 4:
        complete_trick(new_state)
    else:
        new_state.current_player = (player + 1) % 4  # type: ignore[assignment]

    return ActionResult(ok=True, error=None, new_state=new_state)


def complete_trick(state: GameState) -> None:
    """Complete a trick and determine winner."""
    from hearts_engine.engine.round import complete_round

    winner = trick_winner(state.trick)
    cards_won = [p.card for p in state.trick]
    state.tricks_won[winner.player].append(cards_won)
    state.trick = []
    state.lead_player = winner.player
    state.current_player = winner.player

    if all(len(h) == 0 for h in state.hands):
        complete_round(state)
