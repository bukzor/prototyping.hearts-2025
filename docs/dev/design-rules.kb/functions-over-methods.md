# Functions Over Methods

Prefer free functions to methods. They're more honest about dependencies and
easier to refactor.

## Why Functions Win

- **Symmetric arguments**: `f(a: A, b: B)` treats both types as peers. Making it
  `a.f(b)` falsely privileges A as the "owner."
- **Narrow signatures**: Functions naturally take only what they need. Methods
  implicitly take all of `self`.
- **Refactoring**: Narrowing a function signature is trivial. Extracting a
  method out of a class is painful.
- **Testing**: Functions with explicit arguments are easier to test in
  isolation.

## When Methods Make Sense

See `alternate-constructors.md` and `single-arg-methods.md` for the exceptions.

## Example

```python
# Good: function takes what it needs
def trick_winner(trick: Trick, lead_player: PlayerId) -> PlayerId: ...

# Avoid: method privileges one argument
class Trick:
    def winner(self, lead_player: PlayerId) -> PlayerId: ...
```

Both arguments are peers. Neither "owns" the operation.
