"""Determine winner of a trick."""

from ..types import api as T
from ..types.api import Trick


def trick_winner(trick: Trick) -> T.PlayerId:
    """Determine winner of a trick."""
    assert len(trick) == 4, len(trick)
    assert trick.lead is not None
    lead_card = trick[trick.lead]
    assert lead_card is not None
    lead_suit = lead_card.suit
    winner = trick.lead
    for player, card in trick.items():
        winner_card = trick[winner]
        assert winner_card is not None
        if card.suit == lead_suit and card.rank.order > winner_card.rank.order:
            winner = player
    return winner
