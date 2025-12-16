--- # workaround: anthropics/claude-code#13003
requires:
    - Skill(llm.kb)
    - Skill(llm-collab)
---

# Hearts Online

Multiplayer Hearts card game for competitive players.

## Quick Orient

- `docs/` - Project knowledge base (start here)
- `docs/README.md` - Vision and overview
- `docs/milestones.kb/a000-local-prototype.md` - Current milestone
- `docs/dev/adr/` - Architecture decisions

## Current State

POC phase. Building Python prototype to validate game mechanics before Rust
rewrite.

## Key Context

**Product positioning:** "Mental exercise" for serious players. "Fry or be
fried" - no hand-holding.

**Expert user:** The developer's partner is a Hearts enthusiast who will
validate gameplay feel and drive UI decisions during testing.

**Strategic context:** This is one of several POC prototypes to "see what
sticks." Common thread: web interface repackaged for mobile/desktop with
micropayments.

**Urgency:** a000 target is ~5 days to first playable version.

## Tech Stack (POC)

- Python + uv workspace
- FastAPI + Preact/TypeScript renderer
- Packages: engine, bot, server (mirrors eventual Rust crates)

## What to Build Next

See `docs/milestones.kb/a000-local-prototype.md` for scope. Key deliverable:
4-player pass-the-controller Hearts game in single browser.
