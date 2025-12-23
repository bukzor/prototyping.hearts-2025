"""Tests for rules module."""

from collections.abc import Sequence

from hypothesis import given
from hypothesis import strategies as st

from . import types as T
from .card import QUEEN_OF_SPADES
from .card import TWO_OF_CLUBS
from .card import Trick
from .rules import trick_winner
from .scoring import card_points
from .scoring import is_point_card
from .scoring import trick_points


def trick_from_players(
    players: Sequence[int], cards: Sequence[T.Card]
) -> Trick:
    """Build a Trick from hypothesis-generated player indices and cards."""
    lead = players[0]
    assert T.is_player_id(lead)
    plays: dict[T.PlayerId, T.Card] = {}
    for p, c in zip(players, cards):
        assert T.is_player_id(p)
        plays[p] = c
    return Trick.from_dict(plays, lead=lead)


class DescribeIsPointCard:
    """Tests for point card identification."""

    def it_identifies_hearts_as_point_cards(self) -> None:
        for rank in T.Rank:
            card = T.Card(T.Suit.HEARTS, rank)
            assert is_point_card(card)

    def it_identifies_queen_of_spades(self) -> None:
        assert is_point_card(QUEEN_OF_SPADES)

    def it_rejects_other_spades(self) -> None:
        for rank in T.Rank:
            if rank != T.Rank.QUEEN:
                card = T.Card(T.Suit.SPADES, rank)
                assert not is_point_card(card)

    def it_rejects_clubs_and_diamonds(self) -> None:
        for suit in [T.Suit.CLUBS, T.Suit.DIAMONDS]:
            for rank in T.Rank:
                card = T.Card(suit, rank)
                assert not is_point_card(card)


class DescribeCardPoints:
    """Tests for point values."""

    def it_scores_hearts_as_one(self) -> None:
        for rank in T.Rank:
            card = T.Card(T.Suit.HEARTS, rank)
            assert card_points(card) == 1

    def it_scores_queen_of_spades_as_thirteen(self) -> None:
        assert card_points(QUEEN_OF_SPADES) == 13

    def it_scores_other_cards_as_zero(self) -> None:
        assert card_points(TWO_OF_CLUBS) == 0
        assert card_points(T.Card(T.Suit.DIAMONDS, T.Rank.ACE)) == 0
        assert card_points(T.Card(T.Suit.SPADES, T.Rank.ACE)) == 0


class DescribeTrickPoints:
    """Tests for trick scoring."""

    def it_sums_point_cards(self) -> None:
        trick = Trick(
            cards=(
                T.Card(T.Suit.HEARTS, T.Rank.TWO),
                T.Card(T.Suit.HEARTS, T.Rank.THREE),
                T.Card(T.Suit.CLUBS, T.Rank.ACE),
                T.Card(T.Suit.DIAMONDS, T.Rank.KING),
            ),
            lead=0,
        )
        assert trick_points(trick) == 2

    def it_counts_queen_of_spades(self) -> None:
        trick = Trick(
            cards=(
                QUEEN_OF_SPADES,
                T.Card(T.Suit.CLUBS, T.Rank.ACE),
                T.Card(T.Suit.CLUBS, T.Rank.KING),
                T.Card(T.Suit.CLUBS, T.Rank.QUEEN),
            ),
            lead=0,
        )
        assert trick_points(trick) == 13

    def it_handles_all_hearts_plus_queen(self) -> None:
        trick = Trick(
            cards=(
                T.Card(T.Suit.HEARTS, T.Rank.ACE),
                T.Card(T.Suit.HEARTS, T.Rank.KING),
                T.Card(T.Suit.HEARTS, T.Rank.QUEEN),
                QUEEN_OF_SPADES,
            ),
            lead=0,
        )
        assert trick_points(trick) == 16


class DescribeTrickWinner:
    """Tests for trick winner determination."""

    def it_picks_highest_of_led_suit(self) -> None:
        trick = Trick(
            cards=(
                T.Card(T.Suit.CLUBS, T.Rank.TWO),
                T.Card(T.Suit.CLUBS, T.Rank.ACE),
                T.Card(T.Suit.CLUBS, T.Rank.KING),
                T.Card(T.Suit.CLUBS, T.Rank.QUEEN),
            ),
            lead=0,
        )
        winner = trick_winner(trick)
        assert winner == 1

    def it_ignores_off_suit_cards(self) -> None:
        trick = Trick(
            cards=(
                T.Card(T.Suit.CLUBS, T.Rank.TWO),
                T.Card(T.Suit.HEARTS, T.Rank.ACE),  # Off suit
                T.Card(T.Suit.CLUBS, T.Rank.THREE),
                T.Card(T.Suit.SPADES, T.Rank.ACE),  # Off suit
            ),
            lead=0,
        )
        winner = trick_winner(trick)
        assert winner == 2

    def it_leader_wins_if_all_off_suit(self) -> None:
        trick = Trick(
            cards=(
                T.Card(T.Suit.CLUBS, T.Rank.TWO),
                T.Card(T.Suit.HEARTS, T.Rank.ACE),
                T.Card(T.Suit.DIAMONDS, T.Rank.ACE),
                T.Card(T.Suit.SPADES, T.Rank.ACE),
            ),
            lead=0,
        )
        winner = trick_winner(trick)
        assert winner == 0


# Hypothesis strategies
suits = st.sampled_from(list(T.Suit))
ranks = st.sampled_from(list(T.Rank))
cards = st.builds(T.Card, suit=suits, rank=ranks)
player_ids = st.sampled_from([0, 1, 2, 3])


class DescribeTrickWinnerProperties:
    """Property-based tests for trick winner."""

    @given(
        st.lists(cards, min_size=4, max_size=4, unique=True),
        st.permutations([0, 1, 2, 3]),
    )
    def it_always_returns_a_player_from_the_trick(
        self, four_cards: list[T.Card], players: list[int]
    ) -> None:
        trick = trick_from_players(players, four_cards)
        winner = trick_winner(trick)
        assert winner in players

    @given(
        st.lists(cards, min_size=4, max_size=4, unique=True),
        st.permutations([0, 1, 2, 3]),
    )
    def it_returns_a_card_from_the_trick(
        self, four_cards: list[T.Card], players: list[int]
    ) -> None:
        trick = trick_from_players(players, four_cards)
        winner = trick_winner(trick)
        assert trick[winner] in four_cards


class DescribePointCardProperties:
    """Property-based tests for point cards."""

    @given(cards)
    def it_total_points_is_26(self, _: T.Card) -> None:
        # All hearts (13) + queen of spades (13) = 26
        from .cards import Deck

        total = sum(card_points(c) for c in Deck())
        assert total == 26
