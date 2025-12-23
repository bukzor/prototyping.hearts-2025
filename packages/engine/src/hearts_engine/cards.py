"""Card collections for Hearts."""

from collections.abc import Iterator
from collections.abc import Set as AbstractSet
from random import Random
from typing import Self

from . import types as T


class Cards(frozenset[T.Card]):
    """Collection of cards with group operation."""

    def __sub__(self, other: AbstractSet[T.Card]) -> Self:
        """Return self minus other, preserving type."""
        cls = type(self)
        return cls(super().__sub__(other))

    def of_suit(self, suit: T.Suit) -> Self:
        cls = type(self)
        return cls(c for c in self if c.suit == suit)

    def not_of_suit(self, suit: T.Suit) -> Self:
        cls = type(self)
        return cls(c for c in self if c.suit != suit)

    def hearts(self) -> Self:
        return self.of_suit(T.Suit.HEARTS)

    def group(self) -> dict[T.Suit, list[T.Card]]:
        """Return cards grouped by suit, sorted within each group."""
        result: dict[T.Suit, list[T.Card]] = {}
        for card in sorted(self):
            result.setdefault(card.suit, []).append(card)
        return result


def draw(cards: Cards, n: int, rng: Random) -> Cards:
    """Draw n random cards from a collection."""
    return Cards(rng.sample(tuple(cards), n))


def draw_three(cards: Cards, rng: Random) -> tuple[T.Card, T.Card, T.Card]:
    """Draw 3 random cards, typed for passing."""
    a, b, c = rng.sample(tuple(cards), 3)
    return (a, b, c)


class Hand(Cards):
    """A player's hand."""

    pass


class Deck(Cards):
    """A standard 52-card deck."""

    def __new__(cls) -> Deck:
        return super().__new__(
            cls, (T.Card(suit, rank) for suit in T.Suit for rank in T.Rank)
        )


def deal_hands(deck: Deck, rng: Random) -> Iterator[Hand]:
    """Deal deck into 4 hands of 13 cards."""
    remaining = Cards(deck)
    for _ in T.PLAYER_IDS:
        drawn = draw(remaining, 13, rng)
        yield Hand(drawn)
        remaining -= drawn
