"""Draw random cards from a collection."""

from random import Random

from ..types.api import Cards


def draw(cards: Cards, n: int, rng: Random) -> Cards:
    """Draw n random cards from a collection."""
    return Cards(rng.sample(tuple(cards), n))
