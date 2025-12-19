"""Hearts game engine - passing phase."""

from .card import Card
from .cards import Hand
from .main import ActionResult
from .rules import find_two_of_clubs_holder
from .state import GameState
from .state import PassDirection
from .state import Phase
from .state import pass_target
from .state import update_player
from .types import PLAYER_IDS
from .types import PlayerId


def apply_pass(
    state: GameState, cards: tuple[Card, Card, Card]
) -> ActionResult:
    """Apply a pass selection."""
    if state.phase != Phase.PASSING:
        return ActionResult(
            ok=False, error="Not in passing phase", new_state=None
        )

    if state.pass_direction == PassDirection.HOLD:
        return ActionResult(
            ok=False, error="Hold round, no passing", new_state=None
        )

    player = state.current_player
    hand = state.players[player].hand

    if not all(c in hand for c in cards):
        return ActionResult(
            ok=False, error="Cards not in hand", new_state=None
        )

    if len(set(cards)) != 3:
        return ActionResult(
            ok=False, error="Must select 3 different cards", new_state=None
        )

    new_state = state.copy()
    # Create new tuple with this player's selection
    passes = list(new_state.pending_passes)
    passes[player] = cards
    new_state.pending_passes = tuple(passes)  # type: ignore[assignment]

    if all(p is not None for p in new_state.pending_passes):
        execute_passes(new_state)
        start_playing_phase(new_state)
    else:
        new_state.current_player = next_player_for_passing(
            new_state.current_player, new_state.pending_passes
        )

    return ActionResult(ok=True, error=None, new_state=new_state)


def next_player_for_passing(
    current_player: PlayerId,
    pending_passes: tuple[
        tuple[Card, Card, Card] | None,
        tuple[Card, Card, Card] | None,
        tuple[Card, Card, Card] | None,
        tuple[Card, Card, Card] | None,
    ],
) -> PlayerId:
    """Get next player who needs to pass."""
    for i in range(4):
        p: PlayerId = (current_player + 1 + i) % 4  # type: ignore[assignment]
        if pending_passes[p] is None:
            return p
    return current_player


def execute_passes(state: GameState) -> None:
    """Execute all pending passes."""
    direction = state.pass_direction
    received: dict[PlayerId, list[Card]] = {0: [], 1: [], 2: [], 3: []}

    # First pass: remove cards from each player's hand and track received
    for player in PLAYER_IDS:
        cards = state.pending_passes[player]
        assert cards is not None, player
        target = pass_target(player, direction)
        received[target].extend(cards)
        new_hand = Hand(state.players[player].hand - set(cards))
        state.players = update_player(state.players, player, hand=new_hand)

    # Second pass: add received cards to each player's hand
    for player, cards in received.items():
        new_hand = Hand(state.players[player].hand | set(cards))
        state.players = update_player(state.players, player, hand=new_hand)

    state.pending_passes = (None, None, None, None)  # type: ignore[assignment]


def start_playing_phase(state: GameState) -> None:
    """Transition to playing phase."""
    state.phase = Phase.PLAYING
    state.current_player = find_two_of_clubs_holder(state.players)  # type: ignore[assignment]
    state.lead_player = state.current_player
