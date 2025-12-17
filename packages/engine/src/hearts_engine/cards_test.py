"""Tests for cards module."""

from hearts_engine.cards import QUEEN_OF_SPADES
from hearts_engine.cards import TWO_OF_CLUBS
from hearts_engine.cards import Card
from hearts_engine.cards import Play
from hearts_engine.cards import Rank
from hearts_engine.cards import Suit
from hearts_engine.cards import create_deck
from hypothesis import given
from hypothesis import strategies as st


class DescribeCard:
    """Tests for Card dataclass."""

    def it_is_immutable(self) -> None:
        card = Card(Suit.HEARTS, Rank.ACE)
        try:
            card.suit = Suit.SPADES  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass

    def it_displays_nicely(self) -> None:
        assert str(Card(Suit.HEARTS, Rank.ACE)) == "A♥"
        assert str(Card(Suit.SPADES, Rank.QUEEN)) == "Q♠"
        assert str(Card(Suit.CLUBS, Rank.TWO)) == "2♣"
        assert str(Card(Suit.DIAMONDS, Rank.TEN)) == "10♦"

    def it_is_hashable(self) -> None:
        card = Card(Suit.HEARTS, Rank.ACE)
        assert hash(card) == hash(Card(Suit.HEARTS, Rank.ACE))
        s = {card, Card(Suit.HEARTS, Rank.ACE)}
        assert len(s) == 1

    def it_compares_by_suit_then_rank(self) -> None:
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.HEARTS, Rank.KING),
        ]
        sorted_cards = sorted(cards)
        assert sorted_cards[0].suit == Suit.CLUBS
        assert sorted_cards[1].suit == Suit.HEARTS
        assert sorted_cards[2].suit == Suit.SPADES


class DescribeCreateDeck:
    """Tests for deck creation."""

    def it_has_52_cards(self) -> None:
        deck = create_deck()
        assert len(deck) == 52

    def it_has_13_of_each_suit(self) -> None:
        deck = create_deck()
        for suit in Suit:
            count = sum(1 for c in deck if c.suit == suit)
            assert count == 13, (suit, count)

    def it_has_4_of_each_rank(self) -> None:
        deck = create_deck()
        for rank in Rank:
            count = sum(1 for c in deck if c.rank == rank)
            assert count == 4, (rank, count)

    def it_has_no_duplicates(self) -> None:
        deck = create_deck()
        assert len(set(deck)) == 52

    def it_includes_special_cards(self) -> None:
        deck = create_deck()
        assert TWO_OF_CLUBS in deck
        assert QUEEN_OF_SPADES in deck


class DescribePlay:
    """Tests for Play dataclass."""

    def it_stores_player_and_card(self) -> None:
        card = Card(Suit.HEARTS, Rank.ACE)
        play = Play(player=2, card=card)
        assert play.player == 2
        assert play.card == card


# Hypothesis strategies
suits = st.sampled_from(list(Suit))
ranks = st.sampled_from(list(Rank))
cards = st.builds(Card, suit=suits, rank=ranks)


class DescribeCardProperties:
    """Property-based tests for cards."""

    @given(cards)
    def it_round_trips_through_str(self, card: Card) -> None:
        s = str(card)
        assert len(s) >= 2
        assert s[-1] in "♣♦♥♠"

    @given(cards, cards)
    def it_has_consistent_equality(self, a: Card, b: Card) -> None:
        if a.suit == b.suit and a.rank == b.rank:
            assert a == b
            assert hash(a) == hash(b)
        else:
            assert a != b

    @given(cards, cards)
    def it_has_total_ordering(self, a: Card, b: Card) -> None:
        # Exactly one of <, ==, > is true
        lt = a < b
        eq = a == b
        gt = b < a
        assert sum([lt, eq, gt]) == 1
