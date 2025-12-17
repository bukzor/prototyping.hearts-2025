"""Hearts game engine - round and game lifecycle."""

from .cards import Deck
from .main import ActionResult
from .rules import check_shot_moon
from .rules import find_two_of_clubs_holder
from .rules import round_points
from .state import GameState
from .state import PassDirection
from .state import Phase

LOSING_SCORE = 100


def complete_round(state: GameState) -> None:
    """Complete a round and score it."""
    shooter = check_shot_moon(state)
    if shooter is not None:
        state.phase = Phase.ROUND_END
        state.current_player = shooter  # type: ignore[assignment]
        return

    apply_normal_scoring(state)
    check_game_end(state)


def apply_normal_scoring(state: GameState) -> None:
    """Apply normal round scoring (no moon shot)."""
    for i in range(4):
        points = round_points(state.tricks_won[i])
        state.round_scores[i] = points
        state.scores[i] += points


def apply_moon_choice(state: GameState, add_to_others: bool) -> ActionResult:
    """Apply moon shooting choice."""
    if state.phase != Phase.ROUND_END:
        return ActionResult(
            ok=False, error="Not in round end phase", new_state=None
        )

    shooter = check_shot_moon(state)
    if shooter is None or shooter != state.current_player:
        return ActionResult(
            ok=False, error="Not the moon shooter", new_state=None
        )

    new_state = state.copy()

    if add_to_others:
        for i in range(4):
            if i != shooter:
                new_state.scores[i] += 26
                new_state.round_scores[i] = 26
            else:
                new_state.round_scores[i] = 0
    else:
        new_state.scores[shooter] -= 26
        new_state.round_scores[shooter] = -26
        for i in range(4):
            if i != shooter:
                new_state.round_scores[i] = 0

    check_game_end(new_state)
    return ActionResult(ok=True, error=None, new_state=new_state)


def check_game_end(state: GameState) -> None:
    """Check if game should end."""
    if any(s >= LOSING_SCORE for s in state.scores):
        state.phase = Phase.GAME_END
    else:
        start_new_round(state)


def start_new_round(state: GameState) -> None:
    """Start a new round."""
    state.round_number += 1
    state.dealer = (state.dealer + 1) % 4  # type: ignore[assignment]

    state.hands = Deck().deal_hands()

    state.round_scores = [0, 0, 0, 0]
    state.tricks_won = [[], [], [], []]
    state.trick = []
    state.lead_player = None
    state.hearts_broken = False
    state.pending_passes = {}

    if state.pass_direction == PassDirection.HOLD:
        state.phase = Phase.PLAYING
        state.current_player = find_two_of_clubs_holder(state.hands)  # type: ignore[assignment]
        state.lead_player = state.current_player
    else:
        state.phase = Phase.PASSING
        state.current_player = 0
