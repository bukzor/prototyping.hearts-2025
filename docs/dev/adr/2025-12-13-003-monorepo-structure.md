# Monorepo with Separate Packages

## Context

Need a project structure that scales and mirrors eventual Rust implementation.

## Decision

uv workspace monorepo with separate Python packages:

- `engine` - pure game logic, no I/O
- `bot` - AI opponents
- `server` - web server, networking
- `client` - (future) wasm client

## Rationale

- Clean separation of concerns
- Engine testable in isolation
- Bot swappable/optional
- Maps directly to cargo workspace with crates

## Consequences

- More boilerplate than single package
- Import paths slightly longer
- Worth it for architectural clarity
