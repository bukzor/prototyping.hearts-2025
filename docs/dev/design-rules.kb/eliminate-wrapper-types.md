# Eliminate Wrapper Types

Remove types that exist only to hold other types without adding behavior.

## Pattern

```python
# Avoid: wrapper adds nothing
@dataclass
class Play:
    player: PlayerId
    card: Card

trick: list[Play]

# Prefer: direct representation
trick: dict[PlayerId, Card]
```

## When Wrappers Are Worth Keeping

A wrapper earns its place when it:

- Enforces invariants (constructor validates)
- Provides domain-specific methods
- Has identity beyond its fields
- Improves type safety at API boundaries

## Judgment Call

If you remove a wrapper and the code gets _harder_ to read, the wrapper was
carrying meaning. Put it back—or evolve it into something richer.
