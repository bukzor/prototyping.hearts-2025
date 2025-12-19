# Structural Consistency

Parallel data structures should use parallel types.

## Pattern

```python
# Avoid: mixed structures for same-shaped data
hands: tuple[Hand, Hand, Hand, Hand]      # tuple
scores: tuple[int, int, int, int]         # tuple
tricks_won: dict[PlayerId, list[Trick]]   # dict of lists (!!)

# Prefer: uniform structure
hands: tuple[Hand, ...]
scores: tuple[int, ...]
tricks_won: tuple[tuple[Trick, ...], ...]
```

## Why It Matters

Inconsistent structures signal unclear modeling. If four players each have
tricks, that's four collections—not a dict. The dict says "sparse lookup" when
you mean "indexed by player."

## Fix

When you spot structural inconsistency, ask: what's the actual relationship?
Usually the answer is "one per entity"—which means colocate it in the entity
struct.
