"""Pass direction for a round."""

from ..types import api as T

PASS_CYCLE: tuple[T.PassDirection, ...] = (
    T.PassDirection.LEFT,
    T.PassDirection.RIGHT,
    T.PassDirection.ACROSS,
    T.PassDirection.HOLD,
)


def pass_direction_for_round(round_number: int) -> T.PassDirection:
    """Get pass direction for a round (0-indexed)."""
    return PASS_CYCLE[round_number % 4]
