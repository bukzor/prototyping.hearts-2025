"""Tests for round and game lifecycle."""

from .card import QUEEN_OF_SPADES
from .card import Card
from .card import Rank
from .card import Suit
from .main import apply_action
from .main import new_game
from .round import check_game_end
from .round import start_new_round
from .rules import valid_actions
from .state import ChooseMoonOption
from .state import GameState
from .state import PassDirection
from .state import Phase
from .state import SelectPass


def _get_to_playing(seed: int = 42) -> GameState:
    """Helper to skip past passing phase."""
    game: GameState = new_game(seed=seed)
    for i in range(4):
        cards = game.hands[i].draw(3)
        result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
        assert result.ok
        assert result.new_state is not None
        game = result.new_state
    return game


class DescribeRoundCompletion:
    """Tests for complete_round - scoring after 13 tricks."""

    def _play_full_round(self, game: GameState) -> GameState:
        """Play all 13 tricks."""
        for _ in range(13 * 4):  # 13 tricks, 4 cards each
            valid = valid_actions(game)
            if not valid:
                break  # Round/game ended
            result = apply_action(game, valid[0])
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state
        return game

    def it_scores_round_after_13_tricks(self) -> None:
        game = _get_to_playing()
        game = self._play_full_round(game)
        # After round, cumulative scores should sum to 26 (all point cards)
        # (round_scores gets reset when new round starts)
        total_points = sum(game.scores)
        assert (
            total_points == 26 or total_points == -26
        ), f"Total points should be 26 or -26 (moon), got {total_points}"

    def it_empties_all_hands(self) -> None:
        game = _get_to_playing()
        game = self._play_full_round(game)
        # Hands should be empty OR refilled for new round
        total_cards = sum(len(h) for h in game.hands)
        assert total_cards in (
            0,
            52,
        ), f"Expected 0 or 52 cards, got {total_cards}"


class DescribeMoonShooting:
    """Tests for apply_moon_choice - shooter picks +26 others or -26 self."""

    def it_allows_add_to_others(self) -> None:
        # Create a state where player shot the moon
        game = new_game(seed=42)
        game.phase = Phase.ROUND_END
        game.current_player = 0
        # Give player 0 all point cards in tricks_won
        all_hearts = [Card(Suit.HEARTS, r) for r in Rank]
        game.tricks_won[0] = [all_hearts, [QUEEN_OF_SPADES]]

        result = apply_action(game, ChooseMoonOption(add_to_others=True))
        assert result.ok, result.error
        assert result.new_state is not None
        # Others should have +26
        for i in range(1, 4):
            assert result.new_state.scores[i] == 26, (
                i,
                result.new_state.scores[i],
            )
        assert result.new_state.scores[0] == 0

    def it_allows_subtract_from_self(self) -> None:
        game = new_game(seed=42)
        game.phase = Phase.ROUND_END
        game.current_player = 0
        all_hearts = [Card(Suit.HEARTS, r) for r in Rank]
        game.tricks_won[0] = [all_hearts, [QUEEN_OF_SPADES]]

        result = apply_action(game, ChooseMoonOption(add_to_others=False))
        assert result.ok, result.error
        assert result.new_state is not None
        assert result.new_state.scores[0] == -26


class DescribeGameEnd:
    """Tests for check_game_end and start_new_round."""

    def it_ends_game_at_100_points(self) -> None:
        game = new_game(seed=42)
        game.scores = [100, 50, 30, 20]
        check_game_end(game)
        assert game.phase == Phase.GAME_END

    def it_starts_new_round_under_100(self) -> None:
        game = new_game(seed=42)
        game.scores = [50, 30, 20, 10]
        old_round = game.round_number
        check_game_end(game)
        assert game.phase != Phase.GAME_END
        assert game.round_number == old_round + 1

    def it_rotates_pass_direction(self) -> None:
        game = new_game(seed=42)
        assert game.pass_direction == PassDirection.LEFT
        start_new_round(game)
        assert game.pass_direction == PassDirection.RIGHT
