# TypeScript Renderer (Supersedes ADR-002)

## Context

ADR-002 chose htmx for fast iteration. After discussion, realized:

1. Production client is wasm+wgpu, not server-rendered HTML
2. htmx patterns don't transfer to wgpu mental model
3. TypeScript renderer could be a *keeper*, not throwaway
4. Renderer-agnostic architecture enables multiple frontends (web, CLI, curses)

## Decision

Replace htmx with TypeScript renderer. Keep FastAPI backend.

**POC stack:**
- Python engine/server/bot (unchanged)
- TypeScript renderer (Vite build)
- JSON over HTTP/WebSocket for state sync

**Key insight:** If renderer consumes `GameState` and emits `PlayerAction`, the renderer is swappable. Same interface supports:
- React (POC) — rich widget ecosystem
- Babylon.js (future option if we need WebGPU)
- CLI/curses (testing)
- Rust client (future, if needed — Bevy is a fair guess)

## Rationale

- TypeScript renderer likely survives into production (Rust server + TS client is proven pattern)
- Babylon.js ↔ Bevy is a meaningful analogy (scene graph + WebGPU/wgpu)
- Dioxus (Rust) ↔ React (TS) is a meaningful analogy (component model)
- Building transferable skills, not throwaway code

## Consequences

- Added build step (Vite)
- Must define clean GameState/PlayerAction interface (good forcing function)
- Renderer is a real package, not just templates
- CLI renderer becomes viable for testing/CI

## Addendum: Prior Exploration

There was an idea of using Godot as scene editor / retained scene graph with Bevy as the wgpu runtime glue. This remains a possible future direction for a Rust client, but TypeScript renderer may persist well into production — Rust server + TS client is a proven pattern.
