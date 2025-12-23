"""Next player for passing."""

from ..types import api as T
from ..types.api import PendingPasses


def next_player_for_passing(
    current_player: T.PlayerId, pending_passes: PendingPasses
) -> T.PlayerId:
    """Get next player who needs to pass."""
    for i in T.PLAYER_IDS:
        p = T.player_id(current_player + 1 + i)
        if pending_passes[p] is None:
            return p
    return current_player
