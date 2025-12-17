---
status: planned
---

# a010: Web Renderer

Web UI for browser-based play.

## Prerequisites

- a000 complete (CLI playable, engine validated)

## Goals

- Play Hearts in a browser
- Same pass-the-controller mode, nicer UI
- Validate GameState/PlayerAction interface works over HTTP

## Scope

**In:**

- FastAPI server
- Preact + TypeScript + Vite renderer
- Localhost only, single browser
- Pass-the-controller multiplayer

**Out:**

- Networking (multiple clients)
- Authentication
- Persistent state

## Tech Stack

- FastAPI for backend
- Preact + TypeScript + Vite for renderer-web
- GameState as JSON over HTTP/WebSocket

## Notes

- Unicode playing card glyphs (U+1F0A0 block) may work well here - can size via
  CSS unlike CLI where they're fixed to terminal font size

## Package Structure

```
packages/
├── engine/           ← from a000
├── bot/              ← from a000
├── renderer-cli/     ← from a000
├── server/           ← new: FastAPI
├── renderer-web/     ← new: Preact/TS
```
