# Moon Shooter's Choice

## Context

Different Hearts variants handle shooting the moon differently:
- Shooter gets -26
- Everyone else gets +26
- Shooter chooses

## Decision

Shooter chooses between -26 for self or +26 for opponents.

## Rationale

- Adds strategic depth (decision after capturing all points)
- Common in serious play
- More interesting than automatic -26

## Consequences

- UI needs choice prompt after moon shot detected
- Slight complexity in scoring logic
- Better gameplay for competitive players
