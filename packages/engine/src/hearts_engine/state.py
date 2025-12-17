"""Game state types for Hearts."""

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import TYPE_CHECKING

from hearts_engine.cards import Card
from hearts_engine.cards import Play
from hearts_engine.cards import PlayerId

if TYPE_CHECKING:
    from collections.abc import Sequence


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


@dataclass(slots=True)
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
    hands: list[list[Card]]
    scores: list[int]  # Cumulative
    round_scores: list[int]  # Current round
    tricks_won: list[list[list[Card]]]  # Cards won per player this round

    # Current trick
    trick: list[Play]
    lead_player: PlayerId | None
    current_player: PlayerId

    # Derived state
    hearts_broken: bool

    # Pass phase state
    pending_passes: dict[PlayerId, tuple[Card, Card, Card]] = field(
        default_factory=lambda: dict[PlayerId, tuple[Card, Card, Card]]()
    )

    @property
    def pass_direction(self) -> PassDirection:
        """Current pass direction."""
        return pass_direction_for_round(self.round_number)

    def valid_actions(self) -> list[PlayerAction]:
        """Compute valid actions for current player."""
        from hearts_engine.rules import valid_actions

        return valid_actions(self)

    def copy(self) -> GameState:
        """Create a deep copy of the state."""
        return GameState(
            game_id=self.game_id,
            phase=self.phase,
            round_number=self.round_number,
            dealer=self.dealer,
            hands=[list(h) for h in self.hands],
            scores=list(self.scores),
            round_scores=list(self.round_scores),
            tricks_won=[[list(t) for t in p] for p in self.tricks_won],
            trick=list(self.trick),
            lead_player=self.lead_player,
            current_player=self.current_player,
            hearts_broken=self.hearts_broken,
            pending_passes={k: v for k, v in self.pending_passes.items()},
        )


def hands_from_deck(deck: Sequence[Card]) -> list[list[Card]]:
    """Deal a deck into 4 hands of 13 cards."""
    assert len(deck) == 52, len(deck)
    return [list(deck[i * 13 : (i + 1) * 13]) for i in range(4)]
