"""Hearts game rules and validation."""

from typing import TYPE_CHECKING

from hearts_engine.card import QUEEN_OF_SPADES
from hearts_engine.card import TWO_OF_CLUBS
from hearts_engine.card import Card
from hearts_engine.card import Play
from hearts_engine.card import Suit

if TYPE_CHECKING:
    from hearts_engine.state import GameState
    from hearts_engine.state import PlayerAction


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


def trick_points(cards: list[Card]) -> int:
    """Calculate total points in a trick."""
    return sum(card_points(c) for c in cards)


def round_points(tricks: list[list[Card]]) -> int:
    """Calculate total points from tricks won in a round."""
    return sum(trick_points(t) for t in tricks)


def trick_winner(plays: list[Play]) -> Play:
    """Determine winner of a trick."""
    assert len(plays) == 4, len(plays)
    lead_suit = plays[0].card.suit
    winning = plays[0]
    for play in plays[1:]:
        if (
            play.card.suit == lead_suit
            and play.card.rank.order > winning.card.rank.order
        ):
            winning = play
    return winning


def has_suit(hand: list[Card], suit: Suit) -> bool:
    """Check if hand contains a card of the given suit."""
    return any(c.suit == suit for c in hand)


def cards_of_suit(hand: list[Card], suit: Suit) -> list[Card]:
    """Get all cards of a suit from hand."""
    return [c for c in hand if c.suit == suit]


def is_first_trick(state: GameState) -> bool:
    """Check if this is the first trick of the round."""
    return all(len(p) == 0 for p in state.tricks_won)


def can_lead_hearts(state: GameState) -> bool:
    """Check if hearts can be led."""
    if state.hearts_broken:
        return True
    hand = state.hands[state.current_player]
    return all(c.suit == Suit.HEARTS for c in hand)


def valid_leads(state: GameState) -> list[Card]:
    """Get valid cards to lead with."""
    hand = state.hands[state.current_player]

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
    hand = state.hands[state.current_player]
    lead_suit = state.trick[0].card.suit

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

    hand = state.hands[state.current_player]
    return list(combinations(hand, 3))  # type: ignore[return-value]


def valid_actions(state: GameState) -> list[PlayerAction]:
    """Get all valid actions for current player."""
    from hearts_engine.state import ChooseMoonOption
    from hearts_engine.state import Phase
    from hearts_engine.state import PlayCard
    from hearts_engine.state import SelectPass

    match state.phase:
        case Phase.PASSING:
            combos = valid_pass_selections(state)
            return [SelectPass(cards=c) for c in combos]
        case Phase.PLAYING:
            cards = valid_plays(state)
            return [PlayCard(card=c) for c in cards]
        case Phase.ROUND_END:
            if check_shot_moon(state) == state.current_player:
                return [
                    ChooseMoonOption(add_to_others=False),
                    ChooseMoonOption(add_to_others=True),
                ]
            return []
        case Phase.GAME_END:
            return []


def check_shot_moon(state: GameState) -> int | None:
    """Check if any player shot the moon. Returns player id or None."""
    for i, tricks in enumerate(state.tricks_won):
        points = round_points(tricks)
        if points == 26:
            return i
    return None


def find_two_of_clubs_holder(hands: list[list[Card]]) -> int:
    """Find which player has the 2 of clubs."""
    for i, hand in enumerate(hands):
        if TWO_OF_CLUBS in hand:
            return i
    raise AssertionError("No player has 2 of clubs")
