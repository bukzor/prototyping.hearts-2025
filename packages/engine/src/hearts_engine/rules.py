"""Hearts game rules and validation."""

from collections.abc import Iterator
from typing import TYPE_CHECKING

from .actions.play import is_first_trick
from .actions.play import valid_plays
from .ending.check_shot_moon import check_shot_moon
from .types import api as T
from .types.api import GameState
from .types.api import Hand
from .types.api import Trick

if TYPE_CHECKING:
    from .state import PlayerAction


def valid_pass_selections(
    hand: Hand,
) -> Iterator[tuple[T.Card, T.Card, T.Card]]:
    """Get all valid 3-card combinations for passing."""
    from itertools import combinations

    for combo in combinations(hand, 3):
        a, b, c = combo
        yield (a, b, c)


def valid_actions(
    phase: T.Phase,
    current_player: T.PlayerId,
    hand: Hand,
    trick: Trick | None,
    first_trick: bool,
    hearts_broken: bool,
    moon_shooter: T.PlayerId | None,
) -> list[PlayerAction]:
    """Get all valid actions for current player."""
    from .state import ChooseMoonOption
    from .state import PlayCard
    from .state import SelectPass

    match phase:
        case T.Phase.PASSING:
            return [SelectPass(cards=c) for c in valid_pass_selections(hand)]
        case T.Phase.PLAYING:
            assert trick is not None
            cards = valid_plays(
                hand, trick.lead_suit, first_trick, hearts_broken
            )
            return [PlayCard(card=c) for c in cards]
        case T.Phase.ROUND_END:
            if moon_shooter == current_player:
                return [
                    ChooseMoonOption(add_to_others=False),
                    ChooseMoonOption(add_to_others=True),
                ]
            return []
        case T.Phase.GAME_END:
            return []


def valid_actions_for_state(state: GameState) -> list[PlayerAction]:
    """Extract args from GameState and call valid_actions."""
    tricks_won = state.tricks_won
    return valid_actions(
        phase=state.phase,
        current_player=state.current_player,
        hand=state.players[state.current_player].hand,
        trick=state.trick,
        first_trick=is_first_trick(tricks_won),
        hearts_broken=state.hearts_broken,
        moon_shooter=check_shot_moon(tricks_won),
    )
