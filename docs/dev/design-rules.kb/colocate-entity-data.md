# Colocate Entity Data

Group all per-entity fields into a single struct rather than maintaining
parallel collections.

## Pattern

```python
# Avoid: parallel arrays
hands: tuple[Hand, ...]
scores: tuple[int, ...]
round_scores: tuple[int, ...]

# Prefer: per-entity struct
@dataclass
class PlayerState:
    hand: Hand
    score: int
    round_score: int

players: tuple[PlayerState, ...]
```

## Benefits

- **Locality**: Related data accessed together
- **Extensibility**: Adding a field is one change, not N
- **Invariants**: Impossible to have mismatched lengths

## When Parallel Arrays Make Sense

- Bulk operations on one field (SIMD, vectorization)
- Memory layout critical for performance
- Fields have very different access patterns
