# Bots

AI opponents for practice and testing.

## Use Cases

1. **Playtesting** - Developers test game mechanics
2. **Practice** - Players learn without pressure
3. **Fill seats** - Unrated games only

## Constraints

- Bots NEVER participate in rated/ranked games
- Disconnect in rated game = forfeit, no bot substitution
- Bot games clearly marked as unrated

## AI Levels

Start simple (legal random play + basic heuristics), improve over time.
Opt-in only - players choose to include bots.

## Architecture

Separate package/crate from game engine. Clean interface.
