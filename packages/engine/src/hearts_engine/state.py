"""Game state types for Hearts."""

import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import TypedDict
from typing import Unpack

from .card import Card
from .card import Trick
from .cards import Hand
from .types import PlayerId
from .types import player_id


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


PASS_CYCLE: tuple[PassDirection, ...] = (
    PassDirection.LEFT,
    PassDirection.RIGHT,
    PassDirection.ACROSS,
    PassDirection.HOLD,
)

ThreeCards = tuple[Card, Card, Card]
PendingPasses = tuple[
    ThreeCards | None, ThreeCards | None, ThreeCards | None, ThreeCards | None
]


def update_pending_passes(
    pending: PendingPasses, player: PlayerId, cards: ThreeCards
) -> PendingPasses:
    """Update pending passes for one player (type-safe tuple construction)."""
    match player:
        case 0:
            return (cards, pending[1], pending[2], pending[3])
        case 1:
            return (pending[0], cards, pending[2], pending[3])
        case 2:
            return (pending[0], pending[1], cards, pending[3])
        case 3:
            return (pending[0], pending[1], pending[2], cards)


@dataclass(frozen=True, slots=True)
class SelectPass:
    """Action: select 3 cards to pass."""

    cards: tuple[Card, Card, Card]


@dataclass(frozen=True, slots=True)
class PlayCard:
    """Action: play a card."""

    card: Card


@dataclass(frozen=True, slots=True)
class ChooseMoonOption:
    """Action: choose moon shooting option."""

    add_to_others: bool  # True = +26 to others, False = -26 to self


PlayerAction = SelectPass | PlayCard | ChooseMoonOption


def pass_direction_for_round(round_number: int) -> PassDirection:
    """Get pass direction for a round (0-indexed)."""
    return PASS_CYCLE[round_number % 4]


def pass_target(player: PlayerId, direction: PassDirection) -> PlayerId:
    """Get the target player for passing."""
    match direction:
        case PassDirection.LEFT:
            offset = 1
        case PassDirection.RIGHT:
            offset = 3
        case PassDirection.ACROSS:
            offset = 2
        case PassDirection.HOLD:
            return player  # No passing
    return player_id(player + offset)


@dataclass(frozen=True, slots=True)
class PlayerState:
    """State for a single player."""

    hand: Hand
    score: int = 0
    round_score: int = 0
    tricks_won: tuple[Trick, ...] = ()


class PlayerStateChanges(TypedDict, total=False):
    """Valid fields for updating PlayerState."""

    hand: Hand
    score: int
    round_score: int
    tricks_won: tuple[Trick, ...]


def update_player(
    players: tuple[PlayerState, ...],
    pid: PlayerId,
    **changes: Unpack[PlayerStateChanges],
) -> tuple[PlayerState, ...]:
    """Return new players tuple with one player updated via replace()."""
    new_player = dataclasses.replace(players[pid], **changes)
    return players[:pid] + (new_player,) + players[pid + 1 :]


@dataclass(frozen=True, slots=True)
class GameState:
    """Complete game state."""

    # Identity
    game_id: str

    # Phase
    phase: Phase

    # Round context
    round_number: int
    dealer: PlayerId

    # Player state (index = PlayerId)
    players: tuple[PlayerState, ...]

    # Current trick (None during passing phase)
    trick: Trick | None
    current_player: PlayerId

    # Derived state
    hearts_broken: bool

    # Pass phase state (indexed by PlayerId, None = not yet selected)
    pending_passes: PendingPasses = (None, None, None, None)

    @property
    def pass_direction(self) -> PassDirection:
        """Current pass direction."""
        return pass_direction_for_round(self.round_number)

    @property
    def hands(self) -> tuple[Hand, ...]:
        """All player hands as a tuple."""
        return tuple(p.hand for p in self.players)

    @property
    def tricks_won(self) -> tuple[tuple[Trick, ...], ...]:
        """All player tricks_won as a tuple."""
        return tuple(p.tricks_won for p in self.players)
