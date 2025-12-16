# Renderer-Agnostic Architecture

## Context

Multiple renderer targets exist:

- POC: React/Canvas or Babylon.js (TypeScript)
- Testing: CLI, curses
- Production: Possibly keep TS, possibly Bevy/wgpu (Rust)

Need architecture that survives renderer revolutions.

## Decision

Strict separation: engine owns game logic, renderer owns pixels. Interface is
data.

```
Engine ──► GameState ──► Renderer (black box)
              │
              ▼
Renderer ──► PlayerAction ──► Engine
```

**GameState contract (engine → renderer):**

- Pure data, no behavior
- Includes derived state (validActions, playableCards)
- Renderer never computes game logic

**PlayerAction contract (renderer → engine):**

- Intents, not mutations
- Engine validates and applies

**What this enables:**

```
engine/     ← Python → Rust (transfers)
server/     ← Python → Rust (transfers)
bot/        ← Python → Rust (transfers)
renderer/   ← TypeScript (keeps, swappable)
```

## Rationale

The test for a good boundary: can you play a full game via stdin/stdout?

```
> state
{"hands":[[...]], "trick":[], "currentPlayer":0}

> action {"type":"pass_cards","cards":["2H","3H","4H"]}
{"ok":true}
```

If CLI works, any renderer works.

## Consequences

- GameState shape is a first-class design artifact
- "Is this card playable?" lives in engine, not renderer
- Animation state is renderer-local, not in GameState
- Multiple renderers can coexist (web + CLI for testing)

## Analogies (if Rust client needed)

| TypeScript   | Rust (speculative) |
| ------------ | ------------------ |
| React        | Dioxus             |
| Babylon.js   | Bevy               |
| Canvas/WebGL | wgpu               |
| Scene graph  | Entity hierarchy   |

Note: TypeScript renderer may persist into production. These analogies are for
reference if a Rust client becomes necessary.
