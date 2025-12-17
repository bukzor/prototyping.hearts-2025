"""Player protocol for Hearts game."""

from typing import Protocol
from typing import runtime_checkable

from hearts_engine.card import Card
from hearts_engine.cards import Cards
from hearts_engine.cards import Hand


@runtime_checkable
class Player(Protocol):
    """Protocol for a Hearts player (human or bot)."""

    def pass_cards(self, hand: Hand) -> tuple[Card, Card, Card]:
        """Choose 3 cards to pass."""
        ...

    def play_card(self, hand: Hand, valid: Cards) -> Card:
        """Choose a card to play."""
        ...
