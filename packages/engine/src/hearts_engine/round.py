"""Hearts game engine - round and game lifecycle."""

from dataclasses import replace

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
from .types import PlayerId

LOSING_SCORE = 100


def complete_round(state: GameState) -> GameState:
    """Complete a round and score it."""
    shooter = check_shot_moon(state.players)
    if shooter is not None:
        return replace(state, phase=Phase.ROUND_END, current_player=shooter)

    state = apply_normal_scoring(state)
    return check_game_end(state)


def apply_normal_scoring(state: GameState) -> GameState:
    """Apply normal round scoring (no moon shot)."""
    players = state.players
    for i, player in enumerate(players):
        points = round_points(player.tricks_won)
        players = update_player(
            players,
            i,  # type: ignore[arg-type]
            round_score=points,
            score=player.score + points,
        )
    return replace(state, players=players)


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

    players = state.players
    if add_to_others:
        for i, player in enumerate(players):
            if i != shooter:
                players = update_player(
                    players,
                    i,  # type: ignore[arg-type]
                    score=player.score + 26,
                    round_score=26,
                )
            else:
                players = update_player(
                    players, i, round_score=0  # type: ignore[arg-type]
                )
    else:
        players = update_player(
            players,
            shooter,
            score=players[shooter].score - 26,
            round_score=-26,
        )
        for i in range(4):
            if i != shooter:
                players = update_player(
                    players, i, round_score=0  # type: ignore[arg-type]
                )

    state = replace(state, players=players)
    state = check_game_end(state)
    return ActionResult(ok=True, error=None, new_state=state)


def check_game_end(state: GameState) -> GameState:
    """Check if game should end."""
    if any(p.score >= LOSING_SCORE for p in state.players):
        return replace(state, phase=Phase.GAME_END)
    return start_new_round(state)


def start_new_round(state: GameState) -> GameState:
    """Start a new round."""
    round_number = state.round_number + 1
    dealer: PlayerId = (state.dealer + 1) % 4  # type: ignore[assignment]

    players = state.players
    for pid, hand in zip(PLAYER_IDS, Deck().deal_hands()):
        players = update_player(
            players, pid, hand=hand, round_score=0, tricks_won=()
        )

    # Determine phase and starting player
    direction = PassDirection(
        ("left", "right", "across", "hold")[round_number % 4]
    )
    if direction == PassDirection.HOLD:
        phase = Phase.PLAYING
        current_player: PlayerId = find_two_of_clubs_holder(players)  # type: ignore[assignment]
        lead_player: PlayerId | None = current_player
    else:
        phase = Phase.PASSING
        current_player = 0
        lead_player = None

    return replace(
        state,
        round_number=round_number,
        dealer=dealer,
        players=players,
        trick=Trick(),
        lead_player=lead_player,
        current_player=current_player,
        hearts_broken=False,
        pending_passes=(None, None, None, None),
        phase=phase,
    )
