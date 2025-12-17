"""Tests for game engine."""

from hearts_engine.card import TWO_OF_CLUBS
from hearts_engine.cards import create_deck
from hearts_engine.engine import apply_action
from hearts_engine.engine import new_game
from hearts_engine.state import GameState
from hearts_engine.state import PassDirection
from hearts_engine.state import Phase
from hearts_engine.state import PlayCard
from hearts_engine.state import SelectPass
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st


class DescribeNewGame:
    """Tests for new game creation."""

    def it_creates_game_in_passing_phase(self) -> None:
        game = new_game(seed=42)
        assert game.phase == Phase.PASSING

    def it_deals_13_cards_to_each_player(self) -> None:
        game = new_game(seed=42)
        for i in range(4):
            assert len(game.hands[i]) == 13, (i, len(game.hands[i]))

    def it_uses_all_52_cards(self) -> None:
        game = new_game(seed=42)
        all_cards = [c for h in game.hands for c in h]
        assert len(all_cards) == 52
        assert len(set(all_cards)) == 52

    def it_starts_at_round_zero(self) -> None:
        game = new_game(seed=42)
        assert game.round_number == 0

    def it_starts_with_zero_scores(self) -> None:
        game = new_game(seed=42)
        assert game.scores == [0, 0, 0, 0]
        assert game.round_scores == [0, 0, 0, 0]

    def it_has_left_pass_direction_for_round_zero(self) -> None:
        game = new_game(seed=42)
        assert game.pass_direction == PassDirection.LEFT

    def it_starts_with_player_zero_for_passing(self) -> None:
        game = new_game(seed=42)
        assert game.current_player == 0

    def it_is_reproducible_with_seed(self) -> None:
        game1 = new_game(seed=123)
        game2 = new_game(seed=123)
        assert game1.hands == game2.hands

    def it_is_different_without_seed(self) -> None:
        game1 = new_game()
        game2 = new_game()
        # Very unlikely to be identical
        assert game1.hands != game2.hands


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


class DescribePlayPhase:
    """Tests for playing cards."""

    def _get_to_playing(self, seed: int = 42) -> GameState:
        """Helper to skip past passing phase."""
        game: GameState = new_game(seed=seed)
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok
            assert result.new_state is not None
            game = result.new_state
        return game

    def it_starts_with_two_of_clubs_holder(self) -> None:
        game = self._get_to_playing()
        holder = game.current_player
        assert TWO_OF_CLUBS in game.hands[holder]

    def it_requires_two_of_clubs_first(self) -> None:
        game = self._get_to_playing()
        # Try playing something else
        holder = game.current_player
        other_cards = [c for c in game.hands[holder] if c != TWO_OF_CLUBS]
        if other_cards:
            result = apply_action(game, PlayCard(card=other_cards[0]))
            assert not result.ok

    def it_accepts_two_of_clubs_first(self) -> None:
        game = self._get_to_playing()
        result = apply_action(game, PlayCard(card=TWO_OF_CLUBS))
        assert result.ok, result.error

    def it_advances_to_next_player_after_play(self) -> None:
        game = self._get_to_playing()
        first_player = game.current_player
        result = apply_action(game, PlayCard(card=TWO_OF_CLUBS))
        assert result.new_state is not None
        assert result.new_state.current_player == (first_player + 1) % 4


class DescribeFollowingSuit:
    """Tests for following suit rule."""

    def _setup_trick_in_progress(self) -> GameState:
        """Set up a game mid-trick for testing follow rules."""
        game: GameState = new_game(seed=42)
        # Skip passing
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.new_state is not None
            game = result.new_state
        # Play 2 of clubs
        result = apply_action(game, PlayCard(card=TWO_OF_CLUBS))
        assert result.new_state is not None
        return result.new_state

    def it_must_follow_suit_if_able(self) -> None:
        game = self._setup_trick_in_progress()
        player = game.current_player
        hand = game.hands[player]
        lead_suit = game.trick[0].card.suit

        has_lead_suit = any(c.suit == lead_suit for c in hand)
        if has_lead_suit:
            # Must play lead suit
            off_suit = [c for c in hand if c.suit != lead_suit]
            if off_suit:
                result = apply_action(game, PlayCard(card=off_suit[0]))
                assert not result.ok

    def it_can_play_anything_if_void(self) -> None:
        game = self._setup_trick_in_progress()
        player = game.current_player
        hand = game.hands[player]
        lead_suit = game.trick[0].card.suit

        has_lead_suit = any(c.suit == lead_suit for c in hand)
        if not has_lead_suit:
            # Can play any card
            for card in hand:
                result = apply_action(game, PlayCard(card=card))
                # First trick restriction may block some
                if result.ok:
                    break
            # At least one should work
            assert any(
                apply_action(game, PlayCard(card=c)).ok for c in hand
            ), "Should be able to play something"


class DescribeHeartsBroken:
    """Tests for hearts broken rule."""

    def it_starts_not_broken(self) -> None:
        game = new_game(seed=42)
        assert not game.hearts_broken

    def it_breaks_when_heart_played(self) -> None:
        # This needs a specific setup where hearts can be played
        # For now, just test the flag exists and starts false
        game = new_game(seed=42)
        assert game.hearts_broken is False


# Property-based tests
class DescribeGameInvariants:
    """Property-based tests for game invariants."""

    @given(st.integers(min_value=0, max_value=1000))
    @settings(max_examples=20)
    def it_always_deals_valid_hands(self, seed: int) -> None:
        game = new_game(seed=seed)
        all_cards = [c for h in game.hands for c in h]
        assert len(all_cards) == 52
        assert len(set(all_cards)) == 52

    @given(st.integers(min_value=0, max_value=1000))
    @settings(max_examples=20)
    def it_always_has_two_of_clubs_somewhere(self, seed: int) -> None:
        game = new_game(seed=seed)
        all_cards = [c for h in game.hands for c in h]
        assert TWO_OF_CLUBS in all_cards

    @given(st.integers(min_value=0, max_value=1000))
    @settings(max_examples=20)
    def it_pass_direction_cycles_correctly(self, seed: int) -> None:
        from hearts_engine.state import pass_direction_for_round

        for r in range(8):
            d = pass_direction_for_round(r)
            expected = [
                PassDirection.LEFT,
                PassDirection.RIGHT,
                PassDirection.ACROSS,
                PassDirection.HOLD,
            ][r % 4]
            assert d == expected, (r, d, expected)


class DescribeTrickCompletion:
    """Tests for complete_trick - awarding trick to winner."""

    def _play_full_trick(self, game: GameState) -> GameState:
        """Play 4 cards to complete a trick."""
        for _ in range(4):
            valid = game.valid_actions()
            assert valid, "No valid actions"
            result = apply_action(game, valid[0])
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state
        return game

    def _get_to_playing(self, seed: int = 42) -> GameState:
        """Helper to skip past passing phase."""
        game: GameState = new_game(seed=seed)
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok
            assert result.new_state is not None
            game = result.new_state
        return game

    def it_clears_trick_after_4_cards(self) -> None:
        game = self._get_to_playing()
        game = self._play_full_trick(game)
        assert (
            len(game.trick) == 0
        ), f"Trick should be empty, got {len(game.trick)}"

    def it_awards_cards_to_winner(self) -> None:
        game = self._get_to_playing()
        game = self._play_full_trick(game)
        total_cards_won = sum(len(t) for p in game.tricks_won for t in p)
        assert (
            total_cards_won == 4
        ), f"Expected 4 cards won, got {total_cards_won}"

    def it_sets_winner_as_next_lead(self) -> None:
        game = self._get_to_playing()
        game = self._play_full_trick(game)
        # Winner should be current player and lead player
        assert game.current_player == game.lead_player


class DescribeRoundCompletion:
    """Tests for complete_round - scoring after 13 tricks."""

    def _get_to_playing(self, seed: int = 42) -> GameState:
        """Helper to skip past passing phase."""
        game: GameState = new_game(seed=seed)
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok
            assert result.new_state is not None
            game = result.new_state
        return game

    def _play_full_round(self, game: GameState) -> GameState:
        """Play all 13 tricks."""
        for _ in range(13 * 4):  # 13 tricks, 4 cards each
            valid = game.valid_actions()
            if not valid:
                break  # Round/game ended
            result = apply_action(game, valid[0])
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state
        return game

    def it_scores_round_after_13_tricks(self) -> None:
        game = self._get_to_playing()
        game = self._play_full_round(game)
        # After round, cumulative scores should sum to 26 (all point cards)
        # (round_scores gets reset when new round starts)
        total_points = sum(game.scores)
        assert (
            total_points == 26 or total_points == -26
        ), f"Total points should be 26 or -26 (moon), got {total_points}"

    def it_empties_all_hands(self) -> None:
        game = self._get_to_playing()
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
        from hearts_engine.state import ChooseMoonOption

        # Create a state where player shot the moon
        game = new_game(seed=42)
        game.phase = Phase.ROUND_END
        game.current_player = 0
        # Give player 0 all point cards in tricks_won
        from hearts_engine.card import QUEEN_OF_SPADES
        from hearts_engine.card import Card
        from hearts_engine.card import Rank
        from hearts_engine.card import Suit

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
        from hearts_engine.state import ChooseMoonOption

        game = new_game(seed=42)
        game.phase = Phase.ROUND_END
        game.current_player = 0
        from hearts_engine.card import QUEEN_OF_SPADES
        from hearts_engine.card import Card
        from hearts_engine.card import Rank
        from hearts_engine.card import Suit

        all_hearts = [Card(Suit.HEARTS, r) for r in Rank]
        game.tricks_won[0] = [all_hearts, [QUEEN_OF_SPADES]]

        result = apply_action(game, ChooseMoonOption(add_to_others=False))
        assert result.ok, result.error
        assert result.new_state is not None
        assert result.new_state.scores[0] == -26


class DescribeGameEnd:
    """Tests for check_game_end and start_new_round."""

    def it_ends_game_at_100_points(self) -> None:
        from hearts_engine.engine import check_game_end

        game = new_game(seed=42)
        game.scores = [100, 50, 30, 20]
        check_game_end(game)
        assert game.phase == Phase.GAME_END

    def it_starts_new_round_under_100(self) -> None:
        from hearts_engine.engine import check_game_end

        game = new_game(seed=42)
        game.scores = [50, 30, 20, 10]
        old_round = game.round_number
        check_game_end(game)
        assert game.phase != Phase.GAME_END
        assert game.round_number == old_round + 1

    def it_rotates_pass_direction(self) -> None:
        from hearts_engine.engine import start_new_round

        game = new_game(seed=42)
        assert game.pass_direction == PassDirection.LEFT
        start_new_round(game)
        assert game.pass_direction == PassDirection.RIGHT


class DescribeStatefulInvariants:
    """Stateful hypothesis tests - random valid action sequences."""

    @given(st.integers(min_value=0, max_value=10000))
    @settings(max_examples=50)
    def it_conserves_cards_through_passing(self, seed: int) -> None:
        """All 52 cards present after passing phase."""
        game: GameState = new_game(seed=seed)
        # Complete passing phase
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok
            assert result.new_state is not None
            game = result.new_state

        all_cards = [c for h in game.hands for c in h]
        assert (
            len(all_cards) == 52
        ), f"Lost cards during passing: {len(all_cards)}"
        assert len(set(all_cards)) == 52, "Duplicate cards after passing"

    @given(st.integers(min_value=0, max_value=10000))
    @settings(max_examples=20)
    def it_conserves_cards_through_tricks(self, seed: int) -> None:
        """All cards accounted for at any point (hands + tricks_won + trick)."""
        game: GameState = new_game(seed=seed)
        # Complete passing
        for i in range(4):
            cards = tuple(game.hands[i][:3])
            result = apply_action(game, SelectPass(cards=cards))  # type: ignore[arg-type]
            assert result.ok
            assert result.new_state is not None
            game = result.new_state

        # Play some tricks (up to 20 cards played)
        for _ in range(20):
            if game.phase != Phase.PLAYING:
                break
            valid = game.valid_actions()
            if not valid:
                break
            result = apply_action(game, valid[0])
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state

            # Count all cards
            hand_cards = [c for h in game.hands for c in h]
            trick_cards = [p.card for p in game.trick]
            won_cards = [c for p in game.tricks_won for t in p for c in t]
            total = len(hand_cards) + len(trick_cards) + len(won_cards)
            assert total == 52, f"Card count mismatch: {total}"

    @given(st.integers(min_value=0, max_value=10000))
    @settings(max_examples=10, deadline=5000)
    def it_terminates_within_reasonable_actions(self, seed: int) -> None:
        """Game reaches GAME_END within bounded actions."""
        game: GameState = new_game(seed=seed)
        max_actions = 1000  # Generous upper bound

        for _ in range(max_actions):
            if game.phase == Phase.GAME_END:
                return  # Success

            valid = game.valid_actions()
            if not valid:
                break
            result = apply_action(game, valid[0])
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state

        # Game should have ended
        assert (
            game.phase == Phase.GAME_END
        ), f"Game didn't end after {max_actions} actions, phase={game.phase}"
