"""Hearts play validation - valid card selection for playing phase."""

from collections.abc import Callable
from collections.abc import Sequence

from ..constants import QUEEN_OF_SPADES
from ..constants import TWO_OF_CLUBS
from ..types import api as T
from ..types.api import Cards
from ..types.api import Hand
from ..types.api import Trick


def is_point_card(card: T.Card) -> bool:
    """Check if a card is worth points."""
    return card.suit == T.Suit.HEARTS or card == QUEEN_OF_SPADES


def is_first_trick(tricks_won: Sequence[tuple[Trick, ...]]) -> bool:
    """Check if this is the first trick of the round."""
    return all(len(tw) == 0 for tw in tricks_won)


CardRestriction = Callable[[Cards], Cards]


def must_follow_suit(lead_suit: T.Suit) -> CardRestriction:
    """When following, must play matching suit if possible."""
    return lambda cards: cards.of_suit(lead_suit)


def no_point_cards(cards: Cards) -> Cards:
    return Cards(c for c in cards if not is_point_card(c))


def no_hearts(cards: Cards) -> Cards:
    return cards.not_of_suit(T.Suit.HEARTS)


def two_of_clubs_only(cards: Cards) -> Cards:
    assert TWO_OF_CLUBS in cards
    return Cards([TWO_OF_CLUBS])


def _apply_restrictions(
    hand: Hand, restrictions: list[CardRestriction]
) -> Cards:
    """Apply restrictions, falling back if restriction leaves no cards."""
    valid = Cards(hand)
    for restrict in restrictions:
        restricted = restrict(valid)
        if restricted:
            valid = restricted
    return valid


def valid_leads(hand: Hand, first_trick: bool, hearts_broken: bool) -> Cards:
    """Get valid cards when leading a trick."""
    if first_trick:
        restrictions = [two_of_clubs_only]
    elif hearts_broken:
        restrictions = []
    else:
        restrictions = [no_hearts]
    return _apply_restrictions(hand, restrictions)


def valid_follows(hand: Hand, lead_suit: T.Suit, first_trick: bool) -> Cards:
    """Get valid cards when following a trick."""
    restrictions = [must_follow_suit(lead_suit)]
    if first_trick:
        restrictions.append(no_point_cards)
    return _apply_restrictions(hand, restrictions)


def valid_plays(
    hand: Hand,
    lead_suit: T.Suit | None,
    first_trick: bool,
    hearts_broken: bool,
) -> Cards:
    """Get all valid cards to play (dispatcher)."""
    if lead_suit is None:
        return valid_leads(hand, first_trick, hearts_broken)
    return valid_follows(hand, lead_suit, first_trick)
