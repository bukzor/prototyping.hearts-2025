"""Card types and deck creation for Hearts."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Suit(Enum):
    """Card suits. Order: Clubs < Diamonds < Spades < Hearts."""

    CLUBS = ("clubs", "♣")
    DIAMONDS = ("diamonds", "♦")
    SPADES = ("spades", "♠")
    HEARTS = ("hearts", "♥")

    def __init__(self, value: str, symbol: str) -> None:
        self._value_ = value
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol

    def __tty__(self) -> str:
        match self:
            case Suit.HEARTS | Suit.DIAMONDS:
                return f"\033[91m{self.symbol}\033[0m"
            case Suit.CLUBS | Suit.SPADES:
                return f"\033[90m{self.symbol}\033[0m"
            case _:
                raise AssertionError(self)


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

    def __tty__(self) -> str:
        return self.display


SUIT_KEYS = {
    "c": Suit.CLUBS,
    "d": Suit.DIAMONDS,
    "s": Suit.SPADES,
    "h": Suit.HEARTS,
}
RANK_KEYS = {r.display.lower(): r for r in Rank}


@dataclass(frozen=True, slots=True)
class Card:
    """An immutable playing card."""

    suit: Suit
    rank: Rank

    @classmethod
    def from_string(cls, s: str) -> Card:
        """Parse a card from keyboard input like '2h' or 'qs'."""
        s = s.lower()
        suit = SUIT_KEYS[s[-1]]
        rank = RANK_KEYS[s[:-1]]
        return cls(suit, rank)

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"Card({self.suit.name}, {self.rank.name})"

    def __tty__(self) -> str:
        return f"{self.rank}{self.suit.__tty__()}"

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
