"""Hearts game engine - passing phase."""

import dataclasses

from .card import Card
from .card import Trick
from .cards import Hand
from .rules import find_two_of_clubs_holder
from .state import GameState
from .state import PassDirection
from .state import PendingPasses
from .state import Phase
from .state import pass_target
from .state import update_pending_passes
from .state import update_player
from .types import PLAYER_IDS
from .types import ActionFailure
from .types import ActionResult
from .types import ActionSuccess
from .types import PlayerId
from .types import player_id


def apply_pass(
    state: GameState, cards: tuple[Card, Card, Card]
) -> ActionResult:
    """Apply a pass selection."""
    if state.phase != Phase.PASSING:
        return ActionFailure(error="Not in passing phase")

    if state.pass_direction == PassDirection.HOLD:
        return ActionFailure(error="Hold round, no passing")

    player = state.current_player
    hand = state.players[player].hand

    if not all(c in hand for c in cards):
        return ActionFailure(error="Cards not in hand")

    if len(set(cards)) != 3:
        return ActionFailure(error="Must select 3 different cards")

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

    return ActionSuccess(new_state=state)


def next_player_for_passing(
    current_player: PlayerId, pending_passes: PendingPasses
) -> PlayerId:
    """Get next player who needs to pass."""
    for i in PLAYER_IDS:
        p = player_id(current_player + 1 + i)
        if pending_passes[p] is None:
            return p
    return current_player


def execute_passes(state: GameState) -> GameState:
    """Execute all pending passes."""
    received: dict[PlayerId, list[Card]] = {0: [], 1: [], 2: [], 3: []}

    players = state.players
    # First pass: remove cards from each player's hand and track received
    for player in PLAYER_IDS:
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


def start_playing_phase(state: GameState, leader: PlayerId) -> GameState:
    """Transition to playing phase."""
    return dataclasses.replace(
        state,
        phase=Phase.PLAYING,
        trick=Trick(lead=leader),
        current_player=leader,
    )
