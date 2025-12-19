"""Hearts game engine - playing phase."""

from dataclasses import replace

from .card import Card
from .card import Suit
from .card import Trick
from .cards import Hand
from .main import ActionResult
from .rules import is_first_trick
from .rules import trick_winner
from .rules import valid_plays
from .state import GameState
from .state import Phase
from .state import update_player


def apply_play(state: GameState, card: Card) -> ActionResult:
    """Apply a card play."""
    if state.phase != Phase.PLAYING:
        return ActionResult(
            ok=False, error="Not in playing phase", new_state=None
        )
    assert state.trick is not None

    player = state.current_player
    hand = state.players[player].hand

    if card not in hand:
        return ActionResult(ok=False, error="Card not in hand", new_state=None)

    is_first = is_first_trick(state.players)
    if card not in valid_plays(
        hand, state.trick, is_first, state.hearts_broken
    ):
        return ActionResult(
            ok=False, error=f"Invalid play: {card}", new_state=None
        )

    trick = state.trick.with_play(player, card)
    state = replace(
        state,
        players=update_player(state.players, player, hand=Hand(hand - {card})),
        trick=trick,
        hearts_broken=state.hearts_broken or card.suit == Suit.HEARTS,
    )

    if len(trick) == 4:
        state = complete_trick(state)
    else:
        state = replace(state, current_player=(player + 1) % 4)  # type: ignore[arg-type]

    return ActionResult(ok=True, error=None, new_state=state)


def complete_trick(state: GameState) -> GameState:
    """Complete a trick and determine winner."""
    from .round import complete_round

    assert state.trick is not None
    winner = trick_winner(state.trick)
    state = replace(
        state,
        players=update_player(
            state.players,
            winner,
            tricks_won=(*state.players[winner].tricks_won, state.trick),
        ),
        trick=Trick(lead=winner),
        current_player=winner,
    )

    if all(len(p.hand) == 0 for p in state.players):
        state = complete_round(state)

    return state
