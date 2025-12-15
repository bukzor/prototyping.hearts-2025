# Python for POC, Rust for Production

## Context

Building a cross-platform multiplayer Hearts game. Need to validate game mechanics
and architecture quickly before committing to production implementation.

Developer is expert in Python, novice in Rust.

## Decision

Use Python for the proof-of-concept phase, then reimplement in Rust for production.

- POC: Python with FastAPI + htmx
- Production: Rust backend + wasm+wgpu client

Maintain strong analogies between Python and Rust implementations:
- uv monorepo structure mirrors cargo workspace
- Separate packages mirror eventual crates (engine, bot, server, client)
- Property-based tests (hypothesis) map to proptest

## Consequences

**Accepted trade-offs:**
- Will rewrite code (but architecture carries over)
- Python patterns may not map 1:1 to Rust
- Need to maintain tool-equivalence-classes.kb/ to track mappings

**Benefits:**
- Faster iteration in familiar language
- Architecture validated before Rust learning curve
- Can show working prototype sooner
