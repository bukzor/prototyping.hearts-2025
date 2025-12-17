"""Tests for rules module."""

from hearts_engine.cards import QUEEN_OF_SPADES
from hearts_engine.cards import TWO_OF_CLUBS
from hearts_engine.cards import Card
from hearts_engine.cards import Play
from hearts_engine.cards import Rank
from hearts_engine.cards import Suit
from hearts_engine.rules import card_points
from hearts_engine.rules import has_suit
from hearts_engine.rules import is_point_card
from hearts_engine.rules import trick_points
from hearts_engine.rules import trick_winner
from hypothesis import given
from hypothesis import strategies as st


class DescribeIsPointCard:
    """Tests for point card identification."""

    def it_identifies_hearts_as_point_cards(self) -> None:
        for rank in Rank:
            card = Card(Suit.HEARTS, rank)
            assert is_point_card(card)

    def it_identifies_queen_of_spades(self) -> None:
        assert is_point_card(QUEEN_OF_SPADES)

    def it_rejects_other_spades(self) -> None:
        for rank in Rank:
            if rank != Rank.QUEEN:
                card = Card(Suit.SPADES, rank)
                assert not is_point_card(card)

    def it_rejects_clubs_and_diamonds(self) -> None:
        for suit in [Suit.CLUBS, Suit.DIAMONDS]:
            for rank in Rank:
                card = Card(suit, rank)
                assert not is_point_card(card)


class DescribeCardPoints:
    """Tests for point values."""

    def it_scores_hearts_as_one(self) -> None:
        for rank in Rank:
            card = Card(Suit.HEARTS, rank)
            assert card_points(card) == 1

    def it_scores_queen_of_spades_as_thirteen(self) -> None:
        assert card_points(QUEEN_OF_SPADES) == 13

    def it_scores_other_cards_as_zero(self) -> None:
        assert card_points(TWO_OF_CLUBS) == 0
        assert card_points(Card(Suit.DIAMONDS, Rank.ACE)) == 0
        assert card_points(Card(Suit.SPADES, Rank.ACE)) == 0


class DescribeTrickPoints:
    """Tests for trick scoring."""

    def it_sums_point_cards(self) -> None:
        cards = [
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
        ]
        assert trick_points(cards) == 2

    def it_counts_queen_of_spades(self) -> None:
        cards = [
            QUEEN_OF_SPADES,
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN),
        ]
        assert trick_points(cards) == 13

    def it_handles_all_hearts_plus_queen(self) -> None:
        cards = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            QUEEN_OF_SPADES,
        ]
        assert trick_points(cards) == 16


class DescribeTrickWinner:
    """Tests for trick winner determination."""

    def it_picks_highest_of_led_suit(self) -> None:
        plays = [
            Play(player=0, card=Card(Suit.CLUBS, Rank.TWO)),
            Play(player=1, card=Card(Suit.CLUBS, Rank.ACE)),
            Play(player=2, card=Card(Suit.CLUBS, Rank.KING)),
            Play(player=3, card=Card(Suit.CLUBS, Rank.QUEEN)),
        ]
        winner = trick_winner(plays)
        assert winner.player == 1

    def it_ignores_off_suit_cards(self) -> None:
        plays = [
            Play(player=0, card=Card(Suit.CLUBS, Rank.TWO)),
            Play(player=1, card=Card(Suit.HEARTS, Rank.ACE)),  # Off suit
            Play(player=2, card=Card(Suit.CLUBS, Rank.THREE)),
            Play(player=3, card=Card(Suit.SPADES, Rank.ACE)),  # Off suit
        ]
        winner = trick_winner(plays)
        assert winner.player == 2

    def it_leader_wins_if_all_off_suit(self) -> None:
        plays = [
            Play(player=0, card=Card(Suit.CLUBS, Rank.TWO)),
            Play(player=1, card=Card(Suit.HEARTS, Rank.ACE)),
            Play(player=2, card=Card(Suit.DIAMONDS, Rank.ACE)),
            Play(player=3, card=Card(Suit.SPADES, Rank.ACE)),
        ]
        winner = trick_winner(plays)
        assert winner.player == 0


class DescribeHasSuit:
    """Tests for suit checking."""

    def it_finds_suit_in_hand(self) -> None:
        hand = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.CLUBS, Rank.TWO)]
        assert has_suit(hand, Suit.HEARTS)
        assert has_suit(hand, Suit.CLUBS)
        assert not has_suit(hand, Suit.DIAMONDS)
        assert not has_suit(hand, Suit.SPADES)

    def it_handles_empty_hand(self) -> None:
        assert not has_suit([], Suit.HEARTS)


# Hypothesis strategies
suits = st.sampled_from(list(Suit))
ranks = st.sampled_from(list(Rank))
cards = st.builds(Card, suit=suits, rank=ranks)
player_ids = st.sampled_from([0, 1, 2, 3])


class DescribeTrickWinnerProperties:
    """Property-based tests for trick winner."""

    @given(
        st.lists(cards, min_size=4, max_size=4, unique=True),
        st.permutations([0, 1, 2, 3]),
    )
    def it_always_returns_a_player_from_the_trick(
        self, four_cards: list[Card], players: list[int]
    ) -> None:
        plays = [
            Play(player=players[i], card=four_cards[i])  # type: ignore[arg-type]
            for i in range(4)
        ]
        winner = trick_winner(plays)
        assert winner.player in players

    @given(
        st.lists(cards, min_size=4, max_size=4, unique=True),
        st.permutations([0, 1, 2, 3]),
    )
    def it_winner_card_is_in_trick(
        self, four_cards: list[Card], players: list[int]
    ) -> None:
        plays = [
            Play(player=players[i], card=four_cards[i])  # type: ignore[arg-type]
            for i in range(4)
        ]
        winner = trick_winner(plays)
        assert winner.card in four_cards


class DescribePointCardProperties:
    """Property-based tests for point cards."""

    @given(cards)
    def it_total_points_is_26(self, _: Card) -> None:
        # All hearts (13) + queen of spades (13) = 26
        from hearts_engine.cards import create_deck

        deck = create_deck()
        total = sum(card_points(c) for c in deck)
        assert total == 26
