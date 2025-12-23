"""Hearts scoring functions - TEMPORARY: is_point_card moves to actions/play."""

from .constants import QUEEN_OF_SPADES
from .types import types as T


def is_point_card(card: T.Card) -> bool:
    """Check if a card is worth points."""
    return card.suit == T.Suit.HEARTS or card == QUEEN_OF_SPADES
