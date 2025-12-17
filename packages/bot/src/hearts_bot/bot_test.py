"""Tests for Hearts bot."""


class DescribeBot:
    def it_returns_valid_action_for_any_state(self) -> None:
        pass

    def it_chooses_pass_in_passing_phase(self) -> None:
        pass

    def it_chooses_play_in_playing_phase(self) -> None:
        pass

    def it_chooses_moon_option_in_round_end(self) -> None:
        pass


class DescribePassSelection:
    def it_selects_exactly_three_cards(self) -> None:
        pass

    def it_passes_queen_of_spades_when_held(self) -> None:
        pass

    def it_passes_high_spades_to_avoid_taking_queen(self) -> None:
        pass

    def it_passes_high_hearts(self) -> None:
        pass

    def it_avoids_passing_low_cards(self) -> None:
        pass

    def it_prefers_voiding_short_suits(self) -> None:
        pass


class DescribeCardSelection:
    def it_leads_two_of_clubs_on_first_trick(self) -> None:
        pass

    def it_follows_suit_when_able(self) -> None:
        pass

    def it_dumps_queen_of_spades_when_cannot_follow(self) -> None:
        pass

    def it_dumps_high_hearts_when_cannot_follow(self) -> None:
        pass

    def it_avoids_taking_tricks_with_points(self) -> None:
        pass

    def it_avoids_leading_hearts_until_broken(self) -> None:
        pass

    def it_avoids_leading_queen_of_spades_early(self) -> None:
        pass


class DescribeMoonShooting:
    def it_detects_moon_opportunity_from_tricks_taken(self) -> None:
        pass

    def it_takes_points_aggressively_when_shooting(self) -> None:
        pass

    def it_adds_to_others_when_ahead(self) -> None:
        pass

    def it_subtracts_from_self_when_behind(self) -> None:
        pass
