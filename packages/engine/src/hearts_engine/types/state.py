"""Game state types."""

from dataclasses import dataclass
from typing import TypedDict

from .card import Card
from .cards import Hand
from .phase import Phase
from .player import PlayerId
from .trick import Trick

ThreeCards = tuple[Card, Card, Card]
PendingPasses = tuple[
    ThreeCards | None, ThreeCards | None, ThreeCards | None, ThreeCards | None
]


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
    def hands(self) -> tuple[Hand, ...]:
        """All player hands as a tuple."""
        return tuple(p.hand for p in self.players)

    @property
    def tricks_won(self) -> tuple[tuple[Trick, ...], ...]:
        """All player tricks_won as a tuple."""
        return tuple(p.tricks_won for p in self.players)
