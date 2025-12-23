# Method Argument Rules

Methods with arguments beyond `self` must return `Self`.

## The Rule

A method may:

1. **Take only `self`** — accessor/query, any return type
2. **Take additional args** — but must return `Self` (fluent/builder pattern)

If a method takes args and returns something other than `Self`, it should be a
standalone function.

## Why?

- **Fluent methods** like `cards.of_suit(suit) -> Self` compose naturally
- **Non-Self returns** with args treat `self` as privileged when it's really a
  peer (see `functions-over-methods.md`)
- **Explicit dependencies** — functions show what they actually need

## Examples

```python
# Good: takes only self
def __len__(self) -> int: ...
@property
def lead_suit(self) -> Suit | None: ...

# Good: takes args, returns Self
def of_suit(self, suit: Suit) -> Self: ...
def with_play(self, player: PlayerId, card: Card) -> Self: ...

# Bad: takes args, returns non-Self — should be function
def deal_hands(self, rng: Random) -> Iterator[Hand]: ...  # NO
def deal_hands(deck: Deck, rng: Random) -> Iterator[Hand]: ...  # YES
```

## When In Doubt

Keep it a function. Promoting to method is easy; demoting is painful.
