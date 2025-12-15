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

Start simple, improve over time. Opt-in only.

### a000 Bot (Minimal)

Basic heuristics for playtesting:

- Follow suit if able (required by rules)
- Avoid leading QoS early
- Dump high hearts when can't follow
- Pass high spades (Q, K, A) and high hearts
- If shooting moon looks possible, commit to it

Not smart, but exercises all game paths.

## Architecture

Separate package/crate from game engine. Clean interface.
