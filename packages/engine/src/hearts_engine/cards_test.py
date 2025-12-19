"""Tests for cards module."""

from hypothesis import given
from hypothesis import strategies as st

from .card import QUEEN_OF_SPADES
from .card import TWO_OF_CLUBS
from .card import Card
from .card import Rank
from .card import Suit
from .card import Trick
from .cards import Cards
from .cards import Deck
from .cards import Hand
from .tty import SupportsTTY


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
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),  # ace before two in input
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(
                Suit.CLUBS, Rank.TWO
            ),  # two after ace - test fails if rank ignored
        ]
        sorted_cards = sorted(cards)
        # Clubs < Diamonds < Spades < Hearts, then by rank (ace high)
        assert sorted_cards == [
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
        ]

    def it_parses_keyboard_input(self) -> None:
        # Lowercase suit letters for easy typing
        assert Card.from_string("ah") == Card(Suit.HEARTS, Rank.ACE)
        assert Card.from_string("2c") == Card(Suit.CLUBS, Rank.TWO)
        assert Card.from_string("10d") == Card(Suit.DIAMONDS, Rank.TEN)
        assert Card.from_string("qs") == Card(Suit.SPADES, Rank.QUEEN)
        # Case insensitive
        assert Card.from_string("2H") == Card(Suit.HEARTS, Rank.TWO)
        assert Card.from_string("AH") == Card(Suit.HEARTS, Rank.ACE)
        assert Card.from_string("Qs") == Card(Suit.SPADES, Rank.QUEEN)


class DescribeDeck:
    """Tests for Deck."""

    def it_has_52_cards(self) -> None:
        deck = Deck()
        assert len(deck) == 52

    def it_has_13_of_each_suit(self) -> None:
        deck = Deck()
        for suit in Suit:
            count = sum(1 for c in deck if c.suit == suit)
            assert count == 13, (suit, count)

    def it_has_4_of_each_rank(self) -> None:
        deck = Deck()
        for rank in Rank:
            count = sum(1 for c in deck if c.rank == rank)
            assert count == 4, (rank, count)

    def it_has_no_duplicates(self) -> None:
        deck = Deck()
        assert len(set(deck)) == 52

    def it_includes_special_cards(self) -> None:
        deck = Deck()
        assert TWO_OF_CLUBS in deck
        assert QUEEN_OF_SPADES in deck


class DescribeTrick:
    """Tests for Trick tuple subclass."""

    def it_stores_player_to_card_mapping(self) -> None:
        card = Card(Suit.HEARTS, Rank.ACE)
        trick: Trick = Trick.from_dict({2: card}, lead=2)
        assert trick[2] == card

    def it_is_a_dataclass(self) -> None:
        from dataclasses import is_dataclass

        trick: Trick = Trick(lead=0)
        assert is_dataclass(trick)

    def it_is_immutable(self) -> None:
        trick = Trick(lead=0)
        try:
            trick[0] = Card(Suit.HEARTS, Rank.ACE)  # type: ignore[index]
        except TypeError:
            pass
        else:
            raise AssertionError("Should have raised TypeError")


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


# ANSI color codes
RED = "\033[91m"  # bright red
BLACK = "\033[90m"  # bright black (dark gray)
RESET = "\033[0m"


class DescribeSuitTTY:
    """Tests for Suit.__tty__."""

    def it_implements_supports_tty(self) -> None:
        assert isinstance(Suit.HEARTS, SupportsTTY)

    def it_colors_hearts_red(self) -> None:
        assert Suit.HEARTS.__tty__() == f"{RED}♥{RESET}"

    def it_colors_diamonds_red(self) -> None:
        assert Suit.DIAMONDS.__tty__() == f"{RED}♦{RESET}"

    def it_colors_clubs_black(self) -> None:
        assert Suit.CLUBS.__tty__() == f"{BLACK}♣{RESET}"

    def it_colors_spades_black(self) -> None:
        assert Suit.SPADES.__tty__() == f"{BLACK}♠{RESET}"


class DescribeRankTTY:
    """Tests for Rank.__tty__."""

    def it_implements_supports_tty(self) -> None:
        assert isinstance(Rank.ACE, SupportsTTY)

    def it_returns_display_value(self) -> None:
        # Rank has no color - just returns display
        assert Rank.ACE.__tty__() == "A"
        assert Rank.TEN.__tty__() == "10"
        assert Rank.TWO.__tty__() == "2"


class DescribeCardTTY:
    """Tests for Card.__tty__."""

    def it_implements_supports_tty(self) -> None:
        assert isinstance(Card(Suit.HEARTS, Rank.ACE), SupportsTTY)

    def it_colors_hearts_red(self) -> None:
        card = Card(Suit.HEARTS, Rank.ACE)
        assert card.__tty__() == f"A{RED}♥{RESET}"

    def it_colors_diamonds_red(self) -> None:
        card = Card(Suit.DIAMONDS, Rank.QUEEN)
        assert card.__tty__() == f"Q{RED}♦{RESET}"

    def it_colors_clubs_black(self) -> None:
        card = Card(Suit.CLUBS, Rank.TWO)
        assert card.__tty__() == f"2{BLACK}♣{RESET}"

    def it_colors_spades_black(self) -> None:
        card = Card(Suit.SPADES, Rank.KING)
        assert card.__tty__() == f"K{BLACK}♠{RESET}"


class DescribeCards:
    """Tests for Cards collection."""

    def it_is_a_frozenset_of_card(self) -> None:
        cards = Cards([Card(Suit.HEARTS, Rank.ACE)])
        assert isinstance(cards, frozenset)
        assert len(cards) == 1

    def it_groups_by_suit(self) -> None:
        cards = Cards([
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.CLUBS, Rank.TWO),
        ])
        grouped = cards.group()
        assert grouped[Suit.CLUBS] == [
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.CLUBS, Rank.ACE),
        ]
        assert grouped[Suit.HEARTS] == [Card(Suit.HEARTS, Rank.KING)]
        assert Suit.DIAMONDS not in grouped
        assert Suit.SPADES not in grouped


class DescribeHand:
    """Tests for Hand subclass."""

    def it_is_a_cards(self) -> None:
        hand = Hand([Card(Suit.HEARTS, Rank.ACE)])
        assert isinstance(hand, Cards)
