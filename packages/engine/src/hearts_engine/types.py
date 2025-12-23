"""Foundation types for Hearts engine."""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from typing import Literal
from typing import TypeGuard

if TYPE_CHECKING:
    from .state import GameState

# Player identity
PlayerId = Literal[0, 1, 2, 3]
PLAYER_IDS: tuple[PlayerId, ...] = (0, 1, 2, 3)


def is_player_id(n: int) -> TypeGuard[PlayerId]:
    """Check if n is a valid PlayerId (0-3)."""
    return n in (0, 1, 2, 3)


def player_id(n: int) -> PlayerId:
    """Convert an integer to a PlayerId (mod 4)."""
    result = n % 4
    assert is_player_id(result), result
    return result


# Card primitives
class Suit(Enum):
    """Card suits. Order: Clubs < Diamonds < Spades < Hearts."""

    CLUBS = (0, "clubs", "♣")
    DIAMONDS = (1, "diamonds", "♦")
    SPADES = (2, "spades", "♠")
    HEARTS = (3, "hearts", "♥")

    def __init__(self, order: int, value: str, symbol: str) -> None:
        self.order = order
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
            return self.suit.order < other.suit.order
        return self.rank.order < other.rank.order


# Game phases
class Phase(Enum):
    """Game phase."""

    PASSING = "passing"
    PLAYING = "playing"
    ROUND_END = "round_end"
    GAME_END = "game_end"


class PassDirection(Enum):
    """Direction for passing cards."""

    LEFT = "left"
    RIGHT = "right"
    ACROSS = "across"
    HOLD = "hold"


# Action results
@dataclass(frozen=True, slots=True)
class ActionSuccess:
    """Successful action result."""

    new_state: GameState


@dataclass(frozen=True, slots=True)
class ActionFailure:
    """Failed action result."""

    error: str


ActionResult = ActionSuccess | ActionFailure
