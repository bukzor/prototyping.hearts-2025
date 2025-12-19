"""Shared type definitions for Hearts engine."""

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Literal
from typing import TypeGuard

if TYPE_CHECKING:
    from .state import GameState

PlayerId = Literal[0, 1, 2, 3]
PLAYER_IDS: tuple[PlayerId, ...] = (0, 1, 2, 3)


def is_player_id(n: int) -> TypeGuard[PlayerId]:
    """Check if n is a valid PlayerId (0-3)."""
    return n in (0, 1, 2, 3)


def player_id(n: int) -> PlayerId:
    """Convert an integer to a PlayerId (mod 4)."""
    result = n % 4
    assert is_player_id(result), result
    return result


@dataclass(frozen=True, slots=True)
class ActionSuccess:
    """Successful action result."""

    new_state: GameState


@dataclass(frozen=True, slots=True)
class ActionFailure:
    """Failed action result."""

    error: str


ActionResult = ActionSuccess | ActionFailure
