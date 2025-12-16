# Renderers

Client-side UI and graphics.

|              | POC              | Production               |
| ------------ | ---------------- | ------------------------ |
| UI framework | Preact           | Preact or Dioxus (TBD)   |
| Scene graph  | (not needed yet) | Babylon.js or Bevy (TBD) |
| Graphics API | Canvas/WebGL     | WebGPU or wgpu (TBD)     |

## Notes

- TypeScript renderer may persist into production (Rust server + TS client is
  proven)
- Preact chosen for POC: React API in 3kb, excellent TypeScript support, same
  patterns
- Babylon.js is an option if we need WebGPU scene graph in TS
- Dioxus is React-like in Rust; Bevy provides scene graph + wgpu

## Why Preact over React

- 3kb vs 40kb
- `class` instead of `className`
- Native DOM events (no synthetic event overhead)
- Same API, same JSX, same hooks — React-compatible via `preact/compat`
- Excellent TypeScript types (same JSX.IntrinsicElements as React)

## Speculative Rust Analogies

If a Rust client becomes necessary:

| TypeScript   | Rust   |
| ------------ | ------ |
| Preact/React | Dioxus |
| Babylon.js   | Bevy   |
| Canvas/WebGL | wgpu   |

## Prior Exploration

There was discussion of using Godot as scene editor with Bevy as wgpu runtime
glue. This remains a possible future direction but is not committed.
