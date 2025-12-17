"""Tests for CLI renderer."""


class DescribeCardFormatter:
    def it_formats_number_cards_with_suit_symbol(self) -> None:
        pass

    def it_formats_face_cards_with_letter(self) -> None:
        pass

    def it_formats_ace_as_A(self) -> None:
        pass

    def it_formats_ten_as_10(self) -> None:
        pass


class DescribeHandRenderer:
    def it_sorts_cards_by_suit_then_rank(self) -> None:
        pass

    def it_groups_cards_by_suit(self) -> None:
        pass

    def it_highlights_valid_plays(self) -> None:
        pass

    def it_handles_empty_hand(self) -> None:
        pass


class DescribeTrickRenderer:
    def it_shows_cards_played_in_order(self) -> None:
        pass

    def it_shows_placeholders_for_unplayed_positions(self) -> None:
        pass

    def it_indicates_lead_player(self) -> None:
        pass

    def it_handles_empty_trick(self) -> None:
        pass


class DescribeScoreRenderer:
    def it_shows_cumulative_scores(self) -> None:
        pass

    def it_shows_round_scores(self) -> None:
        pass

    def it_shows_round_number(self) -> None:
        pass

    def it_shows_pass_direction(self) -> None:
        pass


class DescribeGameRenderer:
    def it_renders_passing_phase(self) -> None:
        pass

    def it_renders_playing_phase(self) -> None:
        pass

    def it_renders_round_end_with_moon_choice(self) -> None:
        pass

    def it_renders_game_end_with_winner(self) -> None:
        pass

    def it_shows_current_player(self) -> None:
        pass

    def it_shows_hearts_broken_status(self) -> None:
        pass

    def it_shows_valid_actions(self) -> None:
        pass


class DescribeInputParser:
    """Parses user text input into PlayerAction."""

    def it_parses_card_play(self) -> None:
        pass

    def it_parses_pass_selection(self) -> None:
        pass

    def it_parses_moon_choice_add(self) -> None:
        pass

    def it_parses_moon_choice_subtract(self) -> None:
        pass

    def it_rejects_invalid_input(self) -> None:
        pass

    def it_is_case_insensitive(self) -> None:
        pass

    def it_accepts_suit_symbols_and_letters(self) -> None:
        pass
