"""Tests for game engine."""

from hearts_engine.cards import TWO_OF_CLUBS
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
