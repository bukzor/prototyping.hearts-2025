# Immutability

All stored state must be immutable. This enables undo/replay, simplifies
reasoning, and prevents hidden mutation bugs.

## Requirements

### Dataclasses

All dataclasses must be `@dataclass(frozen=True, slots=True)`.

### Collections in Dataclass Fields

- `list` → `tuple`
- `set` → `frozenset`
- `dict` → `tuple` of pairs, or redesign

### State Mutation

Functions that "mutate" state must return new state:

```python
def complete_trick(state: GameState) -> GameState:
    # ... compute changes ...
    return replace(state, trick=Trick(), lead_player=winner)
```

Never mutate in-place, even on a copy.

## Exceptions

### Local Variables

Mutable collections as local accumulators are fine:

```python
received: dict[PlayerId, list[Card]] = {0: [], 1: [], 2: [], 3: []}
```

These are consumed within the function, never stored.

### Function Parameters

Use abstract read-only types to signal intent:

- `Mapping` instead of `dict`
- `Sequence` instead of `list`
- `AbstractSet` instead of `set`
