"""Check if any player shot the moon."""

from collections.abc import Sequence

from ..types import api as T
from ..types.api import Trick
from .scoring import round_points


def check_shot_moon(
    tricks_won: Sequence[tuple[Trick, ...]],
) -> T.PlayerId | None:
    """Check if any player shot the moon. Returns player id or None."""
    for pid, tw in zip(T.PLAYER_IDS, tricks_won):
        if round_points(tw) == 26:
            return pid
    return None
