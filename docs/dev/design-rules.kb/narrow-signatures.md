# Narrow Signatures

Functions should accept the minimal data they need, not entire state objects.

## Motivation

- **Explicit dependencies**: Signature shows exactly what the function uses
- **Reduced coupling**: Function doesn't depend on unrelated state structure
- **Testability**: Easier to construct minimal test inputs
- **Reusability**: Function works in more contexts

## Pattern

```python
# Avoid: takes full state, uses two fields
def can_lead_hearts(state: GameState) -> bool:
    if state.hearts_broken:
        return True
    hand = state.players[state.current_player].hand
    return not hand.not_of_suit(Suit.HEARTS)

# Prefer: takes only what it needs
def can_lead_hearts(hand: Hand, hearts_broken: bool) -> bool:
    if hearts_broken:
        return True
    return not hand.not_of_suit(Suit.HEARTS)
```

## When to Apply

Always. Every function takes only what it uses. No exceptions for
"orchestration" or "convenience."

If extraction patterns repeat at call sites, that's a signal to create a helper
or reconsider the data model—not to widen the signature.
