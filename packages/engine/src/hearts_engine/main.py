"""Hearts game engine - entry points."""

import random
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .card import Trick
from .cards import Deck
from .state import ChooseMoonOption
from .state import GameState
from .state import Phase
from .state import PlayCard
from .state import PlayerState
from .state import SelectPass

if TYPE_CHECKING:
    from .state import PlayerAction


@dataclass(frozen=True, slots=True)
class ActionResult:
    """Result of applying an action."""

    ok: bool
    error: str | None
    new_state: GameState | None


def new_game(game_id: str | None = None, seed: int | None = None) -> GameState:
    """Create a new game with shuffled deck."""
    rng = random.Random(seed)
    hands = Deck().deal_hands(rng)

    return GameState(
        game_id=game_id or str(uuid.uuid4()),
        phase=Phase.PASSING,
        round_number=0,
        dealer=0,
        players=[PlayerState(hand=h) for h in hands],
        trick=Trick(),
        lead_player=None,
        current_player=0,  # Start with player 0 for passing
        hearts_broken=False,
        pending_passes={},
    )


def apply_action(state: GameState, action: PlayerAction) -> ActionResult:
    """Apply an action to the game state."""
    from .passing import apply_pass
    from .play import apply_play
    from .round import apply_moon_choice

    match action:
        case SelectPass(cards=cards):
            return apply_pass(state, cards)
        case PlayCard(card=card):
            return apply_play(state, card)
        case ChooseMoonOption(add_to_others=add_to_others):
            return apply_moon_choice(state, add_to_others)
