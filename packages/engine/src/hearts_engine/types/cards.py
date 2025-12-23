"""Card collection types."""

from collections.abc import Set as AbstractSet
from typing import Self

from .card import Card
from .card import Suit


class Cards(frozenset[Card]):
    """Collection of cards with group operation."""

    def __sub__(self, other: AbstractSet[Card]) -> Self:
        """Return self minus other, preserving type."""
        cls = type(self)
        return cls(super().__sub__(other))

    def of_suit(self, suit: Suit) -> Self:
        cls = type(self)
        return cls(c for c in self if c.suit == suit)

    def not_of_suit(self, suit: Suit) -> Self:
        cls = type(self)
        return cls(c for c in self if c.suit != suit)

    def hearts(self) -> Self:
        return self.of_suit(Suit.HEARTS)

    def group(self) -> dict[Suit, list[Card]]:
        """Return cards grouped by suit, sorted within each group."""
        result: dict[Suit, list[Card]] = {}
        for card in sorted(self):
            result.setdefault(card.suit, []).append(card)
        return result


class Hand(Cards):
    """A player's hand."""

    pass
