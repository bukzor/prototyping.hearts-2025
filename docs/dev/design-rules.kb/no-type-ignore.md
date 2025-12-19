# No Type Ignore

Avoid `# type: ignore` comments. They hide real issues and erode type safety.

Every `type: ignore` indicates a pending task to fix the underlying type issue.

## Strategies

### Use `zip(PLAYER_IDS, ...)` instead of `enumerate`

```python
# Avoid: enumerate returns int, not PlayerId
for i, player in enumerate(players):
    return i  # type: ignore[return-value]

# Prefer: zip with typed constant
for pid, player in zip(PLAYER_IDS, players):
    return pid  # no ignore needed
```

### Fix return types at the source

```python
# Avoid: ignoring at call site
holder: PlayerId = find_holder(players)  # type: ignore[assignment]

# Prefer: fix the function signature
def find_holder(players: ...) -> PlayerId:  # not int
```

### Use helper functions for arithmetic

```python
# Avoid: arithmetic on Literal types
next_player = (player + 1) % 4  # type: ignore[assignment]

# Prefer: helper that encapsulates the cast
next_player = next_player_id(player)
```
