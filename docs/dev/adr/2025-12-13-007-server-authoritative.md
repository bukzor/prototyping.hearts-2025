# Server-Authoritative Architecture

## Context

Multiplayer card games are vulnerable to cheating if clients have access to hidden information (other players' hands).

## Decision

Server is the single source of truth. Clients are "dumb terminals."

- All game state lives on server
- Client only receives: own hand, played cards, scores, whose turn
- Client sends: selected card to play, selected cards to pass
- Server validates all moves before applying
- Illegal moves rejected (client bug or cheat attempt)

## Rationale

- Anti-cheat by design (can't see what you don't receive)
- Simplifies client (no game logic needed)
- Spectators can't leak info (they see same as players)
- Consistent state (no sync issues)

## Consequences

- All game logic in `engine` package on server
- Client is pure UI
- Latency affects feel (but card games are slow anyway)
- Works naturally with pass-the-controller (single client)
