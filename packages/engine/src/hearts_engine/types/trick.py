"""Trick type."""

from collections.abc import Iterator
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from .card import Card
from .card import Suit
from .player import PLAYER_IDS
from .player import PlayerId


@dataclass(frozen=True, slots=True)
class Trick:
    """Cards played in a trick, indexed by player position 0-3."""

    lead: PlayerId
    cards: tuple[Card | None, Card | None, Card | None, Card | None] = (
        None,
        None,
        None,
        None,
    )

    def __getitem__(self, player: PlayerId) -> Card | None:
        return self.cards[player]

    @property
    def lead_suit(self) -> Suit | None:
        """Suit of the lead card, or None if trick is empty."""
        lead_card = self.cards[self.lead]
        return lead_card.suit if lead_card else None

    def __len__(self) -> int:
        """Number of cards played (non-None slots)."""
        return sum(1 for c in self.cards if c is not None)

    def items(self) -> Iterator[tuple[PlayerId, Card]]:
        """Yield (player_id, card) pairs for played cards."""
        for pid, card in zip(PLAYER_IDS, self.cards):
            if card is not None:
                yield pid, card

    def values(self) -> Iterator[Card]:
        """Yield cards that have been played."""
        for card in self.cards:
            if card is not None:
                yield card

    def with_play(self, player: PlayerId, card: Card) -> Self:
        """Return a new Trick with the given card added."""
        cls = type(self)
        c = self.cards
        match player:
            case 0:
                cards = (card, c[1], c[2], c[3])
            case 1:
                cards = (c[0], card, c[2], c[3])
            case 2:
                cards = (c[0], c[1], card, c[3])
            case 3:
                cards = (c[0], c[1], c[2], card)
        return cls(lead=self.lead, cards=cards)

    @classmethod
    def from_dict(cls, plays: Mapping[PlayerId, Card], lead: PlayerId) -> Self:
        return cls(
            cards=(plays.get(0), plays.get(1), plays.get(2), plays.get(3)),
            lead=lead,
        )
