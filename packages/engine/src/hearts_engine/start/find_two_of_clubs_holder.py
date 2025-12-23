"""Find which player has the 2 of clubs."""

from collections.abc import Sequence

from ..constants import TWO_OF_CLUBS
from ..types import api as T
from ..types.api import Hand


def find_two_of_clubs_holder(hands: Sequence[Hand]) -> T.PlayerId:
    """Find which player has the 2 of clubs."""
    for pid, hand in zip(T.PLAYER_IDS, hands):
        if TWO_OF_CLUBS in hand:
            return pid
    raise AssertionError("No player has 2 of clubs")
