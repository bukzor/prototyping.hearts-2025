"""Tests for game creation."""

from random import Random

from . import types as T
from .main import new_game


class DescribeNewGame:
    """Tests for new game creation."""

    def it_creates_game_in_passing_phase(self) -> None:
        game = new_game(Random(42))
        assert game.phase == T.Phase.PASSING

    def it_deals_13_cards_to_each_player(self) -> None:
        game = new_game(Random(42))
        for i in T.PLAYER_IDS:
            assert len(game.players[i].hand) == 13, (
                i,
                len(game.players[i].hand),
            )

    def it_uses_all_52_cards(self) -> None:
        game = new_game(Random(42))
        all_cards = [c for p in game.players for c in p.hand]
        assert len(all_cards) == 52
        assert len(set(all_cards)) == 52

    def it_starts_at_round_zero(self) -> None:
        game = new_game(Random(42))
        assert game.round_number == 0

    def it_starts_with_zero_scores(self) -> None:
        game = new_game(Random(42))
        assert [p.score for p in game.players] == [0, 0, 0, 0]
        assert [p.round_score for p in game.players] == [0, 0, 0, 0]

    def it_has_left_pass_direction_for_round_zero(self) -> None:
        game = new_game(Random(42))
        assert game.pass_direction == T.PassDirection.LEFT

    def it_starts_with_player_zero_for_passing(self) -> None:
        game = new_game(Random(42))
        assert game.current_player == 0

    def it_is_reproducible_with_seed(self) -> None:
        game1 = new_game(Random(123))
        game2 = new_game(Random(123))
        assert [p.hand for p in game1.players] == [
            p.hand for p in game2.players
        ]

    def it_is_different_without_seed(self) -> None:
        game1 = new_game(Random())
        game2 = new_game(Random())
        # Very unlikely to be identical
        assert [p.hand for p in game1.players] != [
            p.hand for p in game2.players
        ]
