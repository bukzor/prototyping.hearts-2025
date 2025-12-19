"""Hearts game engine - passing phase."""

from dataclasses import replace

from .card import Card
from .card import Trick
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

    # Create new tuple with this player's selection
    pending = (
        state.pending_passes[:player]
        + (cards,)
        + state.pending_passes[player + 1 :]
    )
    state = replace(state, pending_passes=pending)  # type: ignore[arg-type]

    if all(p is not None for p in state.pending_passes):
        state = execute_passes(state)
        state = start_playing_phase(state)
    else:
        state = replace(
            state,
            current_player=next_player_for_passing(
                player, state.pending_passes
            ),
        )

    return ActionResult(ok=True, error=None, new_state=state)


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
    for i in PLAYER_IDS:
        p: PlayerId = (current_player + 1 + i) % 4  # type: ignore[assignment]
        if pending_passes[p] is None:
            return p
    return current_player


def execute_passes(state: GameState) -> GameState:
    """Execute all pending passes."""
    received: dict[PlayerId, list[Card]] = {0: [], 1: [], 2: [], 3: []}

    players = state.players
    # First pass: remove cards from each player's hand and track received
    for player in PLAYER_IDS:
        cards = state.pending_passes[player]
        assert cards is not None, player
        received[pass_target(player, state.pass_direction)].extend(cards)
        players = update_player(
            players, player, hand=Hand(players[player].hand - set(cards))
        )

    # Second pass: add received cards to each player's hand
    for player, cards in received.items():
        players = update_player(
            players, player, hand=Hand(players[player].hand | set(cards))
        )

    return replace(
        state, players=players, pending_passes=(None, None, None, None)
    )


def start_playing_phase(state: GameState) -> GameState:
    """Transition to playing phase."""
    leader = find_two_of_clubs_holder(state.players)
    return replace(
        state,
        phase=Phase.PLAYING,
        trick=Trick(lead=leader),
        current_player=leader,
    )
