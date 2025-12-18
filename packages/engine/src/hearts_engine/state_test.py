"""Tests for PlayerState."""

import dataclasses

import pytest

from .card import Card
from .card import Rank
from .card import Suit
from .card import Trick
from .cards import Hand
from .state import PlayerState


class DescribePlayerState:
    """Tests for PlayerState dataclass."""

    def it_exists(self) -> None:
        assert PlayerState is not None

    def it_holds_hand(self) -> None:
        hand = Hand([Card(Suit.HEARTS, Rank.ACE)])
        ps = PlayerState(hand=hand)
        assert ps.hand is hand

    def it_defaults_score_to_zero(self) -> None:
        ps = PlayerState(hand=Hand())
        assert ps.score == 0

    def it_defaults_round_score_to_zero(self) -> None:
        ps = PlayerState(hand=Hand())
        assert ps.round_score == 0

    def it_defaults_tricks_won_to_empty_tuple(self) -> None:
        ps = PlayerState(hand=Hand())
        assert ps.tricks_won == ()

    def it_stores_tricks_won(self) -> None:
        trick = Trick.from_dict({0: Card(Suit.HEARTS, Rank.ACE)})
        ps = PlayerState(hand=Hand(), tricks_won=(trick,))
        assert ps.tricks_won == (trick,)

    def it_is_frozen(self) -> None:
        ps = PlayerState(hand=Hand())
        with pytest.raises(dataclasses.FrozenInstanceError):
            ps.score = 100  # type: ignore[misc]

    def it_is_not_yet_hashable_because_hand_is_mutable(self) -> None:
        # TODO: Hand needs to be frozenset for full hashability
        ps = PlayerState(hand=Hand())
        with pytest.raises(TypeError, match="unhashable"):
            hash(ps)
