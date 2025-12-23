"""Card collections for Hearts."""

from collections.abc import Iterator
from random import Random
from typing import Self

from .types import types as T
from .types.types import Cards
from .types.types import Hand


def draw(cards: Cards, n: int, rng: Random) -> Cards:
    """Draw n random cards from a collection."""
    return Cards(rng.sample(tuple(cards), n))


def draw_three(cards: Cards, rng: Random) -> tuple[T.Card, T.Card, T.Card]:
    """Draw 3 random cards, typed for passing."""
    a, b, c = rng.sample(tuple(cards), 3)
    return (a, b, c)


class Deck(Cards):
    """A standard 52-card deck."""

    def __new__(cls) -> Self:
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
