# Lazy Iteration

Return iterators instead of eagerly building collections.

## Preference Order

```
Iterator > tuple > list
```

- **Iterator**: Lazy, composable, memory-efficient
- **tuple**: Immutable, hashable, fixed-size
- **list**: Only when mutation or random access is required

## Pattern

```python
# Avoid: builds list eagerly
def valid_plays(state: GameState) -> list[Card]:
    return [c for c in hand if is_valid(c)]

# Prefer: yields lazily
def valid_plays(state: GameState) -> Iterator[Card]:
    return (c for c in hand if is_valid(c))

# Or with yield for complex logic
def valid_plays(state: GameState) -> Iterator[Card]:
    for card in hand:
        if is_valid(card):
            yield card
```

## Benefits

- **Early termination**: Callers can stop iteration early
- **Composition**: Chain filters without intermediate allocations
- **Memory**: No temporary collections for large datasets

## When to Materialize

Callers materialize when they need:

- Random access: `list(valid_plays(state))[0]`
- Multiple passes: `cards = tuple(valid_plays(state))`
- Length: `len(list(valid_plays(state)))`

Let the caller decide; don't assume they need a collection.
