"""Hearts game rules and validation."""

from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from typing import TYPE_CHECKING

from .card import QUEEN_OF_SPADES
from .card import TWO_OF_CLUBS
from .card import Card
from .card import Suit
from .card import Trick
from .cards import Cards
from .cards import Hand
from .state import GameState
from .state import Phase
from .types import PLAYER_IDS
from .types import PlayerId

if TYPE_CHECKING:
    from .state import PlayerAction


def is_point_card(card: Card) -> bool:
    """Check if a card is worth points."""
    return card.suit == Suit.HEARTS or card == QUEEN_OF_SPADES


def card_points(card: Card) -> int:
    """Get point value of a card."""
    if card.suit == Suit.HEARTS:
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


def trick_winner(trick: Trick) -> PlayerId:
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


def must_follow_suit(lead_suit: Suit) -> CardRestriction:
    """When following, must play matching suit if possible."""
    return lambda cards: cards.of_suit(lead_suit)


def no_point_cards(cards: Cards) -> Cards:
    return Cards(c for c in cards if not is_point_card(c))


def two_of_clubs_only(cards: Cards) -> Cards:
    assert TWO_OF_CLUBS in cards
    return Cards([TWO_OF_CLUBS])


def no_hearts(cards: Cards) -> Cards:
    return cards.not_of_suit(Suit.HEARTS)


def valid_plays(
    hand: Hand, trick: Trick, first_trick: bool, hearts_broken: bool
) -> Cards:
    """Get all valid cards to play."""
    lead_card = trick[trick.lead]

    restrictions: list[CardRestriction]
    if lead_card is not None:
        restrictions = [must_follow_suit(lead_card.suit)]
        if first_trick:
            restrictions.append(no_point_cards)
    elif first_trick:
        restrictions = [two_of_clubs_only]
    elif hearts_broken:
        restrictions = []
    else:
        restrictions = [no_hearts]

    valid = Cards(hand)
    for restrict in restrictions:
        restricted = restrict(valid)
        if restricted:
            valid = restricted

    return valid


def valid_pass_selections(hand: Hand) -> Iterator[tuple[Card, Card, Card]]:
    """Get all valid 3-card combinations for passing."""
    from itertools import combinations

    for combo in combinations(hand, 3):
        a, b, c = combo
        yield (a, b, c)


def valid_actions(
    phase: Phase,
    current_player: PlayerId,
    hand: Hand,
    trick: Trick | None,
    first_trick: bool,
    hearts_broken: bool,
    moon_shooter: PlayerId | None,
) -> list[PlayerAction]:
    """Get all valid actions for current player."""
    from .state import ChooseMoonOption
    from .state import PlayCard
    from .state import SelectPass

    match phase:
        case Phase.PASSING:
            return [SelectPass(cards=c) for c in valid_pass_selections(hand)]
        case Phase.PLAYING:
            assert trick is not None
            cards = valid_plays(hand, trick, first_trick, hearts_broken)
            return [PlayCard(card=c) for c in cards]
        case Phase.ROUND_END:
            if moon_shooter == current_player:
                return [
                    ChooseMoonOption(add_to_others=False),
                    ChooseMoonOption(add_to_others=True),
                ]
            return []
        case Phase.GAME_END:
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
) -> PlayerId | None:
    """Check if any player shot the moon. Returns player id or None."""
    for pid, tw in zip(PLAYER_IDS, tricks_won):
        if round_points(tw) == 26:
            return pid
    return None


def find_two_of_clubs_holder(hands: Sequence[Hand]) -> PlayerId:
    """Find which player has the 2 of clubs."""
    for pid, hand in zip(PLAYER_IDS, hands):
        if TWO_OF_CLUBS in hand:
            return pid
    raise AssertionError("No player has 2 of clubs")
