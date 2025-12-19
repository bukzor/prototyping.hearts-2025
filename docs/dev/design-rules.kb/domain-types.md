# Domain Types Over Primitives

Prefer specific types over generic ones. `UserId` over `int`, `Email` over
`str`, `OrderItems` over `list[tuple[str, int]]`.

## Why

- **Readability**: `def send(to: Email, msg: Body)` beats
  `def send(to: str, msg: str)`
- **Type checking**: Pyright catches `send(body, email)` vs `send(email, body)`
  when types differ
- **Agents and editors**: Autocomplete and docs work better with named types
- **Refactoring**: Change the representation without changing the API

## Pattern

```python
# Avoid: primitives everywhere
def create_order(items: list[tuple[str, int]], user: int) -> dict: ...

# Prefer: domain types
def create_order(items: OrderItems, user: UserId) -> Order: ...
```

## Minimum Viable Types

Even a simple alias helps:

```python
Priority = Literal["low", "medium", "high"]  # Better than raw str
```

Subclass for type distinction, methods, or validation:

```python
class Email(str):
    """Validated email address."""
    pass  # Empty is fine—type distinction is the value
```

## When Primitives Are Fine

- Truly generic utilities (`len`, `sum`, `sorted`)
- Local variables with obvious meaning
- Interfacing with external APIs that use primitives
