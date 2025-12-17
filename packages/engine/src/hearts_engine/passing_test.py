"""Tests for passing phase."""

from .cards import Deck
from .main import apply_action
from .main import new_game
from .state import GameState
from .state import Phase
from .state import SelectPass


class DescribePassPhase:
    """Tests for passing cards."""

    def it_accepts_valid_pass(self) -> None:
        game = new_game(seed=42)
        cards = game.hands[0].draw(3)
        result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
        assert result.ok, result.error
        assert result.new_state is not None
        assert 0 in result.new_state.pending_passes

    def it_rejects_cards_not_in_hand(self) -> None:
        game = new_game(seed=42)
        # Find cards not in player 0's hand
        other_cards = [c for c in Deck() if c not in game.hands[0]][:3]
        result = apply_action(game, SelectPass(cards=tuple(other_cards)))  # type: ignore[arg-type]
        assert not result.ok
        assert "not in hand" in result.error.lower()  # type: ignore[union-attr]

    def it_rejects_duplicate_cards(self) -> None:
        game = new_game(seed=42)
        card = next(iter(game.hands[0]))
        result = apply_action(game, SelectPass(cards=(card, card, card)))
        assert not result.ok
        assert "different" in result.error.lower()  # type: ignore[union-attr]

    def it_advances_to_next_player(self) -> None:
        game = new_game(seed=42)
        cards = game.hands[0].draw(3)
        result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
        assert result.new_state is not None
        assert result.new_state.current_player == 1

    def it_transitions_to_playing_after_all_pass(self) -> None:
        game: GameState = new_game(seed=42)
        for i in range(4):
            cards = game.hands[i].draw(3)
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state
        assert game.phase == Phase.PLAYING
