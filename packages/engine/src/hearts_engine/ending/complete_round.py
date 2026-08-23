"""Complete a round and score it."""

import dataclasses
from random import Random

from ..types import api as T
from ..types.api import GameState
from .check_game_end import check_game_end
from .check_shot_moon import check_shot_moon
from .scoring import apply_normal_scoring


def complete_round(state: GameState, random: Random) -> GameState:
    """Complete a round and score it."""
    shooter = check_shot_moon(state.tricks_won)
    if shooter is not None:
        return dataclasses.replace(
            state, phase=T.Phase.ROUND_END, current_player=shooter
        )

    state = dataclasses.replace(
        state, players=apply_normal_scoring(state.players)
    )
    return check_game_end(state, random)
