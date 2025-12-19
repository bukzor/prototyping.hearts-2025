"""Hearts game engine - round and game lifecycle."""

from .card import Trick
from .cards import Deck
from .main import ActionResult
from .rules import check_shot_moon
from .rules import find_two_of_clubs_holder
from .rules import round_points
from .state import GameState
from .state import PassDirection
from .state import Phase
from .state import update_player
from .types import PLAYER_IDS

LOSING_SCORE = 100


def complete_round(state: GameState) -> None:
    """Complete a round and score it."""
    shooter = check_shot_moon(state.players)
    if shooter is not None:
        state.phase = Phase.ROUND_END
        state.current_player = shooter  # type: ignore[assignment]
        return

    apply_normal_scoring(state)
    check_game_end(state)


def apply_normal_scoring(state: GameState) -> None:
    """Apply normal round scoring (no moon shot)."""
    for i, player in enumerate(state.players):
        points = round_points(player.tricks_won)
        state.players = update_player(
            state.players,
            i,  # type: ignore[arg-type]
            round_score=points,
            score=player.score + points,
        )


def apply_moon_choice(state: GameState, add_to_others: bool) -> ActionResult:
    """Apply moon shooting choice."""
    if state.phase != Phase.ROUND_END:
        return ActionResult(
            ok=False, error="Not in round end phase", new_state=None
        )

    shooter = check_shot_moon(state.players)
    if shooter is None or shooter != state.current_player:
        return ActionResult(
            ok=False, error="Not the moon shooter", new_state=None
        )

    new_state = state.copy()

    if add_to_others:
        for i, player in enumerate(new_state.players):
            if i != shooter:
                new_state.players = update_player(
                    new_state.players,
                    i,  # type: ignore[arg-type]
                    score=player.score + 26,
                    round_score=26,
                )
            else:
                new_state.players = update_player(
                    new_state.players,
                    i,  # type: ignore[arg-type]
                    round_score=0,
                )
    else:
        shooter_player = new_state.players[shooter]
        new_state.players = update_player(
            new_state.players,
            shooter,
            score=shooter_player.score - 26,
            round_score=-26,
        )
        for i in range(4):
            if i != shooter:
                new_state.players = update_player(
                    new_state.players,
                    i,  # type: ignore[arg-type]
                    round_score=0,
                )

    check_game_end(new_state)
    return ActionResult(ok=True, error=None, new_state=new_state)


def check_game_end(state: GameState) -> None:
    """Check if game should end."""
    if any(p.score >= LOSING_SCORE for p in state.players):
        state.phase = Phase.GAME_END
    else:
        start_new_round(state)


def start_new_round(state: GameState) -> None:
    """Start a new round."""
    state.round_number += 1
    state.dealer = (state.dealer + 1) % 4  # type: ignore[assignment]

    for pid, hand in zip(PLAYER_IDS, Deck().deal_hands()):
        state.players = update_player(
            state.players, pid, hand=hand, round_score=0, tricks_won=()
        )

    state.trick = Trick()
    state.lead_player = None
    state.hearts_broken = False
    state.pending_passes = (None, None, None, None)  # type: ignore[assignment]

    if state.pass_direction == PassDirection.HOLD:
        state.phase = Phase.PLAYING
        state.current_player = find_two_of_clubs_holder(state.players)  # type: ignore[assignment]
        state.lead_player = state.current_player
    else:
        state.phase = Phase.PASSING
        state.current_player = 0
