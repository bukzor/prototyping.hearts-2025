"""Hearts game engine - entry points."""

import random
import uuid
from dataclasses import dataclass

from hearts_engine.cards import create_deck
from hearts_engine.state import ChooseMoonOption
from hearts_engine.state import GameState
from hearts_engine.state import Phase
from hearts_engine.state import PlayCard
from hearts_engine.state import PlayerAction
from hearts_engine.state import SelectPass
from hearts_engine.state import hands_from_deck


@dataclass(frozen=True, slots=True)
class ActionResult:
    """Result of applying an action."""

    ok: bool
    error: str | None
    new_state: GameState | None


def new_game(game_id: str | None = None, seed: int | None = None) -> GameState:
    """Create a new game with shuffled deck."""
    rng = random.Random(seed)
    deck = create_deck()
    rng.shuffle(deck)
    hands = hands_from_deck(deck)

    return GameState(
        game_id=game_id or str(uuid.uuid4()),
        phase=Phase.PASSING,
        round_number=0,
        dealer=0,
        hands=hands,
        scores=[0, 0, 0, 0],
        round_scores=[0, 0, 0, 0],
        tricks_won=[[], [], [], []],
        trick=[],
        lead_player=None,
        current_player=0,  # Start with player 0 for passing
        hearts_broken=False,
        pending_passes={},
    )


def apply_action(state: GameState, action: PlayerAction) -> ActionResult:
    """Apply an action to the game state."""
    from hearts_engine.engine.passing import apply_pass
    from hearts_engine.engine.play import apply_play
    from hearts_engine.engine.round import apply_moon_choice

    match action:
        case SelectPass(cards=cards):
            return apply_pass(state, cards)
        case PlayCard(card=card):
            return apply_play(state, card)
        case ChooseMoonOption(add_to_others=add_to_others):
            return apply_moon_choice(state, add_to_others)
