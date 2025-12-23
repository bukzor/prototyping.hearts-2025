"""Start a new round."""

import dataclasses
from random import Random

from ..state import update_player
from ..types import api as T
from ..types.api import GameState
from ..types.api import Trick
from .deal_hands import deal_hands
from .Deck import Deck
from .find_two_of_clubs_holder import find_two_of_clubs_holder


def start_new_round(state: GameState, random: Random) -> GameState:
    """Start a new round."""
    from ..passing.api import pass_direction_for_round

    round_number = state.round_number + 1
    dealer = T.player_id(state.dealer + 1)

    players = state.players
    for pid, hand in zip(T.PLAYER_IDS, deal_hands(Deck(), random)):
        players = update_player(
            players, pid, hand=hand, round_score=0, tricks_won=()
        )

    # Determine phase and starting player
    direction = pass_direction_for_round(round_number)
    trick: Trick | None
    if direction == T.PassDirection.HOLD:
        phase = T.Phase.PLAYING
        leader = find_two_of_clubs_holder(tuple(p.hand for p in players))
        trick = Trick(lead=leader)
        current_player = leader
    else:
        phase = T.Phase.PASSING
        trick = None
        current_player: T.PlayerId = 0

    return dataclasses.replace(
        state,
        round_number=round_number,
        dealer=dealer,
        players=players,
        trick=trick,
        current_player=current_player,
        hearts_broken=False,
        pending_passes=(None, None, None, None),
        phase=phase,
    )
