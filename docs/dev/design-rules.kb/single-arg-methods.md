# Single-Argument Methods

A function of one composite type _may_ become a method—but only under strict
conditions.

## Requirements

All three must hold:

1. **Single argument**: Function takes exactly one composite type from this
   project (primitives like `int`, `bool` don't count)
2. **Uses all fields**: The function genuinely needs every field of the type
3. **Stable interface**: No foreseeable refactor would narrow the signature

## Why So Strict?

If a function only uses _some_ fields, it should take those fields directly (see
`narrow-signatures.md`). Making it a method hides this and makes future
narrowing harder.

## Example

```python
# Candidate: uses all fields of Hand?
def is_empty(hand: Hand) -> bool:
    return len(hand) == 0

# But Hand is a frozenset—len() is inherited.
# This doesn't "use all fields" in a meaningful way.
# Keep as function or use inherited __bool__.
```

## When In Doubt

Keep it a function. Promoting to method is easy later if warranted; demoting is
painful.
