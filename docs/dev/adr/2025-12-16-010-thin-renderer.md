# Thin Renderer Architecture

## Context

Building CLI renderer and bot. Need to decide where logic lives.

Multiple renderers anticipated: CLI (log-style), CLI (ncurses), web. Bot and
human players need uniform interface.

## Decision

### 1. Renderer is a thin I/O adapter

All formatting, parsing, sorting, and grouping logic lives in engine. Renderer
only handles:

- Output mechanism (`print()` vs `addstr()` vs DOM)
- Input mechanism (`input()` vs `getch()` vs event handlers)
- Layout decisions (what order, where on screen)
- Prompt strings

### 2. `__tty__` protocol for colored terminal output

Engine types implement `__tty__()` for ANSI-colored representation:

```python
# hearts_engine/tty.py
@runtime_checkable
class SupportsTTY(Protocol):
    def __tty__(self) -> str: ...

def format(obj: object, *, tty: bool | None = None) -> str:
    if tty is None:
        tty = sys.stdout.isatty()
    if tty and isinstance(obj, SupportsTTY):
        return obj.__tty__()
    return str(obj)
```

- `__str__` = plain text (logs, pipes, tests)
- `__tty__` = ANSI-colored (interactive terminal)

### 3. `Player` protocol for bot/human uniformity

```python
# hearts_engine/player.py
class Player(Protocol):
    def choose_action(self, state: GameState) -> PlayerAction: ...
```

- Bot implements via heuristics
- Human implements via render + prompt (per-renderer)
- Game loop is uniform: `players[current].choose_action(state)`

## Consequences

**Engine gains:**

- `tty.format()` function
- `Card.__tty__()`, etc.
- `sort_hand()`, `group_hand()`
- `Card.parse()` (inverse of `__str__`)
- `Player` protocol

**Renderer contains only:**

- I/O glue
- Layout/sequencing
- `Human` class implementing `Player`

**Testing:**

- Formatting/parsing tests live in engine
- Renderer tests are integration tests (output shape, input handling)

## Rationale

If code is shared between CLI and ncurses renderers, it's not
presentation-specific — it's domain logic. Push it down to engine.

This extends ADR-009 (renderer-agnostic architecture): the boundary is data, and
now also protocols.
