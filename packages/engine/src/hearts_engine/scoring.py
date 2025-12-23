"""Hearts scoring functions."""

from collections.abc import Iterable

from . import types as T
from .card import QUEEN_OF_SPADES
from .card import Trick


def is_point_card(card: T.Card) -> bool:
    """Check if a card is worth points."""
    return card.suit == T.Suit.HEARTS or card == QUEEN_OF_SPADES


def card_points(card: T.Card) -> int:
    """Get point value of a card."""
    if card.suit == T.Suit.HEARTS:
        return 1
    if card == QUEEN_OF_SPADES:
        return 13
    return 0


def trick_points(trick: Trick) -> int:
    """Calculate total points in a trick."""
    return sum(card_points(c) for c in trick.values())


def round_points(tricks: Iterable[Trick]) -> int:
    """Calculate total points from tricks won in a round."""
    return sum(trick_points(t) for t in tricks)
