"""Game state helpers for Hearts."""

import dataclasses
from dataclasses import dataclass
from typing import Unpack

from .types import types as T
from .types.types import PendingPasses
from .types.types import PlayerState
from .types.types import PlayerStateChanges
from .types.types import ThreeCards

PASS_CYCLE: tuple[T.PassDirection, ...] = (
    T.PassDirection.LEFT,
    T.PassDirection.RIGHT,
    T.PassDirection.ACROSS,
    T.PassDirection.HOLD,
)


def update_pending_passes(
    pending: PendingPasses, player: T.PlayerId, cards: ThreeCards
) -> PendingPasses:
    """Update pending passes for one player (type-safe tuple construction)."""
    match player:
        case 0:
            return (cards, pending[1], pending[2], pending[3])
        case 1:
            return (pending[0], cards, pending[2], pending[3])
        case 2:
            return (pending[0], pending[1], cards, pending[3])
        case 3:
            return (pending[0], pending[1], pending[2], cards)


@dataclass(frozen=True, slots=True)
class SelectPass:
    """Action: select 3 cards to pass."""

    cards: tuple[T.Card, T.Card, T.Card]


@dataclass(frozen=True, slots=True)
class PlayCard:
    """Action: play a card."""

    card: T.Card


@dataclass(frozen=True, slots=True)
class ChooseMoonOption:
    """Action: choose moon shooting option."""

    add_to_others: bool  # True = +26 to others, False = -26 to self


PlayerAction = SelectPass | PlayCard | ChooseMoonOption


def pass_direction_for_round(round_number: int) -> T.PassDirection:
    """Get pass direction for a round (0-indexed)."""
    return PASS_CYCLE[round_number % 4]


def pass_target(player: T.PlayerId, direction: T.PassDirection) -> T.PlayerId:
    """Get the target player for passing."""
    match direction:
        case T.PassDirection.LEFT:
            offset = 1
        case T.PassDirection.RIGHT:
            offset = 3
        case T.PassDirection.ACROSS:
            offset = 2
        case T.PassDirection.HOLD:
            return player  # No passing
    return T.player_id(player + offset)


def update_player(
    players: tuple[PlayerState, ...],
    pid: T.PlayerId,
    **changes: Unpack[PlayerStateChanges],
) -> tuple[PlayerState, ...]:
    """Return new players tuple with one player updated via replace()."""
    new_player = dataclasses.replace(players[pid], **changes)
    return players[:pid] + (new_player,) + players[pid + 1 :]
