"""Tests for Player protocol."""

from .player import Player
from .types import api as T
from .types.api import Cards
from .types.api import Hand


class DescribePlayer:
    """Tests for Player protocol."""

    def it_is_a_protocol(self) -> None:
        # Player is a Protocol, not instantiated directly
        assert hasattr(Player, "__protocol_attrs__") or hasattr(
            Player, "_is_protocol"
        )

    def it_requires_pass_cards(self) -> None:
        class BadPlayer:
            def play_card(self, hand: Hand, valid: Cards) -> T.Card:
                return list(hand)[0]

        assert not isinstance(BadPlayer(), Player)

    def it_requires_play_card(self) -> None:
        class BadPlayer:
            def pass_cards(self, hand: Hand) -> tuple[T.Card, T.Card, T.Card]:
                cards = list(hand)[:3]
                return (cards[0], cards[1], cards[2])

        assert not isinstance(BadPlayer(), Player)

    def it_accepts_valid_implementation(self) -> None:
        class GoodPlayer:
            def pass_cards(self, hand: Hand) -> tuple[T.Card, T.Card, T.Card]:
                cards = list(hand)[:3]
                return (cards[0], cards[1], cards[2])

            def play_card(self, hand: Hand, valid: Cards) -> T.Card:
                return list(valid)[0]

        assert isinstance(GoodPlayer(), Player)
