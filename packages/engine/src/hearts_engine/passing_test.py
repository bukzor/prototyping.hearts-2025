"""Tests for passing phase."""

from random import Random

from .cards import Deck
from .main import apply_action
from .main import new_game
from .state import GameState
from .state import Phase
from .state import SelectPass
from .types import PLAYER_IDS
from .types import ActionFailure
from .types import ActionSuccess


class DescribePassPhase:
    """Tests for passing cards."""

    def it_accepts_valid_pass(self) -> None:
        random = Random(42)
        game = new_game(random)
        cards = game.players[0].hand.draw_three(random)
        result = apply_action(game, SelectPass(cards=cards), random)
        assert isinstance(result, ActionSuccess), result
        assert result.new_state.pending_passes[0] is not None

    def it_rejects_cards_not_in_hand(self) -> None:
        random = Random(42)
        game = new_game(random)
        # Find cards not in player 0's hand
        other_cards = [c for c in Deck() if c not in game.players[0].hand][:3]
        a, b, c = other_cards
        result = apply_action(game, SelectPass(cards=(a, b, c)), random)
        assert isinstance(result, ActionFailure)
        assert "not in hand" in result.error.lower()

    def it_rejects_duplicate_cards(self) -> None:
        random = Random(42)
        game = new_game(random)
        card = next(iter(game.players[0].hand))
        result = apply_action(
            game, SelectPass(cards=(card, card, card)), random
        )
        assert isinstance(result, ActionFailure)
        assert "different" in result.error.lower()

    def it_advances_to_next_player(self) -> None:
        random = Random(42)
        game = new_game(random)
        cards = game.players[0].hand.draw_three(random)
        result = apply_action(game, SelectPass(cards=cards), random)
        assert isinstance(result, ActionSuccess), result
        assert result.new_state.current_player == 1

    def it_transitions_to_playing_after_all_pass(self) -> None:
        random = Random(42)
        game: GameState = new_game(random)
        for i in PLAYER_IDS:
            cards = game.players[i].hand.draw_three(random)
            result = apply_action(game, SelectPass(cards=cards), random)
            assert isinstance(result, ActionSuccess), result
            game = result.new_state
        assert game.phase == Phase.PLAYING
