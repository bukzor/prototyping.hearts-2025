# 000: Random Bot

Baseline. Random valid play.

## Knows

- Valid actions (from engine)

## Does

- Picks randomly from `state.valid_actions()`

## Doesn't

- Consider card values
- Track anything
- Have preferences

## Use Case

- Baseline for testing
- "Drunk player" simulation
- Verify game terminates with any valid play sequence
