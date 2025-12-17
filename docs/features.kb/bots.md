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

## Sophistication Levels

See [bots.kb/](bots.kb/) for detailed level descriptions.

| Level                            | Name       | Summary                                    |
| -------------------------------- | ---------- | ------------------------------------------ |
| [000](bots.kb/000-random.md)     | Random     | Random valid play                          |
| [010](bots.kb/010-basic.md)      | Basic      | Simple heuristics, no memory (a000 target) |
| [030](bots.kb/030-counting.md)   | Counting   | Tracks cards played                        |
| [050](bots.kb/050-tactical.md)   | Tactical   | Opponent modeling, moon awareness          |
| [070](bots.kb/070-analytical.md) | Analytical | Probability, simulation, lookahead         |
| [090](bots.kb/090-optimal.md)    | Optimal    | Near-optimal (aspirational)                |

## Architecture

- Separate package/crate from game engine
- Implements `Player` protocol (shared with human input)
- `choose_action(state: GameState) -> PlayerAction`
