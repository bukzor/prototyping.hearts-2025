"""Card types and deck creation for Hearts."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Suit(Enum):
    """Card suits."""

    CLUBS = ("clubs", "♣")
    DIAMONDS = ("diamonds", "♦")
    HEARTS = ("hearts", "♥")
    SPADES = ("spades", "♠")

    def __init__(self, value: str, symbol: str) -> None:
        self._value_ = value
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol


class Rank(Enum):
    """Card ranks with numeric values for comparison."""

    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")

    def __init__(self, order: int, display: str) -> None:
        self._value_ = order
        self.order = order
        self.display = display

    def __str__(self) -> str:
        return self.display


@dataclass(frozen=True, slots=True)
class Card:
    """An immutable playing card."""

    suit: Suit
    rank: Rank

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"Card({self.suit.name}, {self.rank.name})"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        if self.suit != other.suit:
            return list(Suit).index(self.suit) < list(Suit).index(other.suit)
        return self.rank.order < other.rank.order


PlayerId = Literal[0, 1, 2, 3]
PLAYER_IDS: tuple[PlayerId, ...] = (0, 1, 2, 3)


@dataclass(frozen=True, slots=True)
class Play:
    """A card played by a player."""

    player: PlayerId
    card: Card


def create_deck() -> list[Card]:
    """Create a standard 52-card deck."""
    return [Card(suit, rank) for suit in Suit for rank in Rank]


TWO_OF_CLUBS = Card(Suit.CLUBS, Rank.TWO)
QUEEN_OF_SPADES = Card(Suit.SPADES, Rank.QUEEN)
