"""Game state types for Hearts."""

from dataclasses import dataclass
from enum import Enum

from .card import Card
from .card import Trick
from .cards import Hand
from .types import PlayerId


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
    return (player + offset) % 4  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class PlayerState:
    """State for a single player."""

    hand: Hand
    score: int = 0
    round_score: int = 0
    tricks_won: tuple[Trick, ...] = ()


from dataclasses import replace as _replace
from typing import Any


def update_player(
    players: tuple[PlayerState, ...], player_id: PlayerId, **changes: Any
) -> tuple[PlayerState, ...]:
    """Return new players tuple with one player updated via replace()."""
    new_player = _replace(players[player_id], **changes)
    return players[:player_id] + (new_player,) + players[player_id + 1 :]


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
    pending_passes: tuple[
        tuple[Card, Card, Card] | None,
        tuple[Card, Card, Card] | None,
        tuple[Card, Card, Card] | None,
        tuple[Card, Card, Card] | None,
    ] = (None, None, None, None)

    @property
    def pass_direction(self) -> PassDirection:
        """Current pass direction."""
        return pass_direction_for_round(self.round_number)
