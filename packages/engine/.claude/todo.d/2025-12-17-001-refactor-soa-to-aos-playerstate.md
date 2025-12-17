# Refactor: SOA → AOS with PlayerState

## Summary

Factor out `PlayerId` entirely by transforming parallel arrays (Structure of
Arrays) into a single `list[PlayerState]` (Array of Structures).

## Current State (SOA)

```python
# GameState has parallel arrays indexed by implicit PlayerId (0-3)
hands: list[Hand]
scores: list[int]
round_scores: list[int]
tricks_won: dict[PlayerId, list[Trick]]

# PlayerId is Literal[0, 1, 2, 3] - just an index
```

## Proposed State (AOS)

```python
@dataclass
class PlayerState:
    player: Player | None  # the actor (None until assigned)
    hand: Hand
    score: int
    round_score: int
    tricks_won: list[Trick]

# GameState has single list
players: list[PlayerState]  # len == 4, indexed 0-3
```

## Benefits

1. All player-related state grouped together
2. No parallel arrays that could get out of sync
3. `Player` (actor) directly associated with its state
4. Clearer ownership model

## Considerations

- `current_player`, `lead_player` become indices (int) or direct `PlayerState`
  references
- `Trick` currently `dict[PlayerId, Card]` - options:
  - `list[tuple[int, Card]]` with player index
  - `list[Card]` if we track lead separately (cards in play order)
  - Keep dict but use int keys
- Serialization implications if using references vs indices

## Related

- `Player` protocol in `player.py` - the actor interface
- `Trick` type in `card.py` - currently `dict[PlayerId, Card]`
