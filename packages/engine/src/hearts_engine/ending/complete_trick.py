"""Complete a trick and determine winner."""

import dataclasses
from random import Random

from ..state import update_player
from ..types.api import GameState
from ..types.api import Trick
from .complete_round import complete_round
from .trick_winner import trick_winner


def complete_trick(state: GameState, random: Random) -> GameState:
    """Complete a trick and determine winner."""
    assert state.trick is not None
    winner = trick_winner(state.trick)
    state = dataclasses.replace(
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
        state = complete_round(state, random)

    return state
