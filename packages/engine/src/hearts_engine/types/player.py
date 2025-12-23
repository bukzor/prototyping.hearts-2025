"""Player identity types."""

from typing import Literal
from typing import TypeGuard

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
