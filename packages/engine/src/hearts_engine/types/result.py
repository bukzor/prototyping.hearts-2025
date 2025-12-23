"""Action result types."""

from dataclasses import dataclass

from .state import GameState


@dataclass(frozen=True, slots=True)
class ActionSuccess:
    """Successful action result."""

    new_state: GameState


@dataclass(frozen=True, slots=True)
class ActionFailure:
    """Failed action result."""

    error: str


ActionResult = ActionSuccess | ActionFailure
