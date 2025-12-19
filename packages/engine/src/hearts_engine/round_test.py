"""Tests for round and game lifecycle."""

import dataclasses
from random import Random

from .card import QUEEN_OF_SPADES
from .card import Card
from .card import Rank
from .card import Suit
from .card import Trick
from .main import apply_action
from .main import new_game
from .round import check_game_end
from .round import start_new_round
from .rules import valid_actions_for_state
from .state import ChooseMoonOption
from .state import GameState
from .state import PassDirection
from .state import Phase
from .state import SelectPass
from .state import update_player
from .types import PLAYER_IDS
from .types import ActionSuccess


def _get_to_playing(seed: int = 42) -> tuple[GameState, Random]:
    """Helper to skip past passing phase. Returns (game, random)."""
    random = Random(seed)
    game: GameState = new_game(random)
    for i in PLAYER_IDS:
        cards = game.players[i].hand.draw_three(random)
        result = apply_action(game, SelectPass(cards=cards), random)
        assert isinstance(result, ActionSuccess), result
        game = result.new_state
    return game, random


class DescribeRoundCompletion:
    """Tests for complete_round - scoring after 13 tricks."""

    def _play_full_round(self, game: GameState, random: Random) -> GameState:
        """Play all 13 tricks."""
        for _ in range(13 * 4):  # 13 tricks, 4 cards each
            valid = valid_actions_for_state(game)
            if not valid:
                break  # Round/game ended
            result = apply_action(game, valid[0], random)
            assert isinstance(result, ActionSuccess), result
            game = result.new_state
        return game

    def it_scores_round_after_13_tricks(self) -> None:
        game, random = _get_to_playing()
        game = self._play_full_round(game, random)
        # After round, cumulative scores should sum to 26 (all point cards)
        # (round_scores gets reset when new round starts)
        total_points = sum(p.score for p in game.players)
        assert (
            total_points == 26 or total_points == -26
        ), f"Total points should be 26 or -26 (moon), got {total_points}"

    def it_empties_all_hands(self) -> None:
        game, random = _get_to_playing()
        game = self._play_full_round(game, random)
        # Hands should be empty OR refilled for new round
        total_cards = sum(len(p.hand) for p in game.players)
        assert total_cards in (
            0,
            52,
        ), f"Expected 0 or 52 cards, got {total_cards}"


class DescribeMoonShooting:
    """Tests for apply_moon_choice - shooter picks +26 others or -26 self."""

    def it_allows_add_to_others(self) -> None:
        # Create a state where player shot the moon
        random = Random(42)
        game = new_game(random)
        # Give player 0 all point cards in tricks_won (13 hearts + queen of spades)
        # Create tricks with all hearts (need 4 tricks of 4 cards = 16, but we only have 13 hearts)
        # For scoring, we just need tricks containing the point cards
        ranks = list(Rank)
        hearts_tricks = tuple(
            Trick(
                cards=(
                    Card(Suit.HEARTS, ranks[k]),
                    Card(Suit.HEARTS, ranks[k + 1]),
                    Card(Suit.HEARTS, ranks[k + 2]),
                    Card(Suit.HEARTS, ranks[k + 3]),
                ),
                lead=0,
            )
            for k in range(0, 12, 4)  # 3 tricks of 4 hearts each = 12 hearts
        )
        # Last heart + queen of spades in final trick
        final_trick = Trick(
            cards=(
                Card(Suit.HEARTS, Rank.ACE),
                QUEEN_OF_SPADES,
                Card(Suit.CLUBS, Rank.TWO),
                Card(Suit.CLUBS, Rank.THREE),
            ),
            lead=0,
        )
        players = update_player(
            game.players, 0, tricks_won=hearts_tricks + (final_trick,)
        )
        game = dataclasses.replace(
            game, phase=Phase.ROUND_END, current_player=0, players=players
        )

        result = apply_action(
            game, ChooseMoonOption(add_to_others=True), random
        )
        assert isinstance(result, ActionSuccess), result
        # Others should have +26
        for i in range(1, 4):
            assert result.new_state.players[i].score == 26, (
                i,
                result.new_state.players[i].score,
            )
        assert result.new_state.players[0].score == 0

    def it_allows_subtract_from_self(self) -> None:
        random = Random(42)
        game = new_game(random)
        # Same setup as above
        ranks = list(Rank)
        hearts_tricks = tuple(
            Trick(
                cards=(
                    Card(Suit.HEARTS, ranks[k]),
                    Card(Suit.HEARTS, ranks[k + 1]),
                    Card(Suit.HEARTS, ranks[k + 2]),
                    Card(Suit.HEARTS, ranks[k + 3]),
                ),
                lead=0,
            )
            for k in range(0, 12, 4)
        )
        final_trick = Trick(
            cards=(
                Card(Suit.HEARTS, Rank.ACE),
                QUEEN_OF_SPADES,
                Card(Suit.CLUBS, Rank.TWO),
                Card(Suit.CLUBS, Rank.THREE),
            ),
            lead=0,
        )
        players = update_player(
            game.players, 0, tricks_won=hearts_tricks + (final_trick,)
        )
        game = dataclasses.replace(
            game, phase=Phase.ROUND_END, current_player=0, players=players
        )

        result = apply_action(
            game, ChooseMoonOption(add_to_others=False), random
        )
        assert isinstance(result, ActionSuccess), result
        assert result.new_state.players[0].score == -26


class DescribeGameEnd:
    """Tests for check_game_end and start_new_round."""

    def it_ends_game_at_100_points(self) -> None:
        random = Random(42)
        game = new_game(random)
        players = update_player(game.players, 0, score=100)
        players = update_player(players, 1, score=50)
        players = update_player(players, 2, score=30)
        players = update_player(players, 3, score=20)
        game = dataclasses.replace(game, players=players)
        game = check_game_end(game, random)
        assert game.phase == Phase.GAME_END

    def it_starts_new_round_under_100(self) -> None:
        random = Random(42)
        game = new_game(random)
        players = update_player(game.players, 0, score=50)
        players = update_player(players, 1, score=30)
        players = update_player(players, 2, score=20)
        players = update_player(players, 3, score=10)
        game = dataclasses.replace(game, players=players)
        old_round = game.round_number
        game = check_game_end(game, random)
        assert game.phase != Phase.GAME_END
        assert game.round_number == old_round + 1

    def it_rotates_pass_direction(self) -> None:
        random = Random(42)
        game = new_game(random)
        assert game.pass_direction == PassDirection.LEFT
        game = start_new_round(game, random)
        assert game.pass_direction == PassDirection.RIGHT
