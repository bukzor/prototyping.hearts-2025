"""Hearts game engine - passing phase."""

from hearts_engine.card import Card
from hearts_engine.card import PlayerId
from hearts_engine.engine.main import ActionResult
from hearts_engine.rules import find_two_of_clubs_holder
from hearts_engine.state import GameState
from hearts_engine.state import PassDirection
from hearts_engine.state import Phase
from hearts_engine.state import pass_target


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
    hand = state.hands[player]

    if not all(c in hand for c in cards):
        return ActionResult(
            ok=False, error="Cards not in hand", new_state=None
        )

    if len(set(cards)) != 3:
        return ActionResult(
            ok=False, error="Must select 3 different cards", new_state=None
        )

    new_state = state.copy()
    new_state.pending_passes[player] = cards

    if len(new_state.pending_passes) == 4:
        execute_passes(new_state)
        start_playing_phase(new_state)
    else:
        new_state.current_player = next_player_for_passing(new_state)

    return ActionResult(ok=True, error=None, new_state=new_state)


def next_player_for_passing(state: GameState) -> PlayerId:
    """Get next player who needs to pass."""
    for i in range(4):
        p: PlayerId = (state.current_player + 1 + i) % 4  # type: ignore[assignment]
        if p not in state.pending_passes:
            return p
    return state.current_player


def execute_passes(state: GameState) -> None:
    """Execute all pending passes."""
    direction = state.pass_direction
    received: dict[PlayerId, list[Card]] = {0: [], 1: [], 2: [], 3: []}

    for player, cards in state.pending_passes.items():
        target = pass_target(player, direction)
        received[target].extend(cards)
        for card in cards:
            state.hands[player].remove(card)

    for player, cards in received.items():
        state.hands[player].extend(cards)

    state.pending_passes.clear()


def start_playing_phase(state: GameState) -> None:
    """Transition to playing phase."""
    state.phase = Phase.PLAYING
    state.current_player = find_two_of_clubs_holder(state.hands)  # type: ignore[assignment]
    state.lead_player = state.current_player
