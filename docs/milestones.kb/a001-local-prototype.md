---
status: active
---

# a001: Local Prototype

First playable version. Validates core game loop.

## Goals

- Play a complete game of Hearts that feels right
- Test game logic correctness
- Show someone else and they understand what this will become

## Scope

**In:**
- Python backend (FastAPI)
- TypeScript renderer (Vite)
- Localhost only, single browser
- Pass-the-controller multiplayer (4 players, 1 screen)
- Core rules only (no JD variant)
- Basic bot for playtesting (simple heuristics, opt-in)
- CLI renderer for testing

**Out:**
- Networking
- Authentication
- Multiple browser sessions
- Optional rules
- Time controls
- Any UI polish

## Tech Stack

- Python 3.x with uv
- FastAPI for backend
- TypeScript + Vite for renderer
- Monorepo structure mimicking eventual Rust crates
- Renderer-agnostic: GameState/PlayerAction interface (see ADR-009)

## Success Criteria

Complete a 4-player game to 100 points with no rule violations.
