"""Deal deck into hands."""

from collections.abc import Iterator
from random import Random

from ..types import api as T
from ..types.api import Cards
from ..types.api import Hand
from .Deck import Deck
from .draw import draw


def deal_hands(deck: Deck, rng: Random) -> Iterator[Hand]:
    """Deal deck into 4 hands of 13 cards."""
    remaining = Cards(deck)
    for _ in T.PLAYER_IDS:
        drawn = draw(remaining, 13, rng)
        yield Hand(drawn)
        remaining -= drawn
