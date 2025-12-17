"""Tests for passing phase."""

from hearts_engine.cards import create_deck
from hearts_engine.engine.main import apply_action
from hearts_engine.engine.main import new_game
from hearts_engine.state import GameState
from hearts_engine.state import Phase
from hearts_engine.state import SelectPass


class DescribePassPhase:
    """Tests for passing cards."""

    def it_accepts_valid_pass(self) -> None:
        game = new_game(seed=42)
        cards = tuple(game.hands[0][:3])
        result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
        assert result.ok, result.error
        assert result.new_state is not None
        assert 0 in result.new_state.pending_passes

    def it_rejects_cards_not_in_hand(self) -> None:
        game = new_game(seed=42)
        # Find cards not in player 0's hand
        other_cards = [c for c in create_deck() if c not in game.hands[0]][:3]
        result = apply_action(game, SelectPass(cards=tuple(other_cards)))  # type: ignore[arg-type]
        assert not result.ok
        assert "not in hand" in result.error.lower()  # type: ignore[union-attr]

    def it_rejects_duplicate_cards(self) -> None:
        game = new_game(seed=42)
        card = game.hands[0][0]
        result = apply_action(game, SelectPass(cards=(card, card, card)))
        assert not result.ok
        assert "different" in result.error.lower()  # type: ignore[union-attr]

    def it_advances_to_next_player(self) -> None:
        game = new_game(seed=42)
        cards = tuple(game.hands[0][:3])
        result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
        assert result.new_state is not None
        assert result.new_state.current_player == 1

    def it_transitions_to_playing_after_all_pass(self) -> None:
        game: GameState = new_game(seed=42)
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state
        assert game.phase == Phase.PLAYING
