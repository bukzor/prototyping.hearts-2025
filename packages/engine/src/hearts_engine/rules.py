"""Hearts game rules and validation."""

from collections.abc import Iterable
from collections.abc import Sequence
from typing import TYPE_CHECKING

from .card import QUEEN_OF_SPADES
from .card import TWO_OF_CLUBS
from .card import Card
from .card import PlayerId
from .card import Suit
from .card import Trick

if TYPE_CHECKING:
    from .state import GameState
    from .state import PlayerAction
    from .state import PlayerState


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


def trick_winner(trick: Trick, lead_player: PlayerId | None) -> PlayerId:
    """Determine winner of a trick."""
    assert len(trick) == 4, len(trick)
    assert lead_player is not None
    lead_card = trick[lead_player]
    assert lead_card is not None
    lead_suit = lead_card.suit
    winner = lead_player
    for player, card in trick.items():
        winner_card = trick[winner]
        assert winner_card is not None
        if card.suit == lead_suit and card.rank.order > winner_card.rank.order:
            winner = player
    return winner


def has_suit(hand: Iterable[Card], suit: Suit) -> bool:
    """Check if hand contains a card of the given suit."""
    return any(c.suit == suit for c in hand)


def cards_of_suit(hand: Iterable[Card], suit: Suit) -> list[Card]:
    """Get all cards of a suit from hand."""
    return [c for c in hand if c.suit == suit]


def is_first_trick(state: GameState) -> bool:
    """Check if this is the first trick of the round."""
    return all(len(p.tricks_won) == 0 for p in state.players)


def can_lead_hearts(state: GameState) -> bool:
    """Check if hearts can be led."""
    if state.hearts_broken:
        return True
    hand = state.players[state.current_player].hand
    return all(c.suit == Suit.HEARTS for c in hand)


def valid_leads(state: GameState) -> list[Card]:
    """Get valid cards to lead with."""
    hand = state.players[state.current_player].hand

    if is_first_trick(state):
        assert TWO_OF_CLUBS in hand, (hand, state.current_player)
        return [TWO_OF_CLUBS]

    if can_lead_hearts(state):
        return list(hand)

    non_hearts = [c for c in hand if c.suit != Suit.HEARTS]
    return non_hearts if non_hearts else list(hand)


def valid_follows(state: GameState) -> list[Card]:
    """Get valid cards when following a trick."""
    assert len(state.trick) > 0
    assert state.lead_player is not None
    hand = state.players[state.current_player].hand
    lead_card = state.trick[state.lead_player]
    assert lead_card is not None
    lead_suit = lead_card.suit

    if has_suit(hand, lead_suit):
        return cards_of_suit(hand, lead_suit)

    if is_first_trick(state):
        non_points = [c for c in hand if not is_point_card(c)]
        return non_points if non_points else list(hand)

    return list(hand)


def valid_plays(state: GameState) -> list[Card]:
    """Get all valid cards to play."""
    if len(state.trick) == 0:
        return valid_leads(state)
    return valid_follows(state)


def valid_pass_selections(state: GameState) -> list[tuple[Card, Card, Card]]:
    """Get all valid 3-card combinations for passing."""
    from itertools import combinations

    hand = state.players[state.current_player].hand
    return list(combinations(hand, 3))  # type: ignore[return-value]


def valid_actions(state: GameState) -> list[PlayerAction]:
    """Get all valid actions for current player."""
    from .state import ChooseMoonOption
    from .state import Phase
    from .state import PlayCard
    from .state import SelectPass

    match state.phase:
        case Phase.PASSING:
            combos = valid_pass_selections(state)
            return [SelectPass(cards=c) for c in combos]
        case Phase.PLAYING:
            cards = valid_plays(state)
            return [PlayCard(card=c) for c in cards]
        case Phase.ROUND_END:
            # TODO: should check all the time, not just round end.
            if check_shot_moon(state) == state.current_player:
                return [
                    ChooseMoonOption(add_to_others=False),
                    ChooseMoonOption(add_to_others=True),
                ]
            return []
        case Phase.GAME_END:
            return []


def check_shot_moon(state: GameState) -> PlayerId | None:
    """Check if any player shot the moon. Returns player id or None."""
    for i, player in enumerate(state.players):
        points = round_points(player.tricks_won)
        if points == 26:
            return i  # type: ignore[return-value]
    return None


def find_two_of_clubs_holder(players: Sequence[PlayerState]) -> int:
    """Find which player has the 2 of clubs."""
    for i, player in enumerate(players):
        if TWO_OF_CLUBS in player.hand:
            return i
    raise AssertionError("No player has 2 of clubs")
