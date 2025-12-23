"""Game state helpers for Hearts."""

import dataclasses
from dataclasses import dataclass
from typing import Unpack

from .types import types as T
from .types.types import PlayerState
from .types.types import PlayerStateChanges


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


def update_player(
    players: tuple[PlayerState, ...],
    pid: T.PlayerId,
    **changes: Unpack[PlayerStateChanges],
) -> tuple[PlayerState, ...]:
    """Return new players tuple with one player updated via replace()."""
    new_player = dataclasses.replace(players[pid], **changes)
    return players[:pid] + (new_player,) + players[pid + 1 :]
