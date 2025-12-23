"""Execute all pending passes."""

import dataclasses

from ..state import update_player
from ..types import api as T
from ..types.api import GameState
from ..types.api import Hand
from .pass_direction_for_round import pass_direction_for_round
from .pass_target import pass_target


def execute_passes(state: GameState) -> GameState:
    """Execute all pending passes."""
    received: dict[T.PlayerId, list[T.Card]] = {0: [], 1: [], 2: [], 3: []}

    players = state.players
    # First pass: remove cards from each player's hand and track received
    for player in T.PLAYER_IDS:
        cards = state.pending_passes[player]
        assert cards is not None, player
        received[
            pass_target(player, pass_direction_for_round(state.round_number))
        ].extend(cards)
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
