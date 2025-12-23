"""Apply a pass selection."""

import dataclasses

from ..start.api import find_two_of_clubs_holder
from ..start.api import start_playing_phase
from ..types import api as T
from ..types.api import GameState
from .execute_passes import execute_passes
from .next_player_for_passing import next_player_for_passing
from .pass_direction_for_round import pass_direction_for_round
from .update_pending_passes import update_pending_passes


def apply_pass(
    state: GameState, cards: tuple[T.Card, T.Card, T.Card]
) -> T.ActionResult:
    """Apply a pass selection."""
    if state.phase != T.Phase.PASSING:
        return T.ActionFailure(error="Not in passing phase")

    if pass_direction_for_round(state.round_number) == T.PassDirection.HOLD:
        return T.ActionFailure(error="Hold round, no passing")

    player = state.current_player
    hand = state.players[player].hand

    if not all(c in hand for c in cards):
        return T.ActionFailure(error="Cards not in hand")

    if len(set(cards)) != 3:
        return T.ActionFailure(error="Must select 3 different cards")

    pending = update_pending_passes(state.pending_passes, player, cards)
    state = dataclasses.replace(state, pending_passes=pending)

    if all(p is not None for p in state.pending_passes):
        state = execute_passes(state)
        leader = find_two_of_clubs_holder(state.hands)
        state = start_playing_phase(state, leader)
    else:
        state = dataclasses.replace(
            state,
            current_player=next_player_for_passing(
                player, state.pending_passes
            ),
        )

    return T.ActionSuccess(new_state=state)
