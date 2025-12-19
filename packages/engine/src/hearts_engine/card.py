"""Single card types for Hearts."""

from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum

from .types import PlayerId


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


@dataclass(frozen=True, slots=True)
class Trick:
    """Cards played in a trick, indexed by player position 0-3."""

    cards: tuple[Card | None, Card | None, Card | None, Card | None] = (
        None,
        None,
        None,
        None,
    )
    lead: PlayerId | None = None

    def __getitem__(self, player: PlayerId) -> Card | None:
        return self.cards[player]

    def __len__(self) -> int:
        """Number of cards played (non-None slots)."""
        return sum(1 for c in self.cards if c is not None)

    def items(self) -> Iterator[tuple[PlayerId, Card]]:
        """Yield (player_id, card) pairs for played cards."""
        for pid, card in enumerate(self.cards):
            if card is not None:
                yield pid, card  # type: ignore[misc]

    def values(self) -> Iterator[Card]:
        """Yield cards that have been played."""
        for card in self.cards:
            if card is not None:
                yield card

    def with_play(self, player: PlayerId, card: Card) -> Trick:
        """Return a new Trick with the given card added. Sets lead if first card."""
        cards = list(self.cards)
        cards[player] = card
        lead = self.lead if self.lead is not None else player
        return Trick(cards=tuple(cards), lead=lead)  # type: ignore[arg-type]

    @classmethod
    def from_dict(
        cls, plays: dict[PlayerId, Card], lead: PlayerId | None = None
    ) -> Trick:
        """Construct from a dict. Lead defaults to first key if not specified."""
        if lead is None and plays:
            lead = next(iter(plays))  # type: ignore[assignment]
        return cls(
            cards=(plays.get(0), plays.get(1), plays.get(2), plays.get(3)),
            lead=lead,
        )


TWO_OF_CLUBS = Card(Suit.CLUBS, Rank.TWO)
QUEEN_OF_SPADES = Card(Suit.SPADES, Rank.QUEEN)
