"""Player protocol for Hearts game."""

from typing import Protocol
from typing import runtime_checkable

from .card import Card
from .cards import Cards
from .cards import Hand


@runtime_checkable
class Player(Protocol):
    """Protocol for a Hearts player (human or bot)."""

    def pass_cards(self, hand: Hand) -> tuple[Card, Card, Card]:
        """Choose 3 cards to pass."""
        ...

    def play_card(self, hand: Hand, valid: Cards) -> Card:
        """Choose a card to play."""
        ...
