"""Transition to playing phase."""

import dataclasses

from ..types import api as T
from ..types.api import GameState
from ..types.api import Trick


def start_playing_phase(state: GameState, leader: T.PlayerId) -> GameState:
    """Transition to playing phase."""
    return dataclasses.replace(
        state,
        phase=T.Phase.PLAYING,
        trick=Trick(lead=leader),
        current_player=leader,
    )
