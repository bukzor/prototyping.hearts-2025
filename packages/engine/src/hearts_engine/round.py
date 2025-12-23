"""Hearts game engine - round and game lifecycle."""

import dataclasses
from random import Random

from .ending.scoring import apply_normal_scoring
from .rules import check_shot_moon
from .start.api import start_new_round
from .state import update_player
from .types import api as T
from .types.api import GameState

LOSING_SCORE = 100


def complete_round(state: GameState, random: Random) -> GameState:
    """Complete a round and score it."""
    shooter = check_shot_moon(state.tricks_won)
    if shooter is not None:
        return dataclasses.replace(
            state, phase=T.Phase.ROUND_END, current_player=shooter
        )

    state = dataclasses.replace(
        state, players=apply_normal_scoring(state.players)
    )
    return check_game_end(state, random)


def apply_moon_choice(
    state: GameState, add_to_others: bool, random: Random
) -> T.ActionResult:
    """Apply moon shooting choice."""
    if state.phase != T.Phase.ROUND_END:
        return T.ActionFailure(error="Not in round end phase")

    shooter = check_shot_moon(state.tricks_won)
    if shooter is None or shooter != state.current_player:
        return T.ActionFailure(error="Not the moon shooter")

    players = state.players
    if add_to_others:
        for pid, player in zip(T.PLAYER_IDS, players):
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
        for pid in T.PLAYER_IDS:
            if pid != shooter:
                players = update_player(players, pid, round_score=0)

    state = dataclasses.replace(state, players=players)
    state = check_game_end(state, random)
    return T.ActionSuccess(new_state=state)


def check_game_end(state: GameState, random: Random) -> GameState:
    """Check if game should end."""
    if any(p.score >= LOSING_SCORE for p in state.players):
        return dataclasses.replace(state, phase=T.Phase.GAME_END)
    return start_new_round(state, random)
