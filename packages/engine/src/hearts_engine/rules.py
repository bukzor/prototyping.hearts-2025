"""Hearts game rules and validation."""

from collections.abc import Callable
from collections.abc import Iterator
from collections.abc import Sequence
from typing import TYPE_CHECKING

from . import types as T
from .card import TWO_OF_CLUBS
from .card import Trick
from .cards import Cards
from .cards import Hand
from .scoring import is_point_card
from .scoring import round_points
from .state import GameState

if TYPE_CHECKING:
    from .state import PlayerAction


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


def is_first_trick(tricks_won: Sequence[tuple[Trick, ...]]) -> bool:
    """Check if this is the first trick of the round."""
    return all(len(tw) == 0 for tw in tricks_won)


CardRestriction = Callable[[Cards], Cards]


def must_follow_suit(lead_suit: T.Suit) -> CardRestriction:
    """When following, must play matching suit if possible."""
    return lambda cards: cards.of_suit(lead_suit)


def no_point_cards(cards: Cards) -> Cards:
    return Cards(c for c in cards if not is_point_card(c))


def two_of_clubs_only(cards: Cards) -> Cards:
    assert TWO_OF_CLUBS in cards
    return Cards([TWO_OF_CLUBS])


def no_hearts(cards: Cards) -> Cards:
    return cards.not_of_suit(T.Suit.HEARTS)


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


def valid_pass_selections(
    hand: Hand,
) -> Iterator[tuple[T.Card, T.Card, T.Card]]:
    """Get all valid 3-card combinations for passing."""
    from itertools import combinations

    for combo in combinations(hand, 3):
        a, b, c = combo
        yield (a, b, c)


def valid_actions(
    phase: T.Phase,
    current_player: T.PlayerId,
    hand: Hand,
    trick: Trick | None,
    first_trick: bool,
    hearts_broken: bool,
    moon_shooter: T.PlayerId | None,
) -> list[PlayerAction]:
    """Get all valid actions for current player."""
    from .state import ChooseMoonOption
    from .state import PlayCard
    from .state import SelectPass

    match phase:
        case T.Phase.PASSING:
            return [SelectPass(cards=c) for c in valid_pass_selections(hand)]
        case T.Phase.PLAYING:
            assert trick is not None
            cards = valid_plays(
                hand, trick.lead_suit, first_trick, hearts_broken
            )
            return [PlayCard(card=c) for c in cards]
        case T.Phase.ROUND_END:
            if moon_shooter == current_player:
                return [
                    ChooseMoonOption(add_to_others=False),
                    ChooseMoonOption(add_to_others=True),
                ]
            return []
        case T.Phase.GAME_END:
            return []


def valid_actions_for_state(state: GameState) -> list[PlayerAction]:
    """Extract args from GameState and call valid_actions."""
    tricks_won = state.tricks_won
    return valid_actions(
        phase=state.phase,
        current_player=state.current_player,
        hand=state.players[state.current_player].hand,
        trick=state.trick,
        first_trick=is_first_trick(tricks_won),
        hearts_broken=state.hearts_broken,
        moon_shooter=check_shot_moon(tricks_won),
    )


def check_shot_moon(
    tricks_won: Sequence[tuple[Trick, ...]],
) -> T.PlayerId | None:
    """Check if any player shot the moon. Returns player id or None."""
    for pid, tw in zip(T.PLAYER_IDS, tricks_won):
        if round_points(tw) == 26:
            return pid
    return None


def find_two_of_clubs_holder(hands: Sequence[Hand]) -> T.PlayerId:
    """Find which player has the 2 of clubs."""
    for pid, hand in zip(T.PLAYER_IDS, hands):
        if TWO_OF_CLUBS in hand:
            return pid
    raise AssertionError("No player has 2 of clubs")
