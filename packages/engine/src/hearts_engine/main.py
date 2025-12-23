"""Hearts game engine - entry points."""

from random import Random
from typing import TYPE_CHECKING

from .state import ChooseMoonOption
from .state import PlayCard
from .state import SelectPass
from .types import api as T
from .types.api import GameState

if TYPE_CHECKING:
    from .state import PlayerAction


def apply_action(
    state: GameState, action: PlayerAction, random: Random
) -> T.ActionResult:
    """Apply an action to the game state."""
    from .passing.api import apply_pass
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
