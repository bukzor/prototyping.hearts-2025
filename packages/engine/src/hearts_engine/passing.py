"""Hearts game engine - passing phase."""

import dataclasses

from . import types as T
from .card import Trick
from .cards import Hand
from .rules import find_two_of_clubs_holder
from .state import GameState
from .state import PendingPasses
from .state import pass_target
from .state import update_pending_passes
from .state import update_player


def apply_pass(
    state: GameState, cards: tuple[T.Card, T.Card, T.Card]
) -> T.ActionResult:
    """Apply a pass selection."""
    if state.phase != T.Phase.PASSING:
        return T.ActionFailure(error="Not in passing phase")

    if state.pass_direction == T.PassDirection.HOLD:
        return T.ActionFailure(error="Hold round, no passing")

    player = state.current_player
    hand = state.players[player].hand

    if not all(c in hand for c in cards):
        return T.ActionFailure(error="Cards not in hand")

    if len(set(cards)) != 3:
        return T.ActionFailure(error="Must select 3 different cards")

    pending = update_pending_passes(state.pending_passes, player, cards)
    state = dataclasses.replace(state, pending_passes=pending)

    if all(p is not None for p in state.pending_passes):
        state = execute_passes(state)
        leader = find_two_of_clubs_holder(state.hands)
        state = start_playing_phase(state, leader)
    else:
        state = dataclasses.replace(
            state,
            current_player=next_player_for_passing(
                player, state.pending_passes
            ),
        )

    return T.ActionSuccess(new_state=state)


def next_player_for_passing(
    current_player: T.PlayerId, pending_passes: PendingPasses
) -> T.PlayerId:
    """Get next player who needs to pass."""
    for i in T.PLAYER_IDS:
        p = T.player_id(current_player + 1 + i)
        if pending_passes[p] is None:
            return p
    return current_player


def execute_passes(state: GameState) -> GameState:
    """Execute all pending passes."""
    received: dict[T.PlayerId, list[T.Card]] = {0: [], 1: [], 2: [], 3: []}

    players = state.players
    # First pass: remove cards from each player's hand and track received
    for player in T.PLAYER_IDS:
        cards = state.pending_passes[player]
        assert cards is not None, player
        received[pass_target(player, state.pass_direction)].extend(cards)
        players = update_player(
            players, player, hand=Hand(players[player].hand - set(cards))
        )

    # Second pass: add received cards to each player's hand
    for player, cards in received.items():
        players = update_player(
            players, player, hand=Hand(players[player].hand | set(cards))
        )

    return dataclasses.replace(
        state, players=players, pending_passes=(None, None, None, None)
    )


def start_playing_phase(state: GameState, leader: T.PlayerId) -> GameState:
    """Transition to playing phase."""
    return dataclasses.replace(
        state,
        phase=T.Phase.PLAYING,
        trick=Trick(lead=leader),
        current_player=leader,
    )
