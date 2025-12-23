"""Property-based tests for game invariants."""

from random import Random

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from . import types as T
from .card import TWO_OF_CLUBS
from .cards import draw_three
from .main import apply_action
from .main import new_game
from .rules import valid_actions_for_state
from .state import GameState
from .state import SelectPass
from .state import pass_direction_for_round


class DescribeGameInvariants:
    """Property-based tests for game invariants."""

    @given(st.integers(min_value=0, max_value=1000))
    @settings(max_examples=20)
    def it_always_deals_valid_hands(self, seed: int) -> None:
        game = new_game(Random(seed))
        all_cards = [c for p in game.players for c in p.hand]
        assert len(all_cards) == 52
        assert len(set(all_cards)) == 52

    @given(st.integers(min_value=0, max_value=1000))
    @settings(max_examples=20)
    def it_always_has_two_of_clubs_somewhere(self, seed: int) -> None:
        game = new_game(Random(seed))
        all_cards = [c for p in game.players for c in p.hand]
        assert TWO_OF_CLUBS in all_cards

    @given(st.integers(min_value=0, max_value=1000))
    @settings(max_examples=20)
    def it_pass_direction_cycles_correctly(self, seed: int) -> None:
        for r in range(8):
            d = pass_direction_for_round(r)
            expected = [
                T.PassDirection.LEFT,
                T.PassDirection.RIGHT,
                T.PassDirection.ACROSS,
                T.PassDirection.HOLD,
            ][r % 4]
            assert d == expected, (r, d, expected)


class DescribeStatefulInvariants:
    """Stateful hypothesis tests - random valid action sequences."""

    @given(st.integers(min_value=0, max_value=10000))
    @settings(max_examples=50)
    def it_conserves_cards_through_passing(self, seed: int) -> None:
        """All 52 cards present after passing phase."""
        random = Random(seed)
        game: GameState = new_game(random)
        # Complete passing phase
        for i in T.PLAYER_IDS:
            cards = draw_three(game.players[i].hand, random)
            result = apply_action(game, SelectPass(cards=cards), random)
            assert isinstance(result, T.ActionSuccess), result
            game = result.new_state

        all_cards = [c for p in game.players for c in p.hand]
        assert (
            len(all_cards) == 52
        ), f"Lost cards during passing: {len(all_cards)}"
        assert len(set(all_cards)) == 52, "Duplicate cards after passing"

    @given(st.integers(min_value=0, max_value=10000))
    @settings(max_examples=20)
    def it_conserves_cards_through_tricks(self, seed: int) -> None:
        """All cards accounted for at any point (hands + tricks_won + trick)."""
        random = Random(seed)
        game: GameState = new_game(random)
        # Complete passing
        for i in T.PLAYER_IDS:
            cards = draw_three(game.players[i].hand, random)
            result = apply_action(game, SelectPass(cards=cards), random)
            assert isinstance(result, T.ActionSuccess), result
            game = result.new_state

        # Play some tricks (up to 20 cards played)
        for _ in range(20):
            if game.phase != T.Phase.PLAYING:
                break
            valid = valid_actions_for_state(game)
            if not valid:
                break
            result = apply_action(game, valid[0], random)
            assert isinstance(result, T.ActionSuccess), result
            game = result.new_state

            # Count all cards
            hand_cards = [c for p in game.players for c in p.hand]
            trick_cards = list(game.trick.values()) if game.trick else []
            won_cards = [
                c
                for p in game.players
                for t in p.tricks_won
                for c in t.values()
            ]
            total = len(hand_cards) + len(trick_cards) + len(won_cards)
            assert total == 52, f"Card count mismatch: {total}"

    @given(st.integers(min_value=0, max_value=10000))
    @settings(max_examples=10, deadline=5000)
    def it_terminates_within_reasonable_actions(self, seed: int) -> None:
        """Game reaches GAME_END within bounded actions."""
        random = Random(seed)
        game: GameState = new_game(random)
        max_actions = 1000  # Generous upper bound

        for _ in range(max_actions):
            if game.phase == T.Phase.GAME_END:
                return  # Success

            valid = valid_actions_for_state(game)
            if not valid:
                break
            result = apply_action(game, valid[0], random)
            assert isinstance(result, T.ActionSuccess), result
            game = result.new_state

        # Game should have ended
        assert (
            game.phase == T.Phase.GAME_END
        ), f"Game didn't end after {max_actions} actions, phase={game.phase}"
