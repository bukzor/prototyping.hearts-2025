"""Draw 3 random cards (test helper)."""

from random import Random

from ..types import api as T
from ..types.api import Cards


def draw_three(cards: Cards, rng: Random) -> tuple[T.Card, T.Card, T.Card]:
    """Draw 3 random cards, typed for passing."""
    a, b, c = rng.sample(tuple(cards), 3)
    return (a, b, c)
