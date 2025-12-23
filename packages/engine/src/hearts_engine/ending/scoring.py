"""Hearts scoring functions."""

from collections.abc import Iterable

from ..constants import QUEEN_OF_SPADES
from ..state import update_player
from ..types import api as T
from ..types.api import PlayerState
from ..types.api import Trick


def card_points(card: T.Card) -> int:
    """Get point value of a card."""
    if card.suit == T.Suit.HEARTS:
        return 1
    if card == QUEEN_OF_SPADES:
        return 13
    return 0


def trick_points(trick: Trick) -> int:
    """Calculate total points in a trick."""
    return sum(card_points(c) for c in trick.values())


def round_points(tricks: Iterable[Trick]) -> int:
    """Calculate total points from tricks won in a round."""
    return sum(trick_points(t) for t in tricks)


def apply_normal_scoring(
    players: tuple[PlayerState, ...],
) -> tuple[PlayerState, ...]:
    """Apply normal round scoring (no moon shot)."""
    for pid, player in zip(T.PLAYER_IDS, players):
        points = round_points(player.tricks_won)
        players = update_player(
            players, pid, round_score=points, score=player.score + points
        )
    return players
