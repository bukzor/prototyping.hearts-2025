"""Hearts game engine - processes actions and manages state."""

import random
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from hearts_engine.cards import Card
from hearts_engine.cards import Play
from hearts_engine.cards import PlayerId
from hearts_engine.cards import Suit
from hearts_engine.cards import create_deck
from hearts_engine.rules import check_shot_moon
from hearts_engine.rules import find_two_of_clubs_holder
from hearts_engine.rules import round_points
from hearts_engine.rules import trick_winner
from hearts_engine.rules import valid_plays
from hearts_engine.state import ChooseMoonOption
from hearts_engine.state import GameState
from hearts_engine.state import PassDirection
from hearts_engine.state import Phase
from hearts_engine.state import PlayCard
from hearts_engine.state import PlayerAction
from hearts_engine.state import SelectPass
from hearts_engine.state import hands_from_deck
from hearts_engine.state import pass_target

if TYPE_CHECKING:
    pass

LOSING_SCORE = 100


@dataclass(frozen=True, slots=True)
class ActionResult:
    """Result of applying an action."""

    ok: bool
    error: str | None
    new_state: GameState | None


def new_game(game_id: str | None = None, seed: int | None = None) -> GameState:
    """Create a new game with shuffled deck."""
    rng = random.Random(seed)
    deck = create_deck()
    rng.shuffle(deck)
    hands = hands_from_deck(deck)

    return GameState(
        game_id=game_id or str(uuid.uuid4()),
        phase=Phase.PASSING,
        round_number=0,
        dealer=0,
        hands=hands,
        scores=[0, 0, 0, 0],
        round_scores=[0, 0, 0, 0],
        tricks_won=[[], [], [], []],
        trick=[],
        lead_player=None,
        current_player=0,  # Start with player 0 for passing
        hearts_broken=False,
        pending_passes={},
    )


def apply_action(state: GameState, action: PlayerAction) -> ActionResult:
    """Apply an action to the game state."""
    match action:
        case SelectPass(cards=cards):
            return apply_pass(state, cards)
        case PlayCard(card=card):
            return apply_play(state, card)
        case ChooseMoonOption(add_to_others=add_to_others):
            return apply_moon_choice(state, add_to_others)


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


def apply_play(state: GameState, card: Card) -> ActionResult:
    """Apply a card play."""
    if state.phase != Phase.PLAYING:
        return ActionResult(
            ok=False, error="Not in playing phase", new_state=None
        )

    player = state.current_player
    hand = state.hands[player]

    if card not in hand:
        return ActionResult(ok=False, error="Card not in hand", new_state=None)

    valid = valid_plays(state)
    if card not in valid:
        return ActionResult(
            ok=False, error=f"Invalid play: {card}", new_state=None
        )

    new_state = state.copy()
    new_state.hands[player].remove(card)
    new_state.trick.append(Play(player=player, card=card))

    if card.suit == Suit.HEARTS:
        new_state.hearts_broken = True

    if len(new_state.trick) == 4:
        complete_trick(new_state)
    else:
        new_state.current_player = (player + 1) % 4  # type: ignore[assignment]

    return ActionResult(ok=True, error=None, new_state=new_state)


def complete_trick(state: GameState) -> None:
    """Complete a trick and determine winner."""
    winner = trick_winner(state.trick)
    cards_won = [p.card for p in state.trick]
    state.tricks_won[winner.player].append(cards_won)
    state.trick = []
    state.lead_player = winner.player
    state.current_player = winner.player

    if all(len(h) == 0 for h in state.hands):
        complete_round(state)


def complete_round(state: GameState) -> None:
    """Complete a round and score it."""
    shooter = check_shot_moon(state)
    if shooter is not None:
        state.phase = Phase.ROUND_END
        state.current_player = shooter  # type: ignore[assignment]
        return

    apply_normal_scoring(state)
    check_game_end(state)


def apply_normal_scoring(state: GameState) -> None:
    """Apply normal round scoring (no moon shot)."""
    for i in range(4):
        points = round_points(state.tricks_won[i])
        state.round_scores[i] = points
        state.scores[i] += points


def apply_moon_choice(state: GameState, add_to_others: bool) -> ActionResult:
    """Apply moon shooting choice."""
    if state.phase != Phase.ROUND_END:
        return ActionResult(
            ok=False, error="Not in round end phase", new_state=None
        )

    shooter = check_shot_moon(state)
    if shooter is None or shooter != state.current_player:
        return ActionResult(
            ok=False, error="Not the moon shooter", new_state=None
        )

    new_state = state.copy()

    if add_to_others:
        for i in range(4):
            if i != shooter:
                new_state.scores[i] += 26
                new_state.round_scores[i] = 26
            else:
                new_state.round_scores[i] = 0
    else:
        new_state.scores[shooter] -= 26
        new_state.round_scores[shooter] = -26
        for i in range(4):
            if i != shooter:
                new_state.round_scores[i] = 0

    check_game_end(new_state)
    return ActionResult(ok=True, error=None, new_state=new_state)


def check_game_end(state: GameState) -> None:
    """Check if game should end."""
    if any(s >= LOSING_SCORE for s in state.scores):
        state.phase = Phase.GAME_END
    else:
        start_new_round(state)


def start_new_round(state: GameState) -> None:
    """Start a new round."""
    state.round_number += 1
    state.dealer = (state.dealer + 1) % 4  # type: ignore[assignment]

    rng = random.Random()
    deck = create_deck()
    rng.shuffle(deck)
    state.hands = hands_from_deck(deck)

    state.round_scores = [0, 0, 0, 0]
    state.tricks_won = [[], [], [], []]
    state.trick = []
    state.lead_player = None
    state.hearts_broken = False
    state.pending_passes = {}

    if state.pass_direction == PassDirection.HOLD:
        state.phase = Phase.PLAYING
        state.current_player = find_two_of_clubs_holder(state.hands)  # type: ignore[assignment]
        state.lead_player = state.current_player
    else:
        state.phase = Phase.PASSING
        state.current_player = 0
