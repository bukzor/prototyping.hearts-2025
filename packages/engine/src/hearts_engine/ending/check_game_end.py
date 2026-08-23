"""Check if game should end."""

import dataclasses
from random import Random

from ..start.api import start_new_round
from ..types import api as T
from ..types.api import GameState

LOSING_SCORE = 100


def check_game_end(state: GameState, random: Random) -> GameState:
    """Check if game should end."""
    if any(p.score >= LOSING_SCORE for p in state.players):
        return dataclasses.replace(state, phase=T.Phase.GAME_END)
    return start_new_round(state, random)
