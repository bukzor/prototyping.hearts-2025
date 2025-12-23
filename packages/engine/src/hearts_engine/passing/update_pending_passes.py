"""Update pending passes."""

from ..types import api as T
from ..types.api import PendingPasses
from ..types.api import ThreeCards


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
