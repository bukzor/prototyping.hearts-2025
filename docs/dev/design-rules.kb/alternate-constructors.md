# Alternate Constructors

Factory functions that return a type should be classmethods on that type.

## Pattern

```python
# Avoid: free function that returns a type
def card_from_string(s: str) -> Card: ...
def trick_from_dict(plays: Mapping[PlayerId, Card]) -> Trick: ...

# Prefer: classmethod on the type
class Card:
    @classmethod
    def from_string(cls, s: str) -> Card: ...

class Trick:
    @classmethod
    def from_dict(cls, plays: Mapping[PlayerId, Card]) -> Trick: ...
```

## Benefits

- **Discoverability**: `Card.` autocomplete shows all ways to create a Card
- **Namespacing**: No need for `card_` prefix on function names
- **Consistency**: Follows Python conventions (`dict.fromkeys()`,
  `datetime.fromisoformat()`)

## When Free Functions Make Sense

- Factory spans multiple types (returns Union, picks type based on input)
- Module-level convenience that wraps multiple constructors
