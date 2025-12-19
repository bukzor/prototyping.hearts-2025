"""Card collections for Hearts."""

import random
from collections.abc import Iterator
from collections.abc import Set as AbstractSet
from random import Random
from typing import Self

from .card import Card
from .card import Rank
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

    def draw(self, n: int, rng: Random = random.seed.__self__) -> Cards:
        """Draw n random cards from this collection."""
        return Cards(rng.sample(tuple(self), n))


class Hand(Cards):
    """A player's hand."""

    pass


class Deck(Cards):
    """A standard 52-card deck."""

    def __new__(cls) -> Deck:
        return super().__new__(
            cls, (Card(suit, rank) for suit in Suit for rank in Rank)
        )

    def deal_hands(self, rng: Random = random.seed.__self__) -> Iterator[Hand]:
        """Deal deck into 4 hands of 13 cards."""
        remaining = Cards(self)
        for _ in range(4):
            drawn = remaining.draw(13, rng)
            yield Hand(drawn)
            remaining -= drawn
