---
status: active
---

# a000: Local Prototype

First playable version. Validates core game loop.

## Goals

- Play a complete game of Hearts that feels right
- Test game logic correctness
- Show someone else and they understand what this will become

## Scope

**In:**
- Pure Python (no server, engine via import)
- Python CLI renderer
- [Pass-the-controller](../features.kb/pass-the-controller.md) multiplayer (4 players, 1 terminal)
- [Core rules](../rules.kb/) only (no JD variant)
- Basic [bot](../features.kb/bots.md) for playtesting (simple heuristics, opt-in)

**Out:**
- Networking
- Authentication
- Multiple browser sessions
- Optional rules
- Time controls
- Any UI polish

## Tech Stack

- Python 3.x with uv
- Python CLI renderer (no web UI in a000)
- Monorepo structure mimicking eventual Rust crates
- Renderer-agnostic: [GameState/PlayerAction interface](../dev/gamestate-interface.md)

## Package Structure

```
packages/
├── engine/           ← game rules, state
├── bot/              ← AI player
├── renderer-cli/     ← Python CLI, a000 primary
```

Server and web renderer (Preact/TS) deferred to a010.

## Success Criteria

Complete a 4-player game to 100 points with no rule violations.

## Getting Started

1. Set up uv workspace (see [project-structure](../tool-equivalence-classes.kb/project-structure.md))
2. Implement `engine/` — cards, hands, tricks, [rules](../rules.kb/), [scoring](../rules.kb/scoring.md)
3. Implement `renderer-cli/` — display [GameState](../dev/gamestate-interface.md), accept input
4. Implement `bot/` — [a000 heuristics](../features.kb/bots.md)
5. Wire together and play test
