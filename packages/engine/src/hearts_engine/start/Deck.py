"""A standard 52-card deck."""

from typing import Self

from ..types import api as T
from ..types.api import Cards


class Deck(Cards):
    """A standard 52-card deck."""

    def __new__(cls) -> Self:
        return super().__new__(
            cls, (T.Card(suit, rank) for suit in T.Suit for rank in T.Rank)
        )
