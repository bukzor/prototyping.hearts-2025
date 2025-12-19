"""Hearts game engine - playing phase."""

import dataclasses
from random import Random

from .card import Card
from .card import Suit
from .card import Trick
from .cards import Hand
from .rules import is_first_trick
from .rules import trick_winner
from .rules import valid_plays
from .state import GameState
from .state import Phase
from .state import update_player
from .types import ActionFailure
from .types import ActionResult
from .types import ActionSuccess
from .types import player_id


def apply_play(state: GameState, card: Card, random: Random) -> ActionResult:
    """Apply a card play."""
    if state.phase != Phase.PLAYING:
        return ActionFailure(error="Not in playing phase")
    assert state.trick is not None

    player = state.current_player
    hand = state.players[player].hand

    if card not in hand:
        return ActionFailure(error="Card not in hand")

    is_first = is_first_trick(state.tricks_won)
    if card not in valid_plays(
        hand, state.trick, is_first, state.hearts_broken
    ):
        return ActionFailure(error=f"Invalid play: {card}")

    trick = state.trick.with_play(player, card)
    state = dataclasses.replace(
        state,
        players=update_player(state.players, player, hand=Hand(hand - {card})),
        trick=trick,
        hearts_broken=state.hearts_broken or card.suit == Suit.HEARTS,
    )

    if len(trick) == 4:
        state = complete_trick(state, random)
    else:
        state = dataclasses.replace(
            state, current_player=player_id(player + 1)
        )

    return ActionSuccess(new_state=state)


def complete_trick(state: GameState, random: Random) -> GameState:
    """Complete a trick and determine winner."""
    from .round import complete_round

    assert state.trick is not None
    winner = trick_winner(state.trick)
    state = dataclasses.replace(
        state,
        players=update_player(
            state.players,
            winner,
            tricks_won=(*state.players[winner].tricks_won, state.trick),
        ),
        trick=Trick(lead=winner),
        current_player=winner,
    )

    if all(len(p.hand) == 0 for p in state.players):
        state = complete_round(state, random)

    return state
