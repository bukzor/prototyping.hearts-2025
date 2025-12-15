# 2025-12-15: Stack Refinement

## Focus

Finalizing v0 tech stack with emphasis on what transfers to production and what enables Claude productivity.

## What Happened

Revisited ADR-002 (FastAPI + htmx) decision. Key realization: htmx patterns don't transfer to wgpu mental model, and the production client is "thin wrapper loading shaders" — renderer choice matters more than initially thought.

Discussion explored:
- htmx vs React vs Babylon.js vs vanilla TS
- wgpu scene graph options (Bevy, Vello, Dioxus)
- Remembered prior discussions: Dioxus (React-like in Rust), Babylon.js (WebGPU-first scene graph), Bevy (wgpu glue)

Landed on: **TypeScript renderer is a keeper**, not throwaway. The real architecture is:
- `GameState → pixels` contract enables renderer swapping
- Same interface supports CLI, Preact, Babylon, or future Bevy
- Engine/server abstractions transfer; renderer is swappable

Further refinement:
- For a000, pure Python is simpler — no need for two languages yet
- Web renderer (Preact + Vite) deferred to a010
- Preact chosen over React: same API, 3kb, better TS types, `class` not `className`

Renamed `rust-python-analogues.kb/` to `tool-equivalence-classes.kb/` — broader scope, organized by capability not language pair.

## Decisions Made

- **ADR-008**: TypeScript renderer (supersedes ADR-002 htmx choice)
- **ADR-009**: Renderer-agnostic architecture (GameState/PlayerAction interface)
- **a000 scope**: Pure Python CLI, no server, no web UI
- **a010 scope**: FastAPI + Preact web renderer

## Artifacts Created

- `docs/dev/gamestate-interface.md` — Interface spec with types + Preact conventions
- `docs/milestones.kb/a000-local-prototype.md` — Renamed from a001, pure Python CLI
- `docs/milestones.kb/a010-web-renderer.md` — Web UI milestone
- `docs/rules.kb/the-rest-are-mine.md` — TRAM rule (deferred to b/v series)
- `docs/tool-equivalence-classes.kb/renderers.md` — Preact/Dioxus/Bevy analogues

## Next Session

**Start implementing a000:**

1. Set up uv workspace with packages: `engine`, `bot`, `renderer-cli`
2. Implement `engine/` — cards, hands, tricks, rules, scoring
3. Implement `renderer-cli/` — display GameState, accept PlayerAction input
4. Implement `bot/` — a000 heuristics
5. Wire together and playtest

**Key discipline:** Renderer never imports engine internals. Engine computes `validActions`, renderer just displays them.
