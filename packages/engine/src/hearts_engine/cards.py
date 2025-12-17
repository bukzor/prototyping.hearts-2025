"""Card collections for Hearts."""

import random
from random import Random

from .card import Card
from .card import Rank
from .card import Suit


class Cards(set[Card]):
    """Collection of cards with group operation."""

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

    def __init__(self) -> None:
        super().__init__(Card(suit, rank) for suit in Suit for rank in Rank)

    def deal_hands(self, rng: Random = random.seed.__self__) -> list[Hand]:
        """Deal deck into 4 hands of 13 cards."""
        remaining = Cards(self)
        hands: list[Hand] = []
        for _ in range(4):
            drawn = remaining.draw(13, rng)
            hands.append(Hand(drawn))
            remaining -= drawn
        return hands
