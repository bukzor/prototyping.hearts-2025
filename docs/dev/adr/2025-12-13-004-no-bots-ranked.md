# No Bots in Ranked Play

## Context

Competitive integrity is core to the product. "Fry or be fried."

## Decision

Bots NEVER participate in rated/ranked games. Period.

- Disconnect = forfeit (no bot substitution)
- Bot games always unrated
- Bot presence clearly marked

## Rationale

- Rated games must reflect human skill
- Bot skill level would distort ratings
- Players deserve to know they're playing humans
- Competitive players will leave if integrity compromised

## Consequences

- Disconnects hurt more (no graceful degradation)
- Need robust reconnection logic
- May lose casual players who want bot fill-in
- This is acceptable - we target competitive players
