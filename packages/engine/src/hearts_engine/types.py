"""Shared type definitions for Hearts engine."""

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Literal

if TYPE_CHECKING:
    from .state import GameState

PlayerId = Literal[0, 1, 2, 3]
PLAYER_IDS: tuple[PlayerId, ...] = (0, 1, 2, 3)


@dataclass(frozen=True, slots=True)
class ActionResult:
    """Result of applying an action."""

    ok: bool
    error: str | None
    new_state: GameState | None
