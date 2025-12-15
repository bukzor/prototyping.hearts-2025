# Renderers

Client-side UI and graphics.

| | POC | Production |
|-|-----|------------|
| UI framework | React | React or Dioxus (TBD) |
| Scene graph | (not needed yet) | Babylon.js or Bevy (TBD) |
| Graphics API | Canvas/WebGL | WebGPU or wgpu (TBD) |

## Notes

- TypeScript renderer may persist into production (Rust server + TS client is proven)
- React chosen for POC due to widget ecosystem
- Babylon.js is an option if we need WebGPU scene graph in TS
- Dioxus is React-like in Rust; Bevy provides scene graph + wgpu

## Speculative Rust Analogies

If a Rust client becomes necessary:

| TypeScript | Rust |
|------------|------|
| React | Dioxus |
| Babylon.js | Bevy |
| Canvas/WebGL | wgpu |

## Prior Exploration

There was discussion of using Godot as scene editor with Bevy as wgpu runtime glue. This remains a possible future direction but is not committed.
