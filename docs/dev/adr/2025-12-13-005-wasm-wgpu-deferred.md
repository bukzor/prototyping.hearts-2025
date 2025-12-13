# wasm+wgpu for Production Client (Deferred)

## Context

Want Rust everywhere, including client. wasm+wgpu enables this.

## Decision

Target wasm+wgpu for production client, but defer to post-POC.

POC uses simple HTML/htmx. Production rewrites client in Rust.

## Rationale

- wgpu enables rich visuals, animations, shaders
- Same language (Rust) for client and server
- Code sharing possible (game logic)
- But: heavyweight for 5-day POC
- Validate gameplay first, polish later

## Consequences

- POC client is throwaway
- Need to learn wgpu (developer is Rust novice)
- Production timeline extends
- Worth it for cross-platform native feel
