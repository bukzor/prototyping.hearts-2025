"""Hearts game engine - entry points."""

import uuid
from random import Random
from typing import TYPE_CHECKING

from .cards import Deck
from .state import ChooseMoonOption
from .state import GameState
from .state import Phase
from .state import PlayCard
from .state import PlayerState
from .state import SelectPass
from .types import ActionResult

if TYPE_CHECKING:
    from .state import PlayerAction


def new_game(random: Random, game_id: str | None = None) -> GameState:
    """Create a new game with shuffled deck."""
    players = tuple(PlayerState(hand=h) for h in Deck().deal_hands(random))

    return GameState(
        game_id=game_id or str(uuid.uuid4()),
        phase=Phase.PASSING,
        round_number=0,
        dealer=0,
        players=players,
        trick=None,
        current_player=0,  # Start with player 0 for passing
        hearts_broken=False,
        pending_passes=(None, None, None, None),
    )


def apply_action(
    state: GameState, action: PlayerAction, random: Random
) -> ActionResult:
    """Apply an action to the game state."""
    from .passing import apply_pass
    from .play import apply_play
    from .round import apply_moon_choice

    match action:
        case SelectPass(cards=cards):
            return apply_pass(state, cards)
        case PlayCard(card=card):
            return apply_play(state, card, random)
        case ChooseMoonOption(add_to_others=add_to_others):
            return apply_moon_choice(state, add_to_others, random)
        case _:
            raise AssertionError(action)
