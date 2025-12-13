---
last-updated: 2025-12-13
---

# Hearts Online

The "best" Hearts game for competitive players who want a community and serious play.

## Vision

Enable lovers of Hearts to have a dedicated community and high-quality game experience.
Target: competitive players. Philosophy: "fry or be fried" - no dumbing down.

## Platforms

- Web (browser client)
- Android
- iOS
- Desktop (Steam)

## Technical Approach

1. **POC Phase**: Python (FastAPI + htmx), localhost, rapid iteration
2. **Production**: Rust backend + wasm+wgpu client
3. **Architecture**: Monorepo with separate packages (engine, bot, server, client)

## Key Constraints

- Bots never affect ranked play (forfeit on disconnect, no seat-filling)
- Synchronous play only (no async/correspondence)
- Monetization doors kept open (free/ads/premium/cosmetics) but not implemented initially

## Status

Alpha development. See `milestones.kb/` for current progress.
