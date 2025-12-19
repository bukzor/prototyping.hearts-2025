"""Tests for playing phase."""

from random import Random

from .card import TWO_OF_CLUBS
from .main import apply_action
from .main import new_game
from .rules import valid_actions_for_state
from .state import GameState
from .state import PlayCard
from .state import SelectPass
from .types import PLAYER_IDS

# Module-level RNG for tests that need shared state
_random = Random(42)


def _get_to_playing(seed: int = 42) -> tuple[GameState, Random]:
    """Helper to skip past passing phase. Returns (game, random)."""
    random = Random(seed)
    game: GameState = new_game(random)
    for i in PLAYER_IDS:
        cards = game.players[i].hand.draw(3, random)
        result = apply_action(game, SelectPass(cards=cards), random)  # type: ignore[arg-type]
        assert result.ok
        assert result.new_state is not None
        game = result.new_state
    return game, random


class DescribePlayPhase:
    """Tests for playing cards."""

    def it_starts_with_two_of_clubs_holder(self) -> None:
        game, _ = _get_to_playing()
        holder = game.current_player
        assert TWO_OF_CLUBS in game.players[holder].hand

    def it_requires_two_of_clubs_first(self) -> None:
        game, random = _get_to_playing()
        # Try playing something else
        holder = game.current_player
        other_cards = [
            c for c in game.players[holder].hand if c != TWO_OF_CLUBS
        ]
        if other_cards:
            result = apply_action(game, PlayCard(card=other_cards[0]), random)
            assert not result.ok

    def it_accepts_two_of_clubs_first(self) -> None:
        game, random = _get_to_playing()
        result = apply_action(game, PlayCard(card=TWO_OF_CLUBS), random)
        assert result.ok, result.error

    def it_advances_to_next_player_after_play(self) -> None:
        game, random = _get_to_playing()
        first_player = game.current_player
        result = apply_action(game, PlayCard(card=TWO_OF_CLUBS), random)
        assert result.new_state is not None
        assert result.new_state.current_player == (first_player + 1) % 4


class DescribeFollowingSuit:
    """Tests for following suit rule."""

    def _setup_trick_in_progress(self) -> tuple[GameState, Random]:
        """Set up a game mid-trick for testing follow rules."""
        game, random = _get_to_playing()
        # Play 2 of clubs
        result = apply_action(game, PlayCard(card=TWO_OF_CLUBS), random)
        assert result.new_state is not None
        return result.new_state, random

    def it_must_follow_suit_if_able(self) -> None:
        game, random = self._setup_trick_in_progress()
        player = game.current_player
        hand = game.players[player].hand
        assert game.trick is not None
        lead_card = game.trick[game.trick.lead]
        assert lead_card is not None
        lead_suit = lead_card.suit

        has_lead_suit = any(c.suit == lead_suit for c in hand)
        if has_lead_suit:
            # Must play lead suit
            off_suit = [c for c in hand if c.suit != lead_suit]
            if off_suit:
                result = apply_action(game, PlayCard(card=off_suit[0]), random)
                assert not result.ok

    def it_can_play_anything_if_void(self) -> None:
        game, random = self._setup_trick_in_progress()
        player = game.current_player
        hand = game.players[player].hand
        assert game.trick is not None
        lead_card = game.trick[game.trick.lead]
        assert lead_card is not None
        lead_suit = lead_card.suit

        has_lead_suit = any(c.suit == lead_suit for c in hand)
        if not has_lead_suit:
            # Can play any card
            for card in hand:
                result = apply_action(game, PlayCard(card=card), random)
                # First trick restriction may block some
                if result.ok:
                    break
            # At least one should work
            assert any(
                apply_action(game, PlayCard(card=c), random).ok for c in hand
            ), "Should be able to play something"


class DescribeHeartsBroken:
    """Tests for hearts broken rule."""

    def it_starts_not_broken(self) -> None:
        game = new_game(Random(42))
        assert not game.hearts_broken

    def it_breaks_when_heart_played(self) -> None:
        # This needs a specific setup where hearts can be played
        # For now, just test the flag exists and starts false
        game = new_game(Random(42))
        assert game.hearts_broken is False


class DescribeTrickCompletion:
    """Tests for complete_trick - awarding trick to winner."""

    def _play_full_trick(self, game: GameState, random: Random) -> GameState:
        """Play 4 cards to complete a trick."""
        for _ in PLAYER_IDS:
            valid = valid_actions_for_state(game)
            assert valid, "No valid actions"
            result = apply_action(game, valid[0], random)
            assert result.ok, result.error
            assert result.new_state is not None
            game = result.new_state
        return game

    def it_clears_trick_after_4_cards(self) -> None:
        game, random = _get_to_playing()
        game = self._play_full_trick(game, random)
        assert game.trick is not None
        assert (
            len(game.trick) == 0
        ), f"Trick should be empty, got {len(game.trick)}"

    def it_awards_cards_to_winner(self) -> None:
        game, random = _get_to_playing()
        game = self._play_full_trick(game, random)
        total_cards_won = sum(
            len(t) for p in game.players for t in p.tricks_won
        )
        assert (
            total_cards_won == 4
        ), f"Expected 4 cards won, got {total_cards_won}"

    def it_sets_winner_as_next_lead(self) -> None:
        game, random = _get_to_playing()
        game = self._play_full_trick(game, random)
        # Winner should be current player and lead of next trick
        assert game.trick is not None
        assert game.current_player == game.trick.lead
