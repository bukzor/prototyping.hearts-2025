# 2025-12-16-002: Design Planning Session

## Focus

Entity analysis and architectural decisions for renderer and bot packages before
implementation.

## What Happened

**Entity analysis:**

- Reviewed existing skeleton tests for renderer_cli and bot
- Compared planned entities against test structure
- Identified renderer components: CardFormatter, HandRenderer, TrickRenderer,
  ScoreRenderer, InputParser
- Identified bot components: PassSelection, CardSelection, MoonShooting

**Key architectural decisions:**

1. **Thin renderer** — All formatting, parsing, sorting, grouping logic lives in
   engine. Renderer is pure I/O adapter.

2. **`__tty__` protocol** — Engine types implement `__tty__()` for ANSI-colored
   output. `tty.format()` function auto-detects terminal.

3. **`Player` protocol** — Bot and Human share interface:
   `choose_action(state) -> PlayerAction`. Game loop is uniform.

4. **Log-style output** — Not ncurses for a000. Sequential append-only output,
   privacy by honor system.

**Bot levels KB created:**

- 000-random: Baseline, random valid play
- 010-basic: a000 target, ~25 lines of heuristics
- 030-counting: Tracks cards played
- 050-tactical: Opponent modeling, moon awareness
- 070-analytical: Probability, simulation
- 090-optimal: Aspirational ceiling

## Decisions

- Push shared logic to engine (if CLI and ncurses would share it, it's domain
  logic)
- Human player impl is per-renderer (implements Player protocol)
- Bot is simple functions, not classes (~25 lines total for 010-basic)

## Files Changed

```
docs/dev/adr/2025-12-16-010-thin-renderer.md (new)
docs/features.kb/bots.md (updated)
docs/features.kb/bots.kb/ (new directory, 7 files)
docs/milestones.kb/a000-local-prototype.md (updated)
```

## Next Session

1. Implement `tty.py` in engine (protocol + format function)
2. Add `__tty__()` to Card, Suit, Rank
3. Add `sort_hand()`, `group_hand()`, `Card.parse()` to engine
4. Add `Player` protocol to engine
5. Implement 010-basic bot
6. Implement CLI renderer (Human class)
7. Wire together game loop
