# 010: Basic Bot

a000 target. Simple heuristics, no memory.

## Knows

- Card point values
- Current trick state
- Own hand

## Does

**Passing:**

- Pass Q♠ if held
- Pass high spades (A, K) to avoid taking Q♠
- Pass high hearts
- Prefer passing high cards

**Playing:**

- Follow suit (required)
- When void: dump Q♠ first, then high hearts, then high cards
- When leading: low non-hearts, avoid Q♠ early

**Moon choice:**

- Add to others if ahead/tied, subtract if behind

## Doesn't

- Track cards played
- Count suits
- Model opponents
- Detect moon attempts (own or others)

## Implementation

~25 lines. Three functions: `pass_priority()`, `select_play()`,
`choose_moon_option()`.
