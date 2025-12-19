"""Hearts game engine - round and game lifecycle."""

import dataclasses
from random import Random

from .card import Trick
from .cards import Deck
from .rules import check_shot_moon
from .rules import find_two_of_clubs_holder
from .rules import round_points
from .state import GameState
from .state import PassDirection
from .state import Phase
from .state import PlayerState
from .state import pass_direction_for_round
from .state import update_player
from .types import PLAYER_IDS
from .types import ActionFailure
from .types import ActionResult
from .types import ActionSuccess
from .types import PlayerId
from .types import player_id

LOSING_SCORE = 100


def complete_round(state: GameState, random: Random) -> GameState:
    """Complete a round and score it."""
    shooter = check_shot_moon(state.tricks_won)
    if shooter is not None:
        return dataclasses.replace(
            state, phase=Phase.ROUND_END, current_player=shooter
        )

    state = dataclasses.replace(
        state, players=apply_normal_scoring(state.players)
    )
    return check_game_end(state, random)


def apply_normal_scoring(
    players: tuple[PlayerState, ...],
) -> tuple[PlayerState, ...]:
    """Apply normal round scoring (no moon shot)."""
    for pid, player in zip(PLAYER_IDS, players):
        points = round_points(player.tricks_won)
        players = update_player(
            players, pid, round_score=points, score=player.score + points
        )
    return players


def apply_moon_choice(
    state: GameState, add_to_others: bool, random: Random
) -> ActionResult:
    """Apply moon shooting choice."""
    if state.phase != Phase.ROUND_END:
        return ActionFailure(error="Not in round end phase")

    shooter = check_shot_moon(state.tricks_won)
    if shooter is None or shooter != state.current_player:
        return ActionFailure(error="Not the moon shooter")

    players = state.players
    if add_to_others:
        for pid, player in zip(PLAYER_IDS, players):
            if pid != shooter:
                players = update_player(
                    players, pid, score=player.score + 26, round_score=26
                )
            else:
                players = update_player(players, pid, round_score=0)
    else:
        players = update_player(
            players,
            shooter,
            score=players[shooter].score - 26,
            round_score=-26,
        )
        for pid in PLAYER_IDS:
            if pid != shooter:
                players = update_player(players, pid, round_score=0)

    state = dataclasses.replace(state, players=players)
    state = check_game_end(state, random)
    return ActionSuccess(new_state=state)


def check_game_end(state: GameState, random: Random) -> GameState:
    """Check if game should end."""
    if any(p.score >= LOSING_SCORE for p in state.players):
        return dataclasses.replace(state, phase=Phase.GAME_END)
    return start_new_round(state, random)


def start_new_round(state: GameState, random: Random) -> GameState:
    """Start a new round."""
    round_number = state.round_number + 1
    dealer = player_id(state.dealer + 1)

    players = state.players
    for pid, hand in zip(PLAYER_IDS, Deck().deal_hands(random)):
        players = update_player(
            players, pid, hand=hand, round_score=0, tricks_won=()
        )

    # Determine phase and starting player
    direction = pass_direction_for_round(round_number)
    trick: Trick | None
    if direction == PassDirection.HOLD:
        phase = Phase.PLAYING
        leader = find_two_of_clubs_holder(tuple(p.hand for p in players))
        trick = Trick(lead=leader)
        current_player = leader
    else:
        phase = Phase.PASSING
        trick = None
        current_player: PlayerId = 0

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
