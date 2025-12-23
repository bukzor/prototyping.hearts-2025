"""Create a new game."""

import uuid
from random import Random

from ..types import api as T
from ..types.api import GameState
from ..types.api import PlayerState
from .deal_hands import deal_hands
from .Deck import Deck


def new_game(random: Random, game_id: str | None = None) -> GameState:
    """Create a new game with shuffled deck."""
    players = tuple(PlayerState(hand=h) for h in deal_hands(Deck(), random))

    return GameState(
        game_id=game_id or str(uuid.uuid4()),
        phase=T.Phase.PASSING,
        round_number=0,
        dealer=0,
        players=players,
        trick=None,
        current_player=0,  # Start with player 0 for passing
        hearts_broken=False,
        pending_passes=(None, None, None, None),
    )
