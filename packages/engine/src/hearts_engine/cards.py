"""Card collections for Hearts."""

from hearts_engine.card import Card
from hearts_engine.card import Rank
from hearts_engine.card import Suit


class Cards(set[Card]):
    """Collection of cards with group operation."""

    def group(self) -> dict[Suit, list[Card]]:
        """Return cards grouped by suit, sorted within each group."""
        result: dict[Suit, list[Card]] = {}
        for card in sorted(self):
            result.setdefault(card.suit, []).append(card)
        return result


class Hand(Cards):
    """A player's hand."""

    pass


class Deck(Cards):
    """A deck of cards."""

    pass


def create_deck() -> list[Card]:
    """Create a standard 52-card deck."""
    return [Card(suit, rank) for suit in Suit for rank in Rank]
